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
#
#
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import shutil
import xml.etree.ElementTree as ET

URL = "http://donnees.ville.montreal.qc.ca/dataset/a5c1f0b9-261f-4247-99d8-f28da5000688/resource/92719d9b-8bf2-4dfd-b8e0-1021ffcaee2f/download/inspection-aliments-contrevenants.xml"
req = Request(URL)


app = Flask(__name__)


def get_xml_root(path):
    tree = ET.parse(path)
    return tree.getroot()


def get_site_data():
    #print(URL)
    try:
        response = urlopen(req)
        #data_xml = response.read()
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        print("c bonnnnnn")
        #data_xml = response.read()
        with open('feed.xml', 'wb') as outfile:
            shutil.copyfileobj(response,outfile)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
def page_acceuil():
    get_site_data()
    root = get_xml_root("test.xml")
    db = get_db()

    print(root.tag)
    for child in root:
        print(child.tag, child.attrib)
    #db.add_contrevenant("a12","c12","e12","adr12","v12","desc12","datei12","datej12",15002)

    list_complete = db.get_liste_complete()
    #for row in list_complete:
        #print(row)

    return render_template('accueil.html')
