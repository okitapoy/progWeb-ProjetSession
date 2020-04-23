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
from flask import jsonify
from .database import Database
#import uuid
import datetime
#
#
import urllib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import shutil
import xml.etree.ElementTree as ET
#
#
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

#from flask_apscheduler import APScheduler

URL = "http://donnees.ville.montreal.qc.ca/dataset/a5c1f0b9-261f-4247-99d8-f28da5000688/resource/92719d9b-8bf2-4dfd-b8e0-1021ffcaee2f/download/inspection-aliments-contrevenants.xml"
req = Request(URL)
donnee_a_jours = False

mois = {
    "janvier": "01",
    "février": "02",
    "mars": "03",
    "avril": "04",
    "mai": "05",
    "juin": "06",
    "juillet": "07",
    "août": "08",
    "septembre": "09",
    "octobre": "10",
    "novembre": "11",
    "décembre": "12"
}


app = Flask(__name__)




def fonction_test():
    n = 0
    print("threaadddddddd")
    n += 10

scheduler = BackgroundScheduler()
scheduler.add_job(fonction_test,'interval',hours=24,start_date='2020-04-20 00:00:00')
scheduler.start()


def get_xml_root(path):
    #tree = ET.fromstring(path)
    #return tree.getroot()
    return ET.fromstring(path)


def get_site_data():
    #print(URL)
    try:
        #response = urlopen(req)
        response = urllib.request.urlopen(URL)

        #response.decode('utf-8')
        #data_xml = response.read()
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        print("c bonnnnnn")
        data_xml = str(response.read().decode('latin-1'))

        #tt = str(data_xml.encode('utf-8','strict'))
        print(data_xml)

        root = get_xml_root(data_xml)

        mettre_a_jours_bd(root,get_db())



        #with open('feed.xml', 'wb') as outfile:
            #shutil.copyfileobj(response,outfile)



def mettre_a_jours_bd(root,db):
    index = 0
    for child in root:
        db.add_contrevenant(root[index][0].text,root[index][1].text,root[index][2].text,
        root[index][3].text,root[index][4].text,root[index][5].text,root[index][6].text,
        root[index][7].text,root[index][8].text,iso_convert(root[index][6].text),iso_convert(root[index][7].text))
        index += 1

def valider_date(la_date):
    valide = 1
    try:
        datetime.datetime.strptime(la_date,'%Y-%m-%d')
    except ValueError:
        valide = 0
    finally:
        return valide


def iso_convert(laDate):
    liste = laDate.split()
    trait = "-"
    return liste[2]+trait+mois[liste[1]]+trait+liste[0]
    #print(iso_date)
    #print(valider_date(iso_date))





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
    #get_site_data();
    db = get_db()

    liste_complete = db.get_liste_complete()
    #for row in list_complete:
    #    print(row)

    return render_template('accueil.html',liste_contrevenants=liste_complete)


@app.route('/recherche')
def page_resulat_recherche():
    db = get_db()
    etablissement = request.args['etablissement']
    proprietaire = request.args['proprietaire']
    rue = request.args['rue']

    if(rue == ""):
        resulat = db.chercher_attribut_sans_rue(etablissement,proprietaire)
    else:
        resulat = db.chercher_attributs_Avec_rue(etablissement,proprietaire,rue)

    return render_template('rechercheRes.html',liste_contrevenants=resulat)



@app.route('/api/contrevenants',methods=['GET'])
def api_contrevenants():

    db = get_db()

    if 'du' in request.args and "au" in request.args:
        date_depart = str(request.args['du'])
        date_fin =  str(request.args['au'])


        if(valider_date(date_depart) is 1 and valider_date(date_fin) is 1):
            liste_entre_date = db.infraction_entre_date(date_depart,date_fin)


            if(len(liste_entre_date) != 0):
                liste_entre_date_json = jsonify(liste_entre_date)
                print(liste_entre_date_json)

                #return render_template('rechercheRes.html',liste_contrevenants=liste_entre_date) #temporair -------
                return(liste_entre_date_json)
            else:
                return(jsonify(liste_entre_date))
                print("aucune infraction trouvee")
        else:
            print("DATE INVALIDE!!!!!")

    elif len(request.args) is 0:
        print("ZEROOOOOO   argument passe liste complete")
        infractions_liste_complete = jsonify(db.get_liste_complete())

        return(infractions_liste_complete)

    elif 'contrevenant' in request.args and len(request.args) is 1:
        print("argument un contrevenant!!!!!")

        etablissement = str(request.args['contrevenant'])
        liste_infractions_etablissement  = jsonify(db.chercher_etablissement(etablissement))

        return (liste_infractions_etablissement)


    else:
        print("argument non pris en charge!!!!!")


    return("fin api")
