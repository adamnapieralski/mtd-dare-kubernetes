kubectl apply -f ../mysql-secrets.yaml
kubectl apply -f ../mysql-deployment.yaml
kubectl apply -f ../wordpress-persistent-volume.yaml
kubectl apply -f ingress.yaml
kubectl apply -f ../ingress-config.yaml -n kube-system

kubectl apply -f wordpress-deployment.yaml
kubectl apply -f wordpress-service.yaml
