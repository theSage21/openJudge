    let root = 'http://localhost:8080';
    export function post(url, data, completed){
        console.log(root+url);
        var data = JSON.stringify(data);
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("POST", root+url, true);
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.withCredentials = true;
        xmlhttp.onreadystatechange = function(){
                    if (xmlhttp.readyState == 4){ completed(xmlhttp);}
        }
        xmlhttp.send(data);
    }
