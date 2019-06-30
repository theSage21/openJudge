<script>
    import { post } from './common.js';
    let contests = [];
    post('/contestList', {}, function (ajax){
        contests = JSON.parse(ajax.responseText);
    });
    function new_contest(){
        post('/newContest', {}, function (ajax){
        }
    }
</script>
<style>
</style>
<div id='content'>
    <div class='contest' on:click={new_contest}>New Contest</div>
    {#each contests as contest}
    <div class='contest'><b>{contest.title}</b><p>{contest.description}</p></div>
    {/each}
</div>
