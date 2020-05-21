from flask import Flask, Response, request

class MyResponse(Response):
    default_mimetype = "text/plain"

app = Flask(__name__)
app.response_class = MyResponse

logo = """
 ____   ___    __  __ __   ___
|    \ /  _]  /  ]|  |  | /   \ 
|  o  )  [_  /  / |  |  ||     |
|   _/    _]/  /  |  _  ||  O  |
|  | |   [_/   \_ |  |  ||     |
|  | |     \     ||  |  ||     |
|__| |_____|\____||__|__| \___/

"""

logo = """
██████╗ ███████╗ ██████╗██╗  ██╗ ██████╗
██╔══██╗██╔════╝██╔════╝██║  ██║██╔═══██╗
██████╔╝█████╗  ██║     ███████║██║   ██║
██╔═══╝ ██╔══╝  ██║     ██╔══██║██║   ██║
██║     ███████╗╚██████╗██║  ██║╚██████╔╝
╚═╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝
"""

@app.route('/')
def index():
    resp = f"""<pre>
{logo}
Welcome to pecho.
<a href="/ip">/ip</a> - return ip
<a href="/echo">/echo</a> - echo request info
</pre>
"""

    return MyResponse(response=resp, mimetype="text/html")

@app.route('/echo')
def echo():
    resp = f"{logo}\n"

    resp += "Headers\n"
    for h in request.headers:
        resp += ": ".join(str(i) for i in h) + "\n"

    resp += "\nRequest Info\n"
    for x in ['full_path', 'host',
            'method', 'path', 'query_string',
            'referrer', 'remote_addr', 'remote_user',
            'scheme', 'url', 'url_charset']:
        resp += f"{x}: {str(getattr(request,x))}\n"

    return resp

@app.route('/ip')
def ip():
    if 'x-real-ip' in request.headers:
        ip = request.headers['X-Real-Ip']
    else:
        ip = request.remote_addr

    resp = f"{ip}\n"
    return resp

#@app.route('/requestobj')
#def requestobj():
#    resp = ""
#
#    gen = (k for k in dir(request) if k is not None)
#    for k in gen:
#        resp += f"{k}: {getattr(request,k)}\n"
#
#    return resp

