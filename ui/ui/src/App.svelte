<script>
    import Cookies from 'js-cookie';
    import Contests from './Contests.svelte';
    import { fade } from 'svelte/transition';

    let username = 'username';
    let password = 'password';
    let userid = Cookies.get('userid');
    let userinfo = '';
    let root = 'http://localhost:8080';
    $: is_logged_in = typeof userid === 'undefined';

    try{
        let userinfo = JSON.parse(Cookies.get('userinfo'));
    }
    catch (e){
        if (e.name !== 'SyntaxError'){
            throw e;
        }
    }

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
                        var data = JSON.parse(ajax.responseText);
                        Cookies.set('userid', data['userid']);
                        Cookies.set('userinfo', data);
                        userid = data['userid'];
                        userinfo = data;
                    });
            }
        });
    }
</script>

<h1>OpenJudge</h1>
{#if is_logged_in }
    <div>
        <div><label>Username</label><input bind:value={username}></div>
        <div><label>Password</label><input bind:value={password}></div>
        <div><button on:click={handleClick}>Login/Register</button></div>
    </div>
{:else}
    <Contests/>
{/if}
