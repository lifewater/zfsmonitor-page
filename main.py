from flask import Flask, Response, render_template, jsonify
app = Flask(__name__)
import psutil
import platform
import json
import time
import random
from datetime import datetime
random.seed()

@app.route("/")
def index():
    return render_template('template.html')


@app.route("/_avg_cpu")
def _avg_cpu():
    util = psutil.cpu_percent()
    return jsonify(result = f'{util:.2f}%')
    
@app.route('/cpu-chart-data')
def chart_data():
    print ("You made it here")
    def get_cpu_utilization():
        while True:
            util = psutil.cpu_percent()
            json_data = json.dumps({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    return Response(get_cpu_utilization(), mimetype='text/event-stream') 
 
@app.route("/cpu")
def cpu():
    cpu = {}
    cpu["cpu"] = platform.processor()
    cpu["machine"] = platform.processor()
    cpu["node"] = platform.processor()
    cpu["system"] = platform.system()
    cpu["threads"] = psutil.cpu_count()
    cpu["cores"] = psutil.cpu_count(logical=False)
    
    tmp = platform.uname()
    print (tmp)
    return render_template('cpu.html', results = cpu)
    
if __name__ == '__main__':
    app.run(debug=True, threaded=True)