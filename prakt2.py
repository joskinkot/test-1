#  we are testing github

from flask import Flask, request, jsonify
import shutil  #disk usage
import psutil #memory usage
import platform #comp Info
import time 
from datetime import datetime

app = Flask(__name__)

metrics_data = []

@app.route('/metrics', methods=['POST']) #metrics
def add():
    data = request.get_json(silent=True)
    if not data or not ( data.get("login") == "admin" and data.get("password") == "admin"):
       metrics_data.append({"message": "Unauthorized"})
    else:
        #get disk info
        disk_usage = shutil.disk_usage("C:/")
        totalD = disk_usage.total / (1024 ** 3)      # at all in gb
        usedD = disk_usage.used / (1024 ** 3)        #using
        freeD = disk_usage.free / (1024 ** 3)        # free
        #get operative-memory info
        memory_usage = psutil.virtual_memory()
        totalOM = memory_usage.total / (1024 ** 3)
        usedOM = memory_usage.used / (1024 ** 3)
        freeOM = memory_usage.free / (1024 ** 3)
        #get computer ID
        computer = platform.node()
        #get time
        """start_time = psutil.boot_time()        #time of starting
    start_datetime = datetime.fromtimestamp(start_time)    #time of starting in datetime format
    now_time = datetime.now()                     #time of now
    up_time = now_time - start_datetime
    """
        uptime_sec=int(time.time()-psutil.boot_time())
        hours, rem =divmod(uptime_sec, 3600)
        minutes, secinds = divmod(rem,60)
        uptime_str = f"{hours}h {minutes}m {secinds}s"
        metrics_data.append ({"debug": uptime_sec,
                        "disk": {"total": totalD, "used": usedD, "free": freeD},
                        "memory": {"total": totalOM, "used": usedOM, "free": freeOM},
                        "computer": {"ID": computer, "OS": platform.release(), "Arch": platform.machine(), "UP_time":{"sec":uptime_sec, "time": uptime_str}}}) #pievieno datus


    return jsonify(metrics_data),200         #(ievada datus json format ),200 - ja viss OK


@app.route('/login', methods = ['GET'])
def get():
    return jsonify(metrics_data),200               #izvada datus       #(ievada datus json formata ),200 - ja viss OK+


@app.route('/login', methods = ['DELETE'])
def delete():
    metrics_data.clear()                                    #nodzezta datus
    return jsonify({"message": "Dati izdsesti"}),200        #(ievada datus json formata ),200 - ja viss OK

if __name__ == '__main__':
    app.run(debug = True)
