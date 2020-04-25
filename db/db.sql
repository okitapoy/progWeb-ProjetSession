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
  montant integer,
  date_iso_infraction text,
  date_iso_jugement text
);
