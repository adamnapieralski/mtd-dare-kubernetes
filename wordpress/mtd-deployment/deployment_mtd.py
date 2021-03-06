import time
import sys
import subprocess

deployment_name = 'wordpress'
container_name = 'wordpress'

def patches_generator():
    images = ['bitnami/wordpress:5.7.2', 'bitnami/wordpress-nginx:5.7.2']
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

def run_mtd(dt, patches_num=100000000):
    patches = patches_generator()
    patches_counter = 1

    while patches_counter <= patches_num:
        patch(next(patches))
        time.sleep(dt)
        patches_counter += 1

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dt = int(sys.argv[1])
        if len(sys.argv) > 2:
            patches_num = int(sys.argv[2])
        else:
            patches_num = 100000000
    else:
        dt = 30
        patches_num = 100000000
    run_mtd(dt, patches_num=patches_num)



