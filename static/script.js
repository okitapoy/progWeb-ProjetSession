console.log("CECIIIIIII ESTTT UN TEEESTTT");


//document.getElementById("form_rehcherche").onsubmit = function(){recherche_date()};
function eraseContainer(element){
     var myNode = document.getElementById(element);


     while (myNode.firstChild) {
       myNode.removeChild(myNode.firstChild);
     }

}



function recherche_date(){
console.log("ON EST DANS LA fonctions javascript");

  du = document.getElementById("form_date").elements[0].value;
  au = document.getElementById("form_date").elements[1].value;

  var url_route = "/api/contrevenants?du="+du+"&au="+au;

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

     var donnee_json = JSON.parse(this.responseText);

     //console.log(donnee_json.length);

     if(donnee_json.length > 0 ){
       chercherContreventionsCompletes();
       creerHeaderTable();
       creerTable(donnee_json);
     }else{
       chercherContreventionsCompletes();
       aucune_donnee_trouve(du,au);
     }


    }
  };
  xhttp.open("GET", url_route, true);
  xhttp.send();

  return false;
}




function creerTable(donnee_json){

  var i;
  var n;
  var nombre = 1;
  var tablo = [];

  for(i = 0; i < donnee_json.length; i++){
    //console.log(donnee_json[i].etablissement);

    for(n = 0; n < donnee_json.length; n++){
      if(donnee_json[i].etablissement == donnee_json[n].etablissement){
        nombre++;
      }

      if(!tablo.includes(donnee_json[i].etablissement)){
       ajouterALaTable(donnee_json[i].etablissement,nombre);
       tablo.push(donnee_json[i].etablissement);
       //console.log(donnee_json[i].etablissement);
       //console.log(nombre);
      }
      nombre = 1;


    }

  }

}





function creerHeaderTable(){

  eraseContainer("block_resultat");
  //document.getElementById("block_resultat").innerHTML = donnee_json[0].etablissement;
  var div = document.createElement("DIV");
  div.setAttribute("id","block_resultat");
  document.body.appendChild(div);

  var table = document.createElement("TABLE");
  table.setAttribute("id", "myTable");
  //document.body.appendChild(table);
  document.getElementById("block_resultat").appendChild(table);

  var row = document.createElement("TR");
  row.setAttribute("id", "myTr");
  document.getElementById("myTable").appendChild(row);

  var th = document.createElement("TH");
  var text = document.createTextNode("nom de l'etablissement");
  th.appendChild(text);
  document.getElementById("myTr").appendChild(th);

  var th_2 = document.createElement("TH");
  var text = document.createTextNode("nombre d'infraction");
  th_2.appendChild(text);
  document.getElementById("myTr").appendChild(th_2);

}


function ajouterALaTable(etablissement,nombre){
/*
  var row_1 = document.createElement("TR");
  row_1.setAttribute("id", "myTr");
  document.getElementById("myTable").appendChild(row_1);

  var th = document.createElement("TD");
  var text = document.createTextNode(etablissement);
  th.appendChild(text);
  document.getElementById("myTr").appendChild(th);

  var th = document.createElement("TD");
  var text = document.createTextNode(nombre);
  th.appendChild(text);
  document.getElementById("myTr").appendChild(th);   */


  //document.getElementById("myTr").appendChild(th);
  //document.getElementById("myTr").appendChild(th);
  //document.getElementById("myTable").appendChild(row);

  //var br = document.createElement("BR");
  //document.getElementById("myTr").appendChild(br);

  var table = document.getElementById("myTable");
  var row = table.insertRow(1);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  cell1.innerHTML = etablissement;
  cell2.innerHTML = nombre;


}



function aucune_donnee_trouve(du,au){

  eraseContainer("block_resultat");
  //document.getElementById("block_resultat").innerHTML = donnee_json[0].etablissement;
  var div = document.createElement("DIV");
  div.setAttribute("id","block_resultat");
  document.body.appendChild(div);


  var p = document.createElement("P");
  var text = document.createTextNode("Aucune infraction trouvée commise entre le " + au + " et le " + du);
  p.appendChild(text);
  document.getElementById("block_resultat").appendChild(p);

}



function menuDeroulant(donnee_json){

  //console.log(donnee_json.length);

  eraseContainer("div_recherche_deroulant");

  var p = document.createElement("P");
  var text = document.createTextNode("Passez la sourris sur le boutton ci-desssous et choisissez un etablissement parmi la liste deroulante pour afficher les infractions de l'etablissement.");
  p.appendChild(text);
  document.getElementById("div_recherche_deroulant").appendChild(p);

  creerBouttonDeroulant(donnee_json);//------

}


function creerBouttonDeroulant(donnee_json){

  var div = document.createElement("DIV");
  div.setAttribute("id","menu_deroulant");
  div.setAttribute("class","dropdown");//----css
  //document.body.appendChild(div);

  document.getElementById("div_recherche_deroulant").appendChild(div);

  var button = document.createElement("BUTTON");
  //button.setAttribute("onclick","derouler()");
  button.setAttribute("class","dropbtn");
  button.setAttribute("id","buttonDropdown");

  document.getElementById("menu_deroulant").appendChild(button);

  var p = document.createElement("P");
  var text = document.createTextNode("Choisir un etablissement");
  p.appendChild(text);
  document.getElementById("buttonDropdown").appendChild(p);

  ajouterDonneeAuMenu(donnee_json)

}


function ajouterDonneeAuMenu(donnee_json){

  var div = document.createElement("DIV");
  div.setAttribute("id","myDropdown");
  div.setAttribute("class","dropdown-content");//----css

  document.getElementById("menu_deroulant").appendChild(div);

  var contenu = document.createElement("A");
  contenu.setAttribute("id","contenu");
  contenu.setAttribute("href","#");//----css

  document.getElementById("myDropdown").appendChild(contenu);

  var p = document.createElement("P");
  var text = document.createTextNode("link 1");
  p.appendChild(text);
  document.getElementById("contenu").appendChild(p);



  var tablo = [];
  var i = 0;
  var n = 0;

  for(i = 0; i < donnee_json.length; i++){
    etablissement = donnee_json[i].etablissement;


    if(!tablo.includes(etablissement)){

      var contenu = document.createElement("A");
      contenu.setAttribute("id",etablissement);
      contenu.setAttribute("href","#");//----css
      contenu.setAttribute("onclick","voirEtablissement(this.id)");

      document.getElementById("myDropdown").appendChild(contenu);

      var p = document.createElement("P");
      var text = document.createTextNode(etablissement);
      p.appendChild(text);
      document.getElementById(etablissement).appendChild(p);

     tablo.push(etablissement);

    }

  }

}


function affichierUnContrevenant(donnee_json){


    eraseContainer("block_resultat");
    //document.getElementById("block_resultat").innerHTML = donnee_json[0].etablissement;
    var div = document.createElement("DIV");
    div.setAttribute("id","block_resultat");
    document.body.appendChild(div);

    var table = document.createElement("TABLE");
    table.setAttribute("id", "myTable");
    //document.body.appendChild(table);
    document.getElementById("block_resultat").appendChild(table);

    table = document.getElementById("myTable");

    var header = table.createTHead();

    var row = header.insertRow(0)

    var cell0 = row.insertCell(0);
    var cell1 = row.insertCell(1);
    var cell2 = row.insertCell(2);
    var cell3 = row.insertCell(3);
    var cell4 = row.insertCell(4);
    var cell5 = row.insertCell(5);
    var cell6 = row.insertCell(6);
    var cell7 = row.insertCell(7);
    var cell8 = row.insertCell(8);

    cell0.innerHTML = "Propriétaire";
    cell1.innerHTML = "Catégorie";
    cell2.innerHTML = "Etablissement";
    cell3.innerHTML = "Adresse";
    cell4.innerHTML = "Ville";
    cell5.innerHTML = "Date de l'infraction";
    cell6.innerHTML = "Date du jugement";
    cell7.innerHTML = "Montant de l'amende";
    cell8.innerHTML = "Description de l'infraction"

    insererDonneeUnContrevenant(donnee_json);
}


function insererDonneeUnContrevenant(donnee_json){

  var i = 0;
  var table = document.getElementById("myTable");
  var ligne = 1;

  for(i = 0; i < donnee_json.length; i++){


    var row = table.insertRow(ligne);
    var cell0 = row.insertCell(0);
    var cell1 = row.insertCell(1);
    var cell2 = row.insertCell(2);
    var cell3 = row.insertCell(3);
    var cell4 = row.insertCell(4);
    var cell5 = row.insertCell(5);
    var cell6 = row.insertCell(6);
    var cell7 = row.insertCell(7);
    var cell8 = row.insertCell(8);

    cell0.innerHTML = donnee_json[i].proprietaire;
    cell1.innerHTML = donnee_json[i].categorie;
    cell2.innerHTML = donnee_json[i].etablissement;
    cell3.innerHTML = donnee_json[i].adresse;
    cell4.innerHTML = donnee_json[i].ville;
    cell5.innerHTML = donnee_json[i].date_infraction;
    cell6.innerHTML = donnee_json[i].date_jugement;
    cell7.innerHTML = donnee_json[i].montant;
    cell8.innerHTML = donnee_json[i].description;

    ligne++;


  }

}






function voirEtablissement(etablissement){
  console.log("on est  dans la fonction deroulller ");
  console.log(etablissement);

  var url_route = "/api/contrevenants?contrevenant="+etablissement;


  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

    var donnee_json = JSON.parse(this.responseText);

    console.log(donnee_json.length);

    affichierUnContrevenant(donnee_json);


    }

  };
  xhttp.open("GET", url_route, true);
  xhttp.send();

  return false;

}





function chercherContreventionsCompletes(){

    //du = document.getElementById("form_date").elements[0].value;
    //au = document.getElementById("form_date").elements[1].value;

    var url_route = "/api/contrevenants";

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {

       var donnee_json = JSON.parse(this.responseText);

       menuDeroulant(donnee_json);



      }

    };
    xhttp.open("GET", url_route, true);
    xhttp.send();

    return false;

}
