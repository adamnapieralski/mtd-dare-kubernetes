kubectl apply -f service-backend.yaml
kubectl apply -f deployment-backend.yaml

kubectl apply -f service-frontend-nginx.yaml
kubectl apply -f service-frontend-apache.yaml
# kubectl apply -f service-frontend.yaml

kubectl apply -f deployment-frontend-nginx.yaml
kubectl apply -f deployment-frontend-apache.yaml

kubectl apply -f ingress.yaml

kubectl apply -f ingress-config.yaml -n kube-system