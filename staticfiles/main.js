$('document').ready(function(){
    function gettoken(){
        return Cookies.get('token');
    };
    function settoken(token){
        if(token === null){
            Cookies.remove('token');
        }
        else {
            Cookies.set('token', token);
        }
    };
    function hitApi(endpoint, json, success_fn, auth=true){
        if(auth){
            json["token"] = gettoken();
        };
        console.log("Hitting " + endpoint + " " + JSON.stringify(json));
        $.ajax({url: endpoint, type: 'post',
                contentType: 'application/json',
                data: JSON.stringify(json),
                success: success_fn});
    } // hit API
    // ----------------------------------
    $("#login_form").hide();
    if(gettoken() !== undefined){
        $("#login").hide();
        $("#logout").show();
    }
    else{
        $("#login").show();
        $("#logout").hide();
    }
    // ------------------------what do do on login click
    $("#login").click(function (){
        // $("#login_uname").show();
        // $("#login_pwd").show();
        $("#login_form").show();
        $("#login").hide();
        $("#signup_button").hide();
        $("#login_button").show();
    });  // on  login click
    $("#login_button").click(function (){
        var uname = $("#login_uname").val();
        var pwd = $("#login_pwd").val();
        hitApi('/login', {"uname": uname, "pwd": pwd},
               function (d, x, s){
                   settoken(d['token']);
                   $("#login_form").hide();
                   $("#login").hide();
                   $("#logout").show();
               });
    });
    // -----------------signup
    $("#signup").click(function (){
        // $("#login_uname").show();
        // $("#login_pwd").show();
        $("#login_form").show();
        $("#login_button").hide();
        $("#signup_button").show();
    });  // on  login click
    $("#signup_button").click(function (){
        var uname = $("#login_uname").val();
        var pwd = $("#login_pwd").val();
        hitApi('/signup', {"uname": uname, "pwd": pwd},
               function (d, x, s){
                   console.log(d);
                   $("#login_form").hide();
               });
    });
    // -----------------logout click
    $("#logout").click(function (){
        hitApi("/logout", {"token": gettoken()}, function (){});
        settoken(null);
        $("#login").show();
        $("#logout").hide();
    });
    // ------------------- what happens on question click
    $(".question_listing").click(function (){
        var qid = this.attributes['qid'].value;
        hitApi("/question", {"qid": qid}, function (d, x, s){
            var converter = new showdown.Converter(),
                text      = d['statement'],
                html      = converter.makeHtml(text);
            $("#content_question_space").html(html);
        });
    });
}); // MAIN on ready
