import time
import sys
import subprocess

ingress_file = 'ingress.yaml'
ingress_name = 'app-ingress'

def patches_generator():
    svc_names = ['wordpress-apache', 'wordpress-nginx']
    i = 0
    while True:
        i = (i + 1) % 2
        yield svc_names[i]

def run_command(command):
    print("command:", command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    print("output:", output.decode('utf-8'))
    return error is not None

def init():
    return run_command('./k8s_apply.sh')

def patch(svc_name):
    cmd = "kubectl patch ingresses.v1.networking.k8s.io {} --type=json -p=".format(ingress_name)
    cmd += "'[{" + '"op": "replace", "path": "/spec/rules/0/http/paths/0/backend/service/name", "value": "{}"'.format(svc_name)
    cmd += "}]'"
    return run_command(cmd)

def run_mtd(dt):

    patches = patches_generator()

    while True:
        patch(next(patches))
        time.sleep(dt)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dt = int(sys.argv[1])
    else:
        dt = 10

    run_mtd(dt)



