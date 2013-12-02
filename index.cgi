#!/usr/bin/python

### Switch on the virtualenv
import os, os.path
this_dir = os.path.dirname(os.path.abspath(__file__))
virtualenv_path = os.path.join(this_dir,
                               'env')
activate_this = os.path.join(virtualenv_path, 'bin', 'activate_this.py')
assert os.path.exists(activate_this)
execfile(activate_this,
         dict(__file__=activate_this))

### code for our trivial Flask app
from flask import Flask, request
import pprint
import smtplib
import email.mime.text
app = Flask(__name__)

ME = 'app@linode.openhatch.org'
YOU = 'paulproteus@localhost'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        as_string = pprint.pprint(dict(request.form))
        msg = email.mime.text.MIMEText(as_string)
        msg['Subject'] = 'Inbound IPN POST'
        msg['From'] = ME
        msg['To'] = YOU
        s = smtplib.SMTP('localhost')
        s.sendmail(ME,
                   [YOU],
                   msg.as_string())
        s.quit()
        return "Success."
    else:
        return "You probably want to POST."


### Actually enable Flask
from wsgiref.handlers import CGIHandler

if __name__ == '__main__':
    CGIHandler().run(app)

