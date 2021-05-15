import time
import sys
import subprocess

deployment_name = 'mtd-deployment'
svc_name = 'mtd-svc'

def patches_generator():
    files = ['patch-apache.yaml', 'patch-nginx.yaml']
    i = 0
    while True:
        i = (i + 1) % 2
        yield files[i]

def run_command(command):
    print("command:", command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    print("output:", output.decode('utf-8'))
    return error is not None

def init():
    return run_command('./k8s_apply.sh')

def patch(patch_file):
    # run_command('kubectl patch svc {} -p "$(cat ../{})"'.format(svc_name, patch_file))
    run_command('kubectl patch deployment {} -p "$(cat {})"'.format(deployment_name, patch_file))

def run_mtd(dt):
    if not init():
        print('Initial error')
        return

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



