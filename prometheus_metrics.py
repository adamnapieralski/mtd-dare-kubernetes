import time
import json
from datetime import datetime
from prometheus_api_client import PrometheusConnect

INTERVAL = 15 # sec

NAME_SEARCH = ".*frontend.*"

prom = PrometheusConnect(url ="http://192.168.49.2:31280/", disable_ssl=True)


def get_cpu_metrics(name, rate_time="3m"):
    q = 'sum(rate(container_cpu_usage_seconds_total{{name=~"{}"}}[{}])) by (pod)'.format(name, rate_time)
    res = prom.custom_query(q)
    data = {}
    if res:
        data = [{ "pod": measure["metric"]["pod"], "cpu": float(measure["value"][1]) } for measure in res]
    return data

def get_memory_metrics(name):
    q = 'sum(container_memory_usage_bytes{{name=~"{}"}}) by (pod)'.format(name)
    res = prom.custom_query(q)
    data = {}
    if res:
        data = [{ "pod":  measure["metric"]["pod"], "memory": int(measure["value"][1]) / 1024 / 1024 } for measure in res]
    return data

def get_all_metrics(name, rate_time='3m'):
    data_cpu = get_cpu_metrics(name, rate_time)
    data_memory = get_memory_metrics(name)
    pods = {entry["pod"] for entry in data_cpu + data_memory}

    data = {}
    for pod in pods:
        data[pod] = {}
        data[pod]["cpu"] = next((entry["cpu"] for entry in data_cpu if entry["pod"] == pod), None)
        data[pod]["memory"] = next((entry["memory"] for entry in data_memory if entry["pod"] == pod), None)
    return data


if __name__ == "__main__":
    data = []
    while True:
        metrics = get_all_metrics(".*frontend.*")
        data.append({ "timestamp": datetime.now().isoformat(), "metrics": metrics })
        print(metrics)
        json.dump(data, open("metrics.json", "w"))
        time.sleep(INTERVAL)
