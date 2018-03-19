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
        Cookies.set('qid', qid);
        // clear all active classes
        $(".question_listing").each(function (){this.className = 'question_listing';});
        // set this to active
        this.className += " vertbaractive";
        // get data
        hitApi("/question", {"qid": qid}, function (d, x, s){
            var converter = new showdown.Converter(),
                text      = d['statement'],
                html      = converter.makeHtml(text);
            $("#content_question_space").html(html);
            $("#submission_form").show();
        });
    });
    // ----------------------------what to do on code submit?
    $("#submit_code").click(function (){
        var qid = Cookies.get('qid');
        var code = $("#codetext").val();
        var lang = $("#language_selection").val();
        var data = {"qid": qid, "lang": lang, "token": gettoken(),
                    "code": code};
        hitApi('/attempt', data, function (d, x, s){
            console.log(d);
        });
    });
    // ----------------------things to do always
    $.ajax({url: '/languages', type: 'get',
            success: function (d, x, s){
                var sel = $("#language_selection");
                for(var i=0; i < d['languages'].length; ++i){
                    var l = d['languages'][i];
                    var opt = $("<option val='"+l+"'>"+l+"</option>");
                    sel.append(opt);
                }
            }});
    $("#login_form").hide();
    $("#submission_form").hide();
    if(gettoken() !== undefined){
        $("#login").hide();
        $("#logout").show();
    }
    else{
        $("#login").show();
        $("#logout").hide();
    }
}); // MAIN on ready
