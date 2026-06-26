# psql / Postgres Cheat Sheet

Complements `SQL/SQL-cheat-sheet.pdf` and the postgres/pgvector docker stacks.

## Connect
```bash
psql -h localhost -U postgres -d mydb
psql "postgresql://user:pass@host:5432/mydb"
PGPASSWORD=secret psql -h host -U user -d db   # non-interactive
```

## psql meta-commands (inside the shell)
```
\l              list databases
\c dbname       connect to a database
\dt             list tables
\d tablename    describe a table (columns, indexes, FKs)
\di             list indexes
\dn             list schemas
\du             list roles/users
\df             list functions
\dv             list views
\x              toggle expanded (vertical) output — great for wide rows
\timing         toggle query timing
\e              edit query in $EDITOR
\i file.sql     run a SQL file
\copy (SELECT...) TO 'out.csv' CSV HEADER   client-side CSV export
\q              quit
```

## Roles & permissions
```sql
CREATE ROLE app WITH LOGIN PASSWORD 'secret';
GRANT CONNECT ON DATABASE mydb TO app;
GRANT USAGE ON SCHEMA public TO app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT ON TABLES TO app;            -- future tables too
```

## Inspect / admin queries
```sql
-- Active queries
SELECT pid, state, query, age(now(), query_start) AS runtime
FROM pg_stat_activity WHERE state != 'idle' ORDER BY runtime DESC;

-- Kill a query / connection
SELECT pg_cancel_backend(<pid>);     -- gentle
SELECT pg_terminate_backend(<pid>);  -- force

-- Table & index sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) AS size
FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC;

-- Database sizes
SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database;

-- Find missing indexes (high seq scans)
SELECT relname, seq_scan, idx_scan
FROM pg_stat_user_tables ORDER BY seq_scan DESC LIMIT 10;

-- Unused indexes (candidates to drop)
SELECT relname, indexrelname, idx_scan
FROM pg_stat_user_indexes WHERE idx_scan = 0;
```

## Performance
```sql
EXPLAIN ANALYZE SELECT ...;     -- real execution plan + timings
VACUUM ANALYZE tablename;        -- reclaim space + refresh stats
REINDEX TABLE tablename;
```

## Backup / restore (shell)
```bash
pg_dump -h host -U user -d mydb -F c -f mydb.dump   # custom format
pg_restore -h host -U user -d mydb mydb.dump
pg_dump -h host -U user mydb > mydb.sql             # plain SQL
psql -h host -U user -d mydb < mydb.sql             # restore plain SQL
```

## pgvector quick reference
```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(1536));
-- nearest neighbors: <-> L2, <=> cosine, <#> inner product
SELECT id FROM items ORDER BY embedding <=> '[...]' LIMIT 5;
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);
```
