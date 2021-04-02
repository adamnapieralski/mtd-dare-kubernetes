kubectl apply -f service-nginx.yaml
kubectl apply -f service-apache.yaml

kubectl apply -f deployment-nginx.yaml
kubectl apply -f deployment-apache.yaml

kubectl apply -f ingress.yaml