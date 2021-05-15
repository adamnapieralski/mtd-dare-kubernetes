import time
import sys
import subprocess

deployment_name = 'hello-frontend'
container_name = 'server'

def patches_generator():
    images = ['kost13/apache-front-test', 'kost13/nginx-test']
    i = 0
    while True:
        i = (i + 1) % 2
        yield images[i]

def run_command(command):
    print("command:", command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    print("output:", output.decode('utf-8'))
    return error is not None

def init():
    return run_command('./k8s_apply.sh')

def patch(patch_image):
    run_command('kubectl set image deployment/{} {}={} --record'.format(deployment_name, container_name, patch_image))

def run_mtd(dt):
    if not init():
        print('Initial error')
        return

    patches = patches_generator()

    while True:
        time.sleep(dt)
        patch(next(patches))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dt = int(sys.argv[1])
    else:
        dt = 30

    run_mtd(dt)



