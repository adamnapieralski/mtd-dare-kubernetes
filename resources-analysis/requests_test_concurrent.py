import time
import subprocess
import threading
import queue
import asyncio
import sys
from datetime import datetime

from requests_html import AsyncHTMLSession


def minikube_url():
    process = subprocess.Popen('minikube ip', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode('utf-8').strip()
    print("minikube ip:", output)
    return output

def current_datetime_string():
    return datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

URL = "http://{}/".format(minikube_url())
LOG_FILE_PATH = "requests.{}.log".format(current_datetime_string())
TASKS_NUM = 5
INTERVAL_MS = 5000


class LoggerThread(threading.Thread):
    def __init__(self, file_path, results_queue):
        threading.Thread.__init__(self)
        self.file_path = file_path
        self.results_queue = results_queue

    def append_to_file(self, request_params):
        line = ""
        for p in request_params:
            line += str(p) + ","
        line += "\n"

        with open(self.file_path, "a") as log_file:
            log_file.write(line)

    def run(self):
        while True:
            new_request_params = self.results_queue.get()
            self.append_to_file(new_request_params)


class RequestsManager():
    def __init__(self, tasks_num, url, interval_ms, results_queue):
        self.tasks_num = tasks_num
        self.url = url
        self.interval_ms = interval_ms
        self.results_queue = results_queue
        self.loop = None

    async def make_request(self, id, asession, url):
            timestamp = datetime.now().isoformat()
            r = await asession.get(url)
            start = time.time()
            await r.html.arender()
            render_time = time.time() - start

            status_code = r.status_code
            server = None
            if "Server" in r.headers:
                server = r.headers['Server']
            request_time = r.elapsed.total_seconds()
            total_time = request_time + render_time

            return [timestamp, id, total_time, request_time, render_time, status_code, server]

    async def make_request_task(self, id):
        asession = AsyncHTMLSession()
        while True:
            res = await self.make_request(id, asession, self.url)
            self.results_queue.put(res)
            await asyncio.sleep(self.interval_ms / 1000.)

    async def make_all_request_tasks(self):
        tasks = []
        for i in range(self.tasks_num):
            tasks.append(asyncio.ensure_future(self.make_request_task(i)))

        await asyncio.gather(*tasks)

    def stop(self):
        self.loop.stop()

    def run(self):
        self.loop = asyncio.get_event_loop()
        try:
            asyncio.ensure_future(self.make_all_request_tasks())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()


def stop_rm_after_time(rm, run_time):
    start_time = datetime.now()
    elapsed = 0
    while elapsed < run_time:
        time.sleep(0.1)
        elapsed = (datetime.now() - start_time).total_seconds()
    rm.stop()

def run(tasks_num, interval_ms, run_time, filename_info):
    results_queue = queue.Queue()
    log_file_path = "requests.{}.{}.log".format(filename_info, current_datetime_string())

    lt = LoggerThread(log_file_path, results_queue)
    lt.setDaemon(True)
    lt.start()

    rm = RequestsManager(tasks_num, URL, interval_ms, results_queue)

    thread = threading.Thread(target=stop_rm_after_time, args=(rm, run_time))
    thread.start()

    rm.run()


if __name__ == "__main__":
    if len(sys.argv) > 3:
        TASKS_NUM = int(sys.argv[1])
        INTERVAL_MS = int(sys.argv[2])
        run_time = int(sys.argv[3])
    else:
        run_time = 120

    run(TASKS_NUM, INTERVAL_MS, run_time, 'mtd-deployment.i15.with-req.mtd')
