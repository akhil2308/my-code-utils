# kubectl Cheat Sheet

## Context & config
```bash
kubectl config get-contexts
kubectl config use-context <ctx>      # switch cluster
kubectl config set-context --current --namespace=mns   # default ns
kubectl cluster-info
```

## Get / inspect
```bash
kubectl get pods                      # in current namespace
kubectl get pods -A                   # all namespaces
kubectl get pods -o wide              # + node, IP
kubectl get pods -w                   # watch
kubectl get svc,deploy,ingress        # multiple resource types
kubectl describe pod <pod>            # events + full state (debug start here)
kubectl get events --sort-by=.lastTimestamp
```

## Logs & exec
```bash
kubectl logs <pod>
kubectl logs -f <pod>                 # follow
kubectl logs <pod> -c <container>     # specific container
kubectl logs <pod> --previous         # crashed container's last logs
kubectl exec -it <pod> -- bash        # shell in
kubectl exec <pod> -- env             # one-off command
```

## Port-forward (reach a pod/service locally)
```bash
kubectl port-forward pod/<pod> 8080:80
kubectl port-forward svc/<svc> 5432:5432
```

## Apply / delete
```bash
kubectl apply -f manifest.yaml
kubectl apply -f ./dir/               # all manifests in a dir
kubectl delete -f manifest.yaml
kubectl delete pod <pod>              # gets recreated if managed by a Deployment
```

## Scale & rollout
```bash
kubectl scale deploy/<name> --replicas=3
kubectl rollout status deploy/<name>
kubectl rollout restart deploy/<name> # rolling restart (re-pull config/secrets)
kubectl rollout undo deploy/<name>    # roll back to previous revision
kubectl set image deploy/<name> app=myimage:2.0
```

## Debug
```bash
kubectl get pod <pod> -o yaml         # full spec
kubectl top pod                       # CPU/mem (needs metrics-server)
kubectl top node
kubectl run tmp --rm -it --image=busybox -- sh   # throwaway debug pod
kubectl cp <pod>:/path/file ./        # copy file out
```

## Secrets & configmaps
```bash
kubectl get secret <name> -o jsonpath='{.data.key}' | base64 -d
kubectl create configmap myconf --from-file=config.yaml
kubectl create secret generic mysecret --from-literal=PASSWORD=xyz
```

## Quick aliases worth setting
```bash
alias k=kubectl
alias kgp='kubectl get pods'
alias kl='kubectl logs -f'
# kubectl completion: source <(kubectl completion bash)
```
