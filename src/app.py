from flask import Flask, Response, request
import re

class MyResponse(Response):
    default_mimetype = "text/plain"

app = Flask(__name__)
app.response_class = MyResponse

all_methods = ['GET', 'HEAD', 'POST', 'PUT', 'OPTIONS', 'DELETE']

logo = """
 ██████╗ ███████╗███████╗██╗     ███████╗ ██████╗   ███╗   ███╗███████╗
 ██╔══██╗██╔════╝██╔════╝██║     ██╔════╝██╔════╝   ████╗ ████║██╔════╝
 ██████╔╝█████╗  █████╗  ██║     █████╗  ██║        ██╔████╔██║█████╗
 ██╔══██╗██╔══╝  ██╔══╝  ██║     ██╔══╝  ██║        ██║╚██╔╝██║██╔══╝
 ██║  ██║███████╗██║     ███████╗███████╗╚██████╗██╗██║ ╚═╝ ██║███████╗
 ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚══════╝ ╚═════╝╚═╝╚═╝     ╚═╝╚══════╝
"""

def get_echo():
    resp = "Headers\n"
    for h in request.headers:
        resp += ": ".join(str(i) for i in h) + "\n"

    resp += "\nRequest Info\n"
    for x in ['full_path', 'host',
            'method', 'path', 'query_string',
            'referrer', 'remote_addr', 'remote_user',
            'scheme', 'url', 'url_charset']:
        resp += f"{x}: {str(getattr(request,x))}\n"

    return resp

def clean_status(status):
    try:
        cleaned = re.findall('[1-5]{1}[0-9]{2}', str(status))
        return cleaned[0]
    except:
        return 404

@app.route('/')
def index():
    echo = get_echo()
    resp = f"""<pre>
{logo}
reflec.me - simple reflective utilities.

<a href="/ip">/ip</a> - return ip
<a href="/echo">/echo</a> - echo request info
<a href="/status/XXX">/status/XXX</a> - respond with given status code
-----------------------------------

{echo}
</pre>
"""

    return MyResponse(response=resp, mimetype="text/html")


@app.route('/echo')
def echo():
    resp = f"{logo}\n"
    resp += get_echo()
    return resp


@app.route('/ip')
def ip():
    if 'cf-connecting-ip' in request.headers:
        ip = request.headers['cf-connecting-ip']
    elif 'x-real-ip' in request.headers:
        ip = request.headers['X-Real-Ip']
    else:
        ip = request.remote_addr

    resp = f"{ip}\n"
    return resp


@app.route('/status/<code>', methods = all_methods )
def status(code):
    code = clean_status(code)
    resp = f"{logo}\n{code}\n"

    return MyResponse(response=resp, status=code)

#@app.route('/requestobj')
#def requestobj():
#    resp = ""
#
#    gen = (k for k in dir(request) if k is not None)
#    for k in gen:
#        resp += f"{k}: {getattr(request,k)}\n"
#
#    return resp

