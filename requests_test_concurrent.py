import time
import subprocess
import datetime
import threading
import queue
import asyncio

from requests_html import AsyncHTMLSession


def minikube_url():
    process = subprocess.Popen('minikube ip', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode('utf-8').strip()
    print("minikube ip:", output)
    return output

def current_datetime_string():
    return datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

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
    def __init__(self, tasks_num, url, interval_ms):
        self.tasks_num = tasks_num
        self.url = url
        self.interval_ms = interval_ms

    async def make_request(self, id, asession, url):
            timestamp = datetime.datetime.now().isoformat()
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

    async def make_request_task(self, id, results_queue, url, interval_ms):
        asession = AsyncHTMLSession()
        while True:
            res = await self.make_request(id, asession, url)
            results_queue.put(res)
            await asyncio.sleep(interval_ms / 1000.)

    async def make_all_request_tasks(self, tasks_num, results_queue, url, interval_ms):
        tasks = []
        for i in range(self.tasks_num):
            tasks.append(asyncio.ensure_future(self.make_request_task(i, results_queue, url, interval_ms)))

        await asyncio.gather(*tasks)

    def run(self):
        loop = asyncio.get_event_loop()
        try:
            asyncio.ensure_future(self.make_all_request_tasks(self.tasks_num, results_queue, self.url, self.interval_ms))
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()


if __name__ == "__main__":
    results_queue = queue.Queue()

    lt = LoggerThread(LOG_FILE_PATH, results_queue)
    lt.start()

    rm = RequestsManager(TASKS_NUM, URL, INTERVAL_MS)
    rm.run()
