from flask import Flask, Response, request
import os
import re


app = Flask(__name__)

all_methods = ["GET", "HEAD", "POST", "PUT", "OPTIONS", "DELETE"]

if os.environ.get("LOGO") is not None:
    logo = os.environ["LOGO"]
else:
    logo = """
██████╗ ███████╗███████╗██╗     ███████╗ ██████╗   ███╗   ███╗███████╗
██╔══██╗██╔════╝██╔════╝██║     ██╔════╝██╔════╝   ████╗ ████║██╔════╝
██████╔╝█████╗  █████╗  ██║     █████╗  ██║        ██╔████╔██║█████╗
██╔══██╗██╔══╝  ██╔══╝  ██║     ██╔══╝  ██║        ██║╚██╔╝██║██╔══╝
██║  ██║███████╗██║     ███████╗███████╗╚██████╗██╗██║ ╚═╝ ██║███████╗
╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚══════╝ ╚═════╝╚═╝╚═╝     ╚═╝╚══════╝
"""

spacer = "= " * 10


def get_echo():
    resp = "Headers\n"
    for h in request.headers:
        resp += ": ".join(str(i) for i in h) + "\n"

    resp += "\nRequest Info\n"

    fields = [
        "full_path",
        "host",
        "method",
        "path",
        "query_string",
        "referrer",
        "remote_addr",
        "remote_user",
        "scheme",
        "url",
        "url_charset",
    ]

    for x in fields:
        resp += f"{x}: {str(getattr(request,x))}\n"

    return resp


def clean_status(status):
    try:
        cleaned = re.search("[1-5]{1}[0-9]{2}", str(status))
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


@app.route("/")
def index():
    echo = get_echo()
    resp = f"""{logo}
reflec.me - simple reflective utilities.

{spacer}
Paths
<a href="/ip">/ip</a> - return ip
<a href="/echo">/echo</a> - echo request info
<a href="/status/200">/status/XXX</a> - respond with given status code
{spacer}

{echo}
"""

    resp = html_wrap(resp)
    return Response(response=resp)


@app.route("/echo")
def echo():
    resp = f"{logo}\n"
    resp += get_echo()

    resp = html_wrap(resp, "- echo -")
    return Response(response=resp)


@app.route("/ip")
def ip():
    if "cf-connecting-ip" in request.headers:
        ip = request.headers["cf-connecting-ip"]
    elif "x-real-ip" in request.headers:
        ip = request.headers["X-Real-Ip"]
    else:
        ip = request.remote_addr

    resp = f"{ip}\n"
    return Response(response=resp, mimetype="text/plain")


@app.route("/status/", methods=all_methods)
def status_index():
    echo = get_echo()
    resp = f"""{logo}

/status/

Examples:
<a href="/status/200">/status/200</a>
<a href="/status/302">/status/302</a>
<a href="/status/403">/status/403</a>
<a href="/status/500">/status/500</a>

{spacer}

{echo}
"""

    resp = html_wrap(resp, "status")
    return Response(response=resp)


@app.route("/status/<code>", methods=all_methods)
def status(code):
    code = clean_status(code)
    echo = get_echo()
    resp = f"""{logo}
{code}

{spacer}

{echo}
"""

    resp = html_wrap(resp, f"{code}")
    return Response(response=resp, status=code)


@app.errorhandler(404)
def page_not_found(e):
    echo = get_echo()
    resp = f"""{logo}
404.
{spacer}

{echo}
"""

    resp = html_wrap(resp)
    return Response(response=resp, status="404")
