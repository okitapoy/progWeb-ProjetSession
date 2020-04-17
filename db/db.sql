create table contrevenants (
  id integer primary key,
  proprietaire varchar,
  categorie varchar,
  etablissement varchar,
  adresse varchar,
  ville varchar,
  description text,
  date_infraction varchar,
  date_jugement varchar,
  montant integer
);



insert into contrevenants (proprietaire,categorie,etablissement,adresse,ville,description,date_infraction,date_jugement,montant)
  values("a1","c1","e1","adr1","v1","desc1","datei1","datej1",1500);
