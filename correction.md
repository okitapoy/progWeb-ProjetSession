# A1
L'application va télécharger les données de la ville lorsque la page d'acceuil sera visité pour
la première fois après avoir parti le programme. Ensuite, une mise a jours sera faite chaque jours
à minuit. Si le programme est arreté, il faudra supprimmer le fichier "db/database.db" et le recréer
pour éviter de dupliquer la base de données, si on repart l'application.

# A2
Sur la page d'acceuil, on peut faire une recherche dans la base données en entrant des critères de
recherches comme indiqué sur la page.

# A3
un BackgroundScheduler est en place pour mettre á jours la base de données à minuit.

# A4
Un service REST est en place pour recuperer une liste de contreventions commmisent entre deux dates.
Une pagge d'erreur (code: 404) est affichée si une date n'est pas valide.

ex de requête : api/contrevenants?du=2018-05-08&au=2020-05-15

# A5
Sur la page d'acceuil du site, il y a aussi un petit formulaire pour faire une recherche avec deux dates.
La page est modifiée avec le resultat de la recherche.
Une pagge d'erreur (code: 404) est affichée si une date n'est pas valide.

# A6
Lorsque le resultat du point A5 est affiché, un bouton est aussi affiché et on peut afficher une liste de
tous les établissement de la base de données. On peut selectionner un établissement pour afficher toutes
les contrenventions de l'établissement.

# C1
Un service REST est en place  la liste des établissements ayant commis une ou
plusieurs infractions avec leurs nombres d'infractions. le format est en JSON

ex : /api/contrevenants/liste_etablissement/JSON

# C2
Un service REST est en place  la liste des établissements ayant commis une ou
plusieurs infractions avec leurs nombres d'infractions. le format est en XML.

ex : /api/contrevenants/liste_etablissement/XML

# C3
Un service REST est en place  la liste des établissements ayant commis une ou
plusieurs infractions avec leurs nombres d'infractions. le format est en CSV.

ex : /api/contrevenants/liste_etablissement/CSV


# F1
L'application est hebergé sur heroku

URL : https://projet-session-inf5190.herokuapp.com
