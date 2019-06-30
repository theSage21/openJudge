<script>
    import Cookies from 'js-cookie';
    import { post } from './common.js';
    import Contests from './Contests.svelte';
    import { fade } from 'svelte/transition';

    let username = 'username';
    let password = 'password';
    let userid = '';
    let userinfo = '';
    $: is_logged_in = userid !== '';

    try{
        let userinfo = JSON.parse(Cookies.get('userinfo'));
    }
    catch (e){
        if (e.name !== 'SyntaxError'){
            throw e;
        }
    }

    post('/me', {}, function (ajax){
        if (ajax.status == 200){
            var data = JSON.parse(ajax.responseText);
            userid = data['userid'];
            userinfo = data;
        }
    });

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

<nav><b>OpenJudge</b>|
    {#if is_logged_in }{userinfo.name} <a href='/logout'>Logout</a>{/if}</nav>
<hr>
{#if !is_logged_in }
    <div>
        <div><label>Username</label><input bind:value={username}></div>
        <div><label>Password</label><input bind:value={password}></div>
        <div><button on:click={handleClick}>Login/Register</button></div>
    </div>
{:else}
    <Contests/>
{/if}
