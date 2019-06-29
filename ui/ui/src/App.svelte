<script>
    let username = 'username';
    let password = 'password';
    let root = 'http://localhost:8080';
    function post(url, data, completed){
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
    function handleClick(){
        post('/register', {'name': username, 'pwd': password}, function (ajax){
                if ((ajax.status == 200) || (ajax.status == 400)){
                    post('/login', {'name': username, 'pwd': password}, function (ajax){
                            alert(ajax.responseText);
                    });
            }
        });
    }
</script>

<h1>OpenJudge</h1>
<div>
    <div><label>Username</label><input bind:value={username}></div>
    <div><label>Password</label><input bind:value={password}></div>
    <div><button on:click={handleClick}>Login/Register</button></div>
</div>
