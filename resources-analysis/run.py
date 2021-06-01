import requests_test_concurrent as rtc
import prometheus_metrics as pm
import threading

if __name__ == "__main__":
    # filename_info = "mtd-ingress.i15.no-req.0-mtd-0"
    filename_info = "mtd-ingress.i15.with-req.mtd"
    thread = threading.Thread(target=pm.run, args=(60*15, filename_info))
    thread.start()
    # rtc.run(5, 5000, 120, filename_info)
    # pm.run(120, "mtd-ingress.i15.req.tn10.i5000")

