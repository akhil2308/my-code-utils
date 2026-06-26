# Docker Cheat Sheet

Daily commands. Compose stacks for specific services live in the sibling folders here.

## Containers
```bash
docker ps                       # running
docker ps -a                    # all, including stopped
docker run -d --name web -p 8080:80 nginx
docker run -it --rm ubuntu bash # interactive, auto-remove on exit
docker exec -it web bash        # shell into running container
docker logs -f web              # follow logs
docker stop web ; docker start web ; docker restart web
docker rm web                   # remove (stopped) container
docker rm -f web                # force remove running
```

## Images
```bash
docker images
docker pull postgres:16
docker build -t myapp:latest .
docker tag myapp:latest myrepo/myapp:1.0
docker push myrepo/myapp:1.0
docker rmi <image>
docker history <image>          # layers
```

## Inspect & debug
```bash
docker inspect web              # full JSON metadata
docker inspect -f '{{.NetworkSettings.IPAddress}}' web
docker stats                    # live CPU/mem per container
docker top web                  # processes in container
docker cp web:/path/file ./     # copy out of container
docker cp ./file web:/path      # copy into container
```

## Compose
```bash
docker compose up -d            # start in background
docker compose up -d --build    # rebuild then start
docker compose down             # stop + remove containers/networks
docker compose down -v          # also remove volumes (destructive)
docker compose ps
docker compose logs -f <svc>
docker compose exec <svc> bash
docker compose restart <svc>
```

## Volumes & networks
```bash
docker volume ls ; docker volume rm <vol>
docker network ls ; docker network inspect <net>
docker run -v $(pwd):/app ...   # bind mount cwd
docker run -v mydata:/data ...  # named volume
```

## Cleanup (free disk)
```bash
docker system df                # what's using space
docker container prune          # remove stopped containers
docker image prune              # remove dangling images
docker image prune -a           # remove all unused images
docker volume prune             # remove unused volumes
docker system prune -a --volumes  # nuke everything unused (careful)
```
