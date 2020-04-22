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

  console.log(url_route);


  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     //document.getElementById("demo").innerHTML = this.responseText;
     var donnee_json = JSON.parse(this.responseText);

     document.getElementById("demo").innerHTML = donnee_json[0].etablissement;
     console.log(donnee_json.length);

     

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

     }

    }
  };
  xhttp.open("GET", url_route, true);
  xhttp.send();

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





  return false;
}
