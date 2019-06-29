<style>
    #content{
        display: grid;
        grid-template-areas:
            "q s s p p";
    }
    #questions{
        grid-area: q;}
    #statement{
        grid-area: s;}
    #program{
        grid-area: p;}
    #questions ul {
        list-style-type: none;
    }
    #statement textarea{
        width: 100%;
    }
</style>
<div id='content'>
    <div id='questions'>
        <ul>
            <li>Question 1</li>
            <li>Question 2</li>
            <li>Question 3</li>
        </ul>
    </div>
    <div id='program'>
        <textarea></textarea>
    </div>
    <div id='statement'>
        <p>What is the question?</p>
    </div>
</div>
