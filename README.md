# mtd-dare-kubernetes
Implementation of Moving Target Defense (MTD) Dynamic  Application  Rotation  Environment  (DARE) solution in Kubernetes. Services are Apache & nginx used by Wordpress deployments.

## minikube
Make sure you have minikube running with k8s cluster and Ingress addon enabled
```
minikube addons list
minikube addons enable ingress
```

## Prometheus
Add Prometheus for resource measurements using provided script
```
cd prometheus && ./add_prometheus.sh
```

## Apply configuration
You need to create nginx and apache services, deployments and configure Ingress for them using proper _.yaml_ files. This may be done with provided script, which is available in each of wordpres/mtd-.* variants:
```
./k8s_apply.sh
```
After creation, it takes a while for the deployments to get ready (since they're pulling Docker images). You may observe status with
```
kubectl get deployment -w
```

## Reaching servers
Ingress exposes currently set service at minikube ip (that can be found using `minikube ip` command - often 192.168.x.x).