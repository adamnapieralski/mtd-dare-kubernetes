import time
import json
import sys
from datetime import datetime
from prometheus_api_client import PrometheusConnect

INTERVAL = 5 # sec

# NAME_SEARCH = ".*wordpress-nginx.*|.*wp-apache.*"
NAME_SEARCH = ".*wordpress.*"

prom = PrometheusConnect(url ="http://192.168.49.2:30943/", disable_ssl=True)

def current_datetime_string():
    return datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

DATA_FILE_PATH = "resource-metrics.{}.json".format(current_datetime_string())


def get_cpu_metrics(name, rate_time="30s"):
    q = 'sum(rate(container_cpu_usage_seconds_total{{name=~"{}"}}[{}])) by (pod)'.format(name, rate_time)
    # 'rate(container_cpu_user_seconds_total[30s]) * 100'
    res = prom.custom_query(q)
    data = []
    if res:
        data = [{ "pod": measure["metric"]["pod"], "cpu": float(measure["value"][1]) } for measure in res]
    return data

def get_memory_metrics(name):
    q = 'sum(container_memory_usage_bytes{{name=~"{}"}}) by (pod)'.format(name)
    res = prom.custom_query(q)
    data = []
    if res:
        data = [{ "pod":  measure["metric"]["pod"], "memory": int(measure["value"][1]) / 1024 / 1024 } for measure in res]
    return data

def get_all_metrics(name, rate_time='3m'):
    data_cpu = get_cpu_metrics(name, rate_time)
    data_memory = get_memory_metrics(name)
    pods = {entry["pod"] for entry in data_cpu + data_memory}

    data = []
    timestamp = datetime.now().isoformat()
    for pod in pods:
        pod_data = { "timestamp": timestamp }
        pod_data["pod"] = pod
        pod_data["cpu"] = next((entry["cpu"] for entry in data_cpu if entry["pod"] == pod), None)
        pod_data["memory"] = next((entry["memory"] for entry in data_memory if entry["pod"] == pod), None)
        data.append(pod_data)
    return data

def run(run_time, filename_info):
    start_time = datetime.now()
    elapsed = 0
    data = []

    data_file_path = "resource-metrics.{}.{}.json".format(filename_info, current_datetime_string())

    while elapsed < run_time:
        sample_data = get_all_metrics(NAME_SEARCH)
        data.extend(sample_data)
        print(sample_data)
        json.dump(data, open(data_file_path, "w"))
        time.sleep(INTERVAL)
        elapsed = (datetime.now() - start_time).total_seconds()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_time = int(sys.argv[1])
    else:
        run_time = 240

    run(run_time, 'test')
