#!/bin/bash

kubectl delete svc --all
kubectl delete deployment --all
kubectl delete pod --all
kubectl delete ingress --all

if [ "$1" == 'pv' ]
then
    kubectl delete pvc --all
    kubectl delete pv --all
fi
