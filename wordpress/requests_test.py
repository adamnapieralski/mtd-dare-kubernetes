import requests
import time
import sys
import subprocess

from requests_html import HTMLSession

def minikube_url():
    process = subprocess.Popen('minikube ip', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode('utf-8').strip()
    print("minikube ip:", output)
    return output

url = "http://{}/".format(minikube_url())
session = HTMLSession()

def make_request():
    r = requests.get(url)
    server = r.headers['Server']
    print(server)

def make_request_with_js():
    r = session.get(url)
    r.html.render()
    server = r.headers['Server']
    print(server)

def run_requests(interval_ms, with_js):
    while True:
        tb = time.time()
        if with_js:
            make_request_with_js()
        else:
            make_request()
        dt = time.time() - tb
        print('response time: ', dt)
        time.sleep(interval_ms / 1000.)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        dt = int(sys.argv[1])
    else:
        dt = 500

    run_requests(dt, True)