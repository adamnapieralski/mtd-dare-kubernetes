# mtd-dare-kubernetes

## minikube
Make sure you have minikube running with k8s cluster and Ingress addon enabled
```
minikube addons list
minikube addons enable ingress
```

## Apply configuration
You need to create nginx and apache services, deployments and configure Ingress for them using proper _.yaml_ files. This may be done with provided script:
```
./k8s_apply.sh
```
After creation, it takes a while for the deployments to get ready (since they're pulling Docker images). You may observe status with
```
kubectl get deployment -w
```

## Reaching servers
Current configuration should route $(minikube ip) and apache.k8s to apache, and nginx.k8s.com to nginx (after setting values in `/etc/hosts`).