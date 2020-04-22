import sqlite3
import datetime

class Database:

    def __init__(self):
        self.connection = None


    def get_connection(self):
        #self.connection = sqlite3.connect('db/database.db')
        self.connection = sqlite3.connect('db/database.db')
        self.connection.row_factory = sqlite3.Row
        return self.connection


    def disconnect(self):
        if self.connection is not None:
            self.connection.close()


    def get_liste_complete(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from contrevenants")
        contrevenants = [dict(row) for row in cursor.fetchall()]
        return contrevenants


    def add_contrevenant(self,proprietaire,categorie,etablissement,adresse,ville,description,date_infraction,date_jugement,montant,iso_infraction,iso_jugement):
        connection = self.get_connection()
        connection.execute(("insert into contrevenants(proprietaire,categorie,etablissement,adresse,ville,description,date_infraction,date_jugement,montant,date_iso_infraction,date_iso_jugement)"
                            "values(?,?,?,?,?,?,?,?,?,?,?)"),(proprietaire,categorie,etablissement,adresse,ville,description,date_infraction,date_jugement,montant,iso_infraction,iso_jugement))
        connection.commit()


    def chercher_etablissement(self,etablissement):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from contrevenants where etablissement = ?",(etablissement,))
        res_nom = [dict(row) for row in cursor.fetchall()]
        return res_nom


    def chercher_propritaire(self,proprietaire):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from contrevenants where proprietaire = ?",(proprietaire,))
        res_proprio = [dict(row) for row in cursor.fetchall()]
        return res_proprio


    def chercher_rue(self,rue):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from contrevenants where adresse like ?", ('%'+expression+'%',))
        res_rue = [dict(row) for row in cursor.fetchall()]
        return res_rue


    def chercher_attributs_Avec_rue(self,etablissement,proprietaire,rue):
        cursor = self.get_connection().cursor()
        #cursor.execute("select * from contrevenants where etablissement = ? or proprietaire = ? or adresse like ?", (etablissement,proprietaire,'%'+rue+'%',))
        cursor.execute("select * from contrevenants where adresse like ? or etablissement = ? collate nocase or proprietaire = ? collate nocase", ('%'+rue+'%',etablissement,proprietaire,))
        res_rue = [dict(row) for row in cursor.fetchall()]
        return res_rue




    def chercher_attribut_sans_rue(self,etablissement,proprietaire):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from contrevenants where etablissement = ? collate nocase or proprietaire = ? collate nocase", (etablissement,proprietaire,))
        res_rue = [dict(row) for row in cursor.fetchall()]
        return res_rue



    def infraction_entre_date(self,depart,fin):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from contrevenants where date_iso_infraction >= date(?) and date_iso_infraction <= date(?)"
                        " order by datetime(date_iso_infraction)",(depart,fin,))
        liste = [dict(row) for row in cursor.fetchall()]
        return liste
