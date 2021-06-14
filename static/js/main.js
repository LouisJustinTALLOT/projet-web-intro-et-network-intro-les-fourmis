// le joueur correspondant

var player_id = -1


window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );

    console.log("document login ");
    socket.emit("login", {})

})


function addInfoLine(newPlayerId) {
    var divInfos = document.getElementById("infos");

    var childInfosJoueur = divInfos.querySelector("#joueur").cloneNode(true)
    console.log(childInfosJoueur)
    var actualNumber = parseInt(newPlayerId) + 1;
    childInfosJoueur.querySelector("#ident").innerText = "Player " + actualNumber;
    console.log(childInfosJoueur)
    childInfosJoueur.querySelector("#gold0").content = "Gold : 0";
    childInfosJoueur.querySelector("#gold0").id = "gold" + newPlayerId;

    var vieJoueur = childInfosJoueur.querySelector("#vie")
    vieJoueur.querySelector("#vie0").content = "Life : 100"
    vieJoueur.querySelector("#vie0").id = "vie" + newPlayerId
    vieJoueur.querySelector("#respawn0").id = "respawn" + newPlayerId

    divInfos.appendChild(childInfosJoueur)
}

window.addEventListener("load", (event) => {

    // socket.emit("login");

    var socket = io.connect("http://" + document.domain + ":" + location.port );

    document.onkeydown = function(e){
        console.log("player_id ", player_id);
        switch(e.keyCode){
            case 37:
                e.preventDefault();
                socket.emit("move", {ident: player_id, dx:-1, dy:0});
                break;
            case 38:
                e.preventDefault();
                socket.emit("move", {ident: player_id, dx:0, dy:-1});
                break;
            case 39:
                e.preventDefault();
                socket.emit("move", {ident: player_id, dx:1, dy:0});
                break;
            case 40:
                e.preventDefault();
                socket.emit("move", {ident: player_id, dx:0, dy:1});
                break;
            case 32:
                // barre espace
                e.preventDefault();
                socket.emit("attack", {ident:player_id})
                break;
        }


    };
    
    var btn_n = document.getElementById("go_n");
    btn_n.onclick = function(e) {
        // console.log("Clicked on button north");
        socket.emit("move", {ident: player_id, dx:0, dy:-1});
    };

    var btn_s = document.getElementById("go_s");
    btn_s.onclick = function(e) {
        // console.log("Clicked on button south");
        socket.emit("move", {ident: player_id, dx:0, dy:1});
    };

    var btn_w = document.getElementById("go_w");
    btn_w.onclick = function(e) {
        // console.log("Clicked on button w");
        socket.emit("move", {ident: player_id, dx:-1, dy:0});
    };

    var btn_e = document.getElementById("go_e");
    btn_e.onclick = function(e) {
        // console.log("Clicked on button e");
        socket.emit("move", {ident: player_id, dx:1, dy:0});
    };

    var btn_sauvegarde = document.getElementById("btn_sauvegarde");
    btn_sauvegarde.onclick = function(e) {
        socket.emit("sauvegarder", {})
        var cell_id = "evenements";
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = "Sauvegarde effectuée !";
    }

    var btn_charger = document.getElementById("btn_charger");
    btn_charger.onclick = function(e) {
        socket.emit("charger", {})
    }

    socket.on("response", function(data){
        // console.log(data);
        for( var i=0; i<2; i++){
            if(data[i].descr === "displacement") {
                if (data[i].i !== "-1" && data[i].j !== "-1") {
                    // n'a pas disparu donc on s'en occupe
                    var cell_id = "cell " + data[i].i + "-" + data[i].j;
                    // console.log(cell_id);
                    var span_to_modif = document.getElementById(cell_id);
                    symbole = data[i].content;
                    span_to_modif.className = data[i].content;
                    span_to_modif.textContent = data[i].content;
                }
            }else if (data[i].descr === "new_challenger") {
                //On lui souhaite la bienvenue
                var cell_id = "evenements";
                var span_to_modif = document.getElementById(cell_id);
                var numéro = parseInt(data[i].ident)+1;
                span_to_modif.textContent = "Bienvenue Joueur n°"+ numéro;
                if (numéro > 1) {
                    btn_sauvegarde.style = "display:none";
                    btn_charger.style = "display:none";
                }

                if(data[i].ident == player_id || player_id == -1) {
                    // do nothing
                }else {
                    // on enlève les boutons de sauvegarde
                    
                    // on ajoute les lignes d'informations d'un nouveau joueur
                    addInfoLine(data[i].ident)
                    // et on le place sur le terrain
                    var cell_id = "cell " + data[i].i + "-" + data[i].j;
                    var span_to_modif = document.getElementById(cell_id);
                    symbole = data[i].content;
                    span_to_modif.className = data[i].content;
                    span_to_modif.textContent = data[i].content;
                }

            } else if (data[i].descr === "send_player_id") {
                if (player_id === -1) {
                    console.log(data[i].id)
                    player_id = parseInt(data[i].id);
                    // on ajoute une flèche pour savoir qui on est
                    var aChanger = document.getElementById("gold" + data[i].id).parentNode.querySelector("#ident");
                    aChanger.innerText = "=>" + aChanger.innerText + "<="
                }
                break;
            }
            else if(data[i].descr === "earn") {
                console.log(data[i].ident + " a gagné " + data[i].val)
                var cell_id = "gold" + data[i].ident;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "Gold : " + data[i].money;

                var cell_id = "score" + data[i].ident;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "Score : " + data[i].score;

                var cell_id = "evenements";
                var span_to_modif = document.getElementById(cell_id);
                var numéro = parseInt(data[i].ident)+1;
                span_to_modif.textContent = "Joueur "+ numéro + " devient riche !";
                break;
            }
            else if(data[i].descr === "fight") {
                console.log("Le joueur" + data[i].ident + " a attaqué le monstre " + data[i].target + " et il est mort ?" + data[i].isdead)
                var cell_id = "evenements";
                var span_to_modif = document.getElementById(cell_id);
                var numéro = parseInt(data[i].ident)+1;
                if (data[i].isdead === "True"){
                    span_to_modif.textContent = "Joueur "+ numéro + " a tué le monstre " + data[i].target;
                }
                else {
                    span_to_modif.textContent = "Joueur "+ numéro + " a attaqué le monstre " + data[i].target;
                }
                var cell_id = "score" + data[i].ident;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "Score : " + data[i].score;
                break;
            }
            else if (data[i].descr === "dead") {
                console.log(data[i].attacker + " a tué Joueur " + data[i].ident);
                var cell_id = "vie" + data[i].ident;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "Dead";

                var cell_id = "score" + data[i].ident;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "Score : " + data[i].score;

                var cell_id = "evenements";
                var span_to_modif = document.getElementById(cell_id);
                var numéro = parseInt(data[i].ident)+1;
                span_to_modif.textContent = "Le monstre " + data[i].attacker + " a tué Joueur " + numéro;


                if (data[i].ident == player_id) {
                    var cell_id = "respawn"+ data[i].ident;
                    var btn_respawn = document.getElementById(cell_id);
                    btn_respawn.onclick = function() {
                    console.log("respawning ... ");
                    socket.emit("respawn", {ident: player_id});
                    var cell_id = "evenements";
                    var span_to_modif = document.getElementById(cell_id);
                    var numéro = parseInt(data[i].ident)+1;
                    span_to_modif.textContent = "Bon retour parmi nous Joueur " + numéro;
                    };
                    btn_respawn.style= "display:inline";
                }
                break;
            }
            else if (data[i].descr === "damaged") {
                console.log("Le monstre " + data[i].attacker + " a fait des dommages au joueur " + data[i].ident + " (" + data[i].amount + " pts de vie)");
                var cell_id = "vie" + data[i].ident;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "Life : " + data[i].life;
                break;
            }
            else if (data[i].descr === "respawn") {
                console.log("Le joueur "+ data[i].ident + " respawn");
                var cell_id = "respawn" + data[i].ident;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.style= "display:none";

                // on refait apparaître le joueur
                var cell_id = "cell " + data[i].i + "-" + data[i].j;
                var span_to_modif = document.getElementById(cell_id);
                symbole = data[i].content;
                span_to_modif.className = data[i].content;
                span_to_modif.textContent = data[i].content;

                // on affiche ses nouveaux PV
                var cell_id = "vie"+ data[i].ident;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "Life : " + data[i].life ;

                break;
            }
            else if (data[i].descr === "next_level") {
                console.log("Going to the next level...")
                var cell_id = "currrent_level";
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "Niveau " + data[i].no_new_level ;

                var cell_id = "score" + data[i].ident;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "Score : " + data[i].score;

                var cell_id = "evenements";
                var span_to_modif = document.getElementById(cell_id);
                var numéro = parseInt(data[i].ident)+1;
                span_to_modif.textContent = "Bienvenue au niveau " + data[i].no_new_level;
                socket.emit("next_level_data_please", {});
                break;
            }

            else if (data[i].descr === "next_level_data") {
                for (let y=0; y< data[i].max_y; y++) {
                    for (let x=0; x < data[i].max_x; x++) {
                        var cell_id = "cell " + String(y) + "-" + String(x);

                        var span_to_modif = document.getElementById(cell_id);
                        symbole = data[i][String(y)][x];
                        span_to_modif.className = symbole;
                        span_to_modif.textContent = symbole;
                    }
                }

            }
            else if (data[i].descr === "update_stats") {
                var cell_id = "evenements";
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "Sauvegarde restorée !";

                var cell_id = "currrent_level";
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "Niveau " + data[i].level;
                console.log("ici")

                for (let j=0; j<data[i].nb_joueurs; i++) {
                    console.log("joueur ",j, " restauré");
                    var cell_id = "score" + String(j);
                    var span_to_modif = document.getElementById(cell_id);
                    span_to_modif.textContent = data[i]["score"+String(j)];


                    var cell_id = "respawn" + String(j);
                    var span_to_modif = document.getElementById(cell_id);
                    if (data[i]["life"+String(j)] === "Dead") {
                        span_to_modif.style= "display:inline";
                    } else {
                        span_to_modif.style= "display:none";
                    }
                    var cell_id = "vie" +  String(j);
                    var span_to_modif = document.getElementById(cell_id);
                    span_to_modif.textContent = data[i]["life"+String(j)];

                    var cell_id = "gold" + String(j);
                    var span_to_modif = document.getElementById(cell_id);
                    span_to_modif.textContent = data[i]["gold"+String(j)];

                }
            }
        }
    });

});