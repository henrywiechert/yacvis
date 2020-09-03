import dash_core_components as dcc
import dash_html_components as html
import dash_table
import platform,socket,re,uuid,json,psutil,multiprocessing
import logging
import numpy as np
import pandas as pd

def getSystemInfo():
        try:
            info={}
            info['platform']=platform.system()
            info['platform-release']=platform.release()
            info['platform-version']=platform.version()
            info['architecture']=platform.machine()
            info['hostname']=socket.gethostname()
            info['ip-address']=socket.gethostbyname(socket.gethostname())
            info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
            info['processor']=platform.processor()
            info['cpu-count']=multiprocessing.cpu_count()
            info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
            return json.dumps(info)
        except Exception as e:
            logging.exception(e)

layout = html.Div([html.H3('System Information'),
                  getSystemInfo()])
