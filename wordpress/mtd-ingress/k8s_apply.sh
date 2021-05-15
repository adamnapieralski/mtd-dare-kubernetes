kubectl apply -f ../mysql-secrets.yaml
kubectl apply -f ../mysql-deployment.yaml
kubectl apply -f ../wordpress-persistent-volume.yaml
kubectl apply -f ingress.yaml
kubectl apply -f ../ingress-config.yaml -n kube-system

kubectl apply -f wordpress-deployment-apache.yaml
sleep 5
kubectl apply -f wordpress-deployment-nginx.yaml