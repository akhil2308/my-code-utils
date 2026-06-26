# jq Cheat Sheet

## Basics
```bash
echo '{"a":1,"b":2}' | jq '.'            # pretty-print
jq '.a' file.json                        # value of key "a"
jq '.user.name' file.json                # nested key
jq '.items[]' file.json                  # iterate array elements
jq '.items[0]' file.json                 # first element
jq '.items[-1]' file.json                # last element
jq '.items[2:5]' file.json               # slice (index 2..4)
jq '.["weird key"]' file.json            # key with spaces/special chars
jq '.a?' file.json                       # optional: no error if .a missing
```

## Select / filter
```bash
jq '.[] | select(.age > 30)' file.json           # filter by condition
jq '.[] | select(.name == "akhil")' file.json    # equality
jq '.[] | select(.tags | contains(["x"]))'       # array contains
jq '.[] | select(.email | test("@gmail"))'       # regex test
jq 'map(select(.active))' file.json              # keep only active
jq '.[] | select(.x != null)' file.json          # drop nulls
```

## Map / transform
```bash
jq 'map(.price)' file.json               # array of one field
jq 'map(.price * 1.1)' file.json         # transform each
jq '[.[] | .name]' file.json             # collect into new array
jq '.items |= map(.qty + 1)' file.json   # update in place
jq 'sort_by(.age)' file.json             # sort
jq 'group_by(.dept)' file.json           # group into arrays
jq 'unique_by(.id)' file.json            # dedupe by key
jq 'add' file.json                       # sum numbers / merge objects
jq 'length' file.json                    # count elements / string length
jq '[.[].price] | add' file.json         # sum a field
```

## Build objects
```bash
jq '{name: .name, id: .id}' file.json            # pick fields into new object
jq '.[] | {n: .name, total: (.a + .b)}'          # computed field
jq '{count: length, items: .}' file.json         # wrap
jq 'to_entries' file.json                        # {a:1} -> [{key:"a",value:1}]
jq 'from_entries' file.json                      # inverse of to_entries
jq 'with_entries(.value |= . * 2)' file.json     # transform every value
jq 'keys' file.json                              # object keys (sorted)
jq 'has("name")' file.json                       # bool: key present
```

## Raw / CSV / TSV output
```bash
jq -r '.name' file.json                  # raw string (no quotes)
jq -r '.[] | .name' file.json            # one name per line
jq -r '.[] | [.id, .name] | @csv'        # CSV rows
jq -r '.[] | [.id, .name] | @tsv'        # TSV rows
jq -r 'keys[]' file.json                 # keys, one per line
jq -r '.[] | "\(.id): \(.name)"'         # string interpolation
jq -rn 'inputs | .id' file.json          # stream multiple JSON docs
```

## Variables / args / env
```bash
jq --arg name "akhil" '.[] | select(.name == $name)'   # pass a string in
jq --argjson n 30 '.[] | select(.age > $n)'            # pass a number/JSON in
jq -n --arg v "$HOME" '{home: $v}'                     # build from shell var
jq '.token = env.API_TOKEN' file.json                  # read from environment
```

## Common curl-pipe recipes
```bash
curl -s api/users | jq '.[].email'                          # extract a field from a list
curl -s api/users | jq -r '.[] | [.id,.name] | @csv'        # API -> CSV
curl -s api/user/1 | jq '{id, name, email}'                 # shorthand: keys = same-named fields
curl -s api/data | jq '.results | length'                   # count results
curl -s api/data | jq -e '.error' && echo "had error"       # -e sets exit code from output
kubectl get pods -o json | jq -r '.items[].metadata.name'   # k8s names
```
