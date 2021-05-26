import requests_test_concurrent as rtc
import prometheus_metrics as pm
import threading

if __name__ == "__main__":
    # filename_info = "mtd-ingress.i15.req.n5.i5000"
    filename_info = "mtd-deployment.i30.no-req"
    thread = threading.Thread(target=pm.run, args=(60*10, filename_info))
    thread.start()
    # rtc.run(5, 5000, 120, filename_info)
    # pm.run(120, "mtd-ingress.i15.req.tn10.i5000")

