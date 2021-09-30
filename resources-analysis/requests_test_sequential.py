import requests
import time
import sys
import subprocess
import asyncio

from requests_html import AsyncHTMLSession

def minikube_url():
    process = subprocess.Popen('minikube ip', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode('utf-8').strip()
    # print("minikube ip:", output)
    return output

url = "http://{}/".format(minikube_url())
session = AsyncHTMLSession()

async def make_request():
    r = await session.get(url)
    # server = r.headers['Server']
    # print(server)

async def make_request_with_js():
    r = await session.get(url)
    await r.html.arender()
    # server = r.headers['Server']
    # print(server)

async def run_single_request(with_js):
    tb = time.time()
    if with_js:
        await make_request_with_js()
    else:
        await make_request()
    dt = time.time() - tb
    return dt

async def run_requests(interval_ms, with_js):
    i = 0
    while True:
        dt = await run_single_request(with_js)
        print('{},{}'.format(i, dt))
        if interval_ms != 0:
            time.sleep(interval_ms / 1000.)
        i += 1

async def run_num_requests(requests_num, interval_ms, with_js):
    for i in range(requests_num):
        dt = await run_single_request(with_js)
        print('{},{}'.format(i, dt))
        if interval_ms != 0:
            time.sleep(interval_ms / 1000.)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        dt = int(sys.argv[1])
    else:
        dt = 500

    # run_requests(dt, True)
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(run_num_requests(5000, 0, False))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
