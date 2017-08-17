import requests
import subprocess
import tempfile
import time
import os

from flask import Blueprint, request, make_response, current_app

from config.default import WKHTML_BINARY

api = Blueprint('api', __name__)

DEBUG_M = "ashishthedev@gmail.com"

def localNow():
    return time.asctime(time.localtime(time.time()))

def b2kb(x):
    if type(x) == type(1):
        return x/1024
    return None
def urltopdf(url, max_reattempts=20, threshold_filesize_kb=2000, delayms=200):
    """
    Return pdf binary contents or None
    """

    resultingPdfBinContents = None
    attempt = 0
    while attempt < max_reattempts:
        attempt += 1
        with tempfile.NamedTemporaryFile(dir="./tmpfiles", delete=False) as tpdf:
            cmd=[]
            cmd.append("sudo")
            cmd.append(WKHTML_BINARY)
            cmd.extend(["--viewport-size", "8000x800",
                "-O", "Landscape",
                 "--no-stop-slow-scripts",
                 #"--javascript-delay", str(delayms),
                url, tpdf.name])
            current_app.logger.info("Attempt#{} cmd is =\n{}".format(attempt, " ".join(cmd)))
            try:
                subprocess.call(cmd)
            except Exception as e:
                current_app.logger.error("error: {}".format(e))
                continue


            statinfo = os.stat(tpdf.name)
            if statinfo.st_size > threshold_filesize_kb * 1024:
                resultingPdfBinContents = tpdf.read()
                current_app.logger.info("{} is finalized and successful pdf with actual size: {}kb which is greater than minimum size of {}kb".format(tpdf.name, b2kb(statinfo.st_size), threshold_filesize_kb))
                return resultingPdfBinContents
            else:
                current_app.logger.error("filesize is only {}kb which is less than threshold size of {}kb".format(b2kb(statinfo.st_size), threshold_filesize_kb))

    return None #Could not convert to pdf


def FetchTitle(weburl):
    r = requests.get(weburl, timeout=120)
    r.encoding = 'utf-8'
    html = r.text
    start = html.find("<title>")
    end = html.find("</title>")
    if start == -1 or end == -1:
        current_app.logger.info("Cannot parse title")
        return None
    else:
        title = html[start + len("<title>"): end].strip()
        current_app.logger.info("Parsed title is: {}".format(title))
        return title
    return

@api.route("/ping")
def ping():
    return make_response("OK")

COMMA = ","
@api.route("/generateFromURLAndEmail", methods=['POST', 'GET'])
def generateFromURLAndEmail():
    if request.method == "GET":
        return make_response("Please use POST method to supply params")
    data = request.form.to_dict(flat=True)
    weburl = data['weburl']
    toEmailCSV = data['toEmailCSV']
    ccEmailCSV = data['ccEmailCSV']
    bccEmailCSV = data['bccEmailCSV']
    enduserEmail = data['enduserEmail']
    enduserPhoneNumber = data['enduserPhoneNumber']
    debug_this_flow = weburl.lower().find('debug_this_flow=true') != -1 or \
            weburl.lower().find('debugmode=on') != -1

    toEmailCSV += COMMA + enduserEmail

    try:
        title = FetchTitle(weburl)
        if not title:
            import datetime
            title = datetime.datetime.now()

        resultingPdfBinContents = urltopdf(weburl, max_reattempts=20, threshold_filesize_kb=20, delayms=1*1000)
    except Exception as e:
        current_app.logger.error("Caught Exception: {}".format(e))
        raise

    subject = "Report attached for {enduserEmail}".format(**locals())
    body_success="""
<br>
<br>
<br>
<br>
<table border="0" cellspacing="0" cellpadding="0" width="auto" bgcolor="#dff0d8">
<tbody>
<tr>
<td style="font-weight:bold;color:#3c763d;padding-left:24px; padding-right:24px" height="44" valign="center">Please find your report attached with this email.</td>
</tr>
</tbody>
</table>
<br>
<br>
Web version of the report is present <a href="{weburl}">here</a>.
<br>
<br>
<br>
""".format(weburl=weburl)

    body_failure="""
<br>
<br>
<br>
<br>
<table border="0" cellspacing="0" cellpadding="0" width="auto" bgcolor="#f2dede">
<tbody>
<tr>
<td style="font-weight:bold;color:#a94442;padding-left:24px; padding-right:24px" height="44" valign="center">Sorry we were unable to generate report right now. Please contact jackie@climaterisk.com.au for your personalised report.</td>
</tr>
</tbody>
</table>
<br>
<br>
Web version of the report is present <a href="{weburl}">here</a>.
<br>
<br>
<br>
""".format(weburl=weburl)

    senderur = "moc.liamg@ptmstropervc"
    senderpr = "77noitaulavetamilc"

    if debug_this_flow:
        print("debug_this_flow found. Resetting emails")
        print("Before resetting the values were: toEmailCSV: {toEmailCSV}, ccEmailCSV: {ccEmailCSV}, bccEmailCSV: {bccEmailCSV}".format(**locals()))
        toEmailCSV = ccEmailCSV = bccEmailCSV = DEBUG_M
        subject = subject + "[DEBUG_CV_MAIL]"

    current_app.logger.info("Trying to send email")
    try:
        if resultingPdfBinContents:
            body = body_success
        else:
            body = body_failure
        SendEmail(senderur[::-1], senderpr[::-1], toEmailCSV, ccEmailCSV, bccEmailCSV, subject, body, resultingPdfBinContents)
    except Exception as ex:
        current_app.logger.error("Error while sending email: {}".format(ex))
    else:
        current_app.logger.info("Mail sent to toEmailCSV:{} ccEmailCSV:{} at {}".format(toEmailCSV, ccEmailCSV, localNow()))
    response = "Report generated successfully and sent through email"
    return make_response(response)

def SendEmail(senderu, senderp, toEmailCSV, ccEmailCSV, bccEmailCSV, subject, body, attachmentAsBinContent):
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.MIMEBase import MIMEBase
    from email import encoders

    COMMA = ","
    recepients = toEmailCSV + COMMA + ccEmailCSV + COMMA+ bccEmailCSV
    recepients = recepients.split(COMMA)
    recepients = [r for r in recepients if r.strip()]

    msg = MIMEMultipart()

    msg['From'] =  senderu
    msg['To'] = toEmailCSV
    msg['Cc'] = ccEmailCSV
    msg['Subject'] = subject


    msg.attach(MIMEText(body, 'html'))

    if attachmentAsBinContent:
        filename = "Report.pdf"

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachmentAsBinContent)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(senderu, senderp)
    text = msg.as_string()
    server.sendmail(senderu, recepients, text)
    server.quit()
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


    resultingPdfBinContents = urltopdf(weburl)
    response = make_response(resultingPdfBinContents)
    response.headers['Content-Disposition'] = "attachment; filename={}.pdf".format(title)
    response.mimetype = 'application/pdf'
    return response

if __name__ == "__main__":
    weburl = u"http://testclimaterealty.appspot.com/report?floor_height_above_ground_meters=0&enduserEmail=karl%40climaterisk.com.au&enduserPhoneNumber=9999999999&wave_setup_percent=15&sea_level_model=Haigh+et+al+2014&debugMode=on&is_exposed_to_coastal=yes&replacement_cost=100000000&name=Karl+Mallon&value_of_house_and_land=100000000&lower_floor_construction_detail=Concrete&estimated_damage_from_flooding_event_percent=50&debug_this_flow=False&address=1+Riverview+Parade%2C+North+Manly+NSW+2100%2C+Australia"
    urltopdf(weburl, max_reattempts=10, threshold_filesize_kb=200, delayms=30*1000)
