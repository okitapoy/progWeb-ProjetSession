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
from flask import send_from_directory, send_file
from .database import Database
#import uuid
import datetime
#
#
import csv
import urllib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import shutil
import xml.etree.ElementTree as ET
#
#
from apscheduler.schedulers.background import BackgroundScheduler
from dicttoxml import dicttoxml
import datetime

#import operator

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




def mise_a_jour_bd():
    get_site_data()
    donnee_a_jours = True
    print("Mise à jours des donnees effectuée")


scheduler = BackgroundScheduler()
scheduler.add_job(mise_a_jour_bd,'interval',hours=24,start_date='2020-04-20 00:00:00')
scheduler.start()


def get_xml_root(path):
    return ET.fromstring(path)


def get_site_data():
    try:
        response = urllib.request.urlopen(URL)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        data_xml = str(response.read().decode('latin-1'))
        root = get_xml_root(data_xml)
        mettre_a_jours_bd(root,get_db())



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



def get_liste_complete_triee():
    db = get_db()
    liste_complete = db.get_liste_complete()
    liste_dict = []
    liste_etablissement = []

    for row in liste_complete:
        if(row['etablissement'] not in liste_etablissement):
            nombre = len(db.chercher_etablissement(row['etablissement']))
            liste_dict.append(dict({"etablissement": row['etablissement'], "contreventions": nombre}))

        liste_etablissement.append(row['etablissement'])

    liste_trie = sorted(liste_dict, key = lambda i : i['contreventions'], reverse=True)
    return liste_trie

def verifier_bd():
    global donnee_a_jours
    if donnee_a_jours is False:
        get_site_data();
        donnee_a_jours = True



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
    #if donnee_a_jours is False:
    #    get_site_data();
    #    donnee_a_jours = True

    #verifier_bd()
    db = get_db()

    liste_complete = db.get_liste_complete()

    return render_template('accueil.html',liste_contrevenants=liste_complete)


@app.route('/recherche')
def page_resulat_recherche():
    db = get_db()
    etablissement = request.args['etablissement'].strip()
    proprietaire = request.args['proprietaire'].strip()
    rue = request.args['rue'].strip()

    if(rue == ""):
        resulat = db.chercher_attribut_sans_rue(etablissement,proprietaire)
    else:
        resulat = db.chercher_attributs_Avec_rue(etablissement,proprietaire,rue)

    return render_template('rechercheRes.html',liste_contrevenants=resulat)



@app.route('/doc')
def documentation():
    return render_template('doc.html')


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
            message = "Une erreur est survenue. Vous devez mettre des dates valident (format annee-mois-jours : 2020-02-25)"
            print("DATE INVALIDE!!!!!")
            return render_template("404.html",msg=message),404

    elif len(request.args) is 0:
        #print("ZEROOOOOO   argument passe liste complete")

        infractions_liste_complete = jsonify(db.get_liste_complete())

        return(infractions_liste_complete)

    #elif 'contrevenant' in request.args and len(request.args) is 1:
        #print("argument un contrevenant!!!!!")

        #etablissement = str(request.args['contrevenant'])
        #liste_infractions_etablissement  = jsonify(db.chercher_etablissement(etablissement))

        #return (liste_infractions_etablissement)


    else:
        message = "Les parametres d'URL que vous avez entrez ne sont pas valident."
        print("argument non pris en charge!!!!!")
        return render_template("404.html",msg=message),404




@app.route('/api/contrevenants/contrevenant/<etablissement>',methods=['GET'])
def api_etblissement(etablissement):
    db = get_db()
    #liste_infractions_etablissement  = jsonify(db.chercher_etablissement(etablissement))

    liste_infractions_etablissement = db.chercher_etablissement(etablissement)
    if(len(liste_infractions_etablissement) > 0):
        #print(liste_infractions_etablissement[0])
        return (jsonify(liste_infractions_etablissement))
    else:
        print("pas trouveeeeee")
        return render_template("404.html"),404



@app.route('/api/contrevenants/liste/non/non',methods=['GET'])
def api_liste_etablissement(format):
    param = ['CSV','JSON','XML']
    db = get_db()
    liste_complete = db.get_liste_complete()

    liste_dict = []
    liste_etablissement = []

    if format.upper() in param:
        for row in liste_complete:
            if(row['etablissement'] not in liste_etablissement):
                nombre = len(db.chercher_etablissement(row['etablissement']))
                liste_dict.append(dict({"etablissement": row['etablissement'], "contreventions": nombre}))

            liste_etablissement.append(row['etablissement'])

        liste_trie = sorted(liste_dict, key = lambda i : i['contreventions'], reverse=True)

        if format.upper() is 'JSON':
            print('json')
            return(jsonify(liste_trie))
        elif format.upper() is 'XML':
            print("XML")
            return(dicttoxml(liste_trie))
        else:
            print(format.upper())
            return("csv incomplet")


    else:
        return render_template("404.html"),404




    #print(liste_trie)

    #return(jsonify(liste_trie))



@app.route('/api/contrevenants/liste_etablissement/JSON',methods=['GET'])
def api_liste_etablissement_JSON():
    #db = get_db()

    liste_trie = get_liste_complete_triee()
    return(jsonify(liste_trie))


@app.route('/api/contrevenants/liste_etablissement/XML',methods=['GET'])
def api_liste_etablissement_XML():
    #db = get_db()

    liste_trie = get_liste_complete_triee()
    return(dicttoxml(liste_trie))


@app.route('/api/contrevenants/liste_etablissement/CSV',methods=['GET'])
def api_liste_etablissement_CSV():
    liste_trie = get_liste_complete_triee()
    csv_columns = ['etablissement','contreventions']
    csv_file = "fichier.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in liste_trie:
                writer.writerow(data)

        with open('fichier.csv','r') as file:
            data = file.read()
        return (data)
    except IOError:
        print("I/O error")
        return render_template("404.html"),500
