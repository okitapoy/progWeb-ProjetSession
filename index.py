#/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from flask import render_template
from flask import make_response
from flask import g
from flask import request
from flask import redirect
from flask import Response
from flask import url_for
from .database import Database
#import uuid
import datetime

app = Flask(__name__)


@app.route('/')
def page_acceuil():
    return render_template('accueil.html')
