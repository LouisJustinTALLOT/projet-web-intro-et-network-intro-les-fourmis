// le joueur correspondant
var player_id = 0

window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );

    document.onkeydown = function(e){
        switch(e.keyCode){
            case 37:
                socket.emit("move", {ident: player_id, dx:-1, dy:0});
                break;
            case 38:
                socket.emit("move", {ident: player_id, dx:0, dy:-1});
                break;
            case 39:
                socket.emit("move", {ident: player_id, dx:1, dy:0});
                break;
            case 40:
                socket.emit("move", {ident: player_id, dx:0, dy:1});
                break;
            case 32:
                // barre espace
                socket.emit("attack", {ident:player_id})
                break;
        }


    };
    
    var btn_n = document.getElementById("go_n");
    btn_n.onclick = function(e) {
        // console.log("Clicked on button north");
        socket.emit("move", {dx:0, dy:-1});
    };

    var btn_s = document.getElementById("go_s");
    btn_s.onclick = function(e) {
        // console.log("Clicked on button south");
        socket.emit("move", {dx:0, dy:1});
    };

    var btn_w = document.getElementById("go_w");
    btn_w.onclick = function(e) {
        // console.log("Clicked on button w");
        socket.emit("move", {dx:-1, dy:0});
    };

    var btn_e = document.getElementById("go_e");
    btn_e.onclick = function(e) {
        // console.log("Clicked on button e");
        socket.emit("move", {dx:1, dy:0});
    };


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
            }
            else if(data[i].descr === "earn") {
                console.log(data[i].ident + " a gagné " + data[i].val)
                break;
            }
            else if(data[i].descr === "fight") {
                console.log("Le joueur" + data[i].ident + " a attaqué le monstre " + data[i].target + " et il est mort ?" + data[i].isdead)
                break;
            }
            else if (data[i].descr === "dead") {
                console.log("Le monstre " + data[i].attacker + " a tué le joueur " + data[i].ident);
                var cell_id = "vie" + data[i].ident;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "Dead";
                break;
            }
            else if (data[i].descr === "damaged") {
                console.log("Le monstre " + data[i].attacker + " a fait des dommages au joueur " + data[i].ident + " (" + data[i].amount + " pts de vie)");
                var cell_id = "vie" + data[i].ident;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = "life : " + data[i].life;
                break;
            }
        }
    });

});