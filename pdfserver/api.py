import requests
import tempfile

from flask import Blueprint, request, make_response

from config.default import WKHTML_BINARY


api = Blueprint('api', __name__)
import logging


def urltopdf(url):
    #with open("/tmp/o.pdf", "w+") as tpdf:
    with tempfile.NamedTemporaryFile(delete=False) as tpdf:
        cmd=[]
        cmd.append(WKHTML_BINARY)
        cmd.extend(["--viewport-size", "8000x800",
            "-O", "Landscape",
             "--no-stop-slow-scripts",
            url, tpdf.name])
        logging.info("cmd=\n{}".format(" ".join(cmd)))
        import subprocess
        subprocess.call(cmd)
        resultingPdf = tpdf.read()
        return resultingPdf


def FetchTitle(weburl):
    r = requests.get(weburl)
    r.encoding = 'utf-8'
    html = r.text
    start = html.find("<title>")
    end = html.find("</title>")
    if start == -1 or end == -1:
        logging.info("Cannot parse title")
        return None
    else:
        title = html[start + len("<title>"): end].strip()
        logging.info("Parsed title is: {}".format(title))
        return title
    return

@api.route("/generateFromURL", methods=['POST'])
def generateFromURL():
    data = request.form.to_dict(flat=True)
    weburl = data['weburl']

    try:
        title = FetchTitle(weburl)
        if not title:
            import datetime
            title = datetime.datetime.now()
    except Exception as e:
        raise e


    resultingPdf = urltopdf(weburl)
    response = make_response(resultingPdf)
    response.headers['Content-Disposition'] = "attachment; filename={}.pdf".format(title)
    response.mimetype = 'application/pdf'
    return response

