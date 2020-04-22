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
  //var block_resultat = document.getElementById("block_resultat");

  //var form_date = document.getElementById("form_date").elements[0].value;

  du = document.getElementById("form_date").elements[0].value;
  au = document.getElementById("form_date").elements[1].value;

  var url_route = "/api/contrevenants?du="+du+"&au="+au;

  //console.log(url_route);


  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

     var donnee_json = JSON.parse(this.responseText);

     //console.log(donnee_json.length);

     if(donnee_json.length > 0 ){
       creerHeaderTable();
       creerTable(donnee_json);
     }else{
       aucune_donnee_trouve(du,au);
     }
/*
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
          tablo.push(donnee_json[i].etablissement);
          console.log(donnee_json[i].etablissement);
          console.log(nombre);
         }
         nombre = 1;


       }

     } */

    }
  };
  xhttp.open("GET", url_route, true);
  xhttp.send();


/*
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

  var th = document.createElement("TH");
  var text = document.createTextNode("nombre d'infraction");
  th.appendChild(text);
  document.getElementById("myTr").appendChild(th);
*/


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
       console.log(donnee_json[i].etablissement);
       console.log(nombre);
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
  var text = document.createTextNode("Aucune infraction trouvée commise entre le " + au + "et le" + du);
  p.appendChild(text);
  document.getElementById("block_resultat").appendChild(p);

}
