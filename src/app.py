from flask import Flask, Response, request
import re

app = Flask(__name__)

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

def html_wrap(resp, title="< - >"):
    resp = f"""
<html><head><title>reflec.me | {title}</title></head><body>
<pre>
{resp}
</pre>
</body>
</html>
"""

    return resp


@app.route('/')
def index():
    echo = get_echo()
    resp = f"""{logo}
reflec.me - simple reflective utilities.

<a href="/ip">/ip</a> - return ip
<a href="/echo">/echo</a> - echo request info
<a href="/status/200">/status/XXX</a> - respond with given status code
-----------------------------------

{echo}
"""

    resp = html_wrap(resp)
    return Response(response=resp)


@app.route('/echo')
def echo():
    resp = f"{logo}\n"
    resp += get_echo()
    resp = html_wrap(resp, "- echo -")
    return Response(response=resp)


@app.route('/ip')
def ip():
    if 'cf-connecting-ip' in request.headers:
        ip = request.headers['cf-connecting-ip']
    elif 'x-real-ip' in request.headers:
        ip = request.headers['X-Real-Ip']
    else:
        ip = request.remote_addr

    resp = f"{ip}\n"
    return Response(response=resp, mimetype='text/plain')

@app.route('/status(|/)$', methods = all_methods)
def status_index():

    resp = f"""
{logo}

/status

Examples:
<a href="/status/200">/status/200</a>
<a href="/status/403">/status/403</a>
"""

    resp = html_wrap(resp, "status")
    return Response(response=resp)

@app.route('/status/<code>', methods = all_methods )
def status(code):
    code = clean_status(code)
    resp = f"{logo}\n{code}\n"

    resp = html_wrap(resp, f"{code}")
    return Response(response=resp, status=code)

@app.errorhandler(404)
def page_not_found(e):
    resp = f"""{logo}
404.

"""
    resp += get_echo()
    resp = html_wrap(resp)

    return Response(response=resp, status="404")


#@app.route('/requestobj')
#def requestobj():
#    resp = ""
#
#    gen = (k for k in dir(request) if k is not None)
#    for k in gen:
#        resp += f"{k}: {getattr(request,k)}\n"
#
#    return resp

