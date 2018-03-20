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
    function update_score(){
        $("score_display").html("Score: -");
        hitApi("/score", {}, function (d, x, s){
            $("#score_display").html("Score: "+d['score']);
        }); // --- score obtained
    }; // ---- update score
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
                   update_score();
               });
    });
    // -----------------signup
    $("#signup").click(function (){
        // $("#login_uname").show();
        // $("#login_pwd").show();
        $("score_display").html("Score: -");
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
        update_score();
    });
    // ------------------- what happens on question click
    $(".question_listing").click(function (){
        var qid = this.attributes['qid'].value;
        Cookies.set('qid', qid);
        // clear all active classes
        $(".question_listing").each(function (){this.className = 'question_listing';});
        // set this to active
        this.className += " vertbaractive";
        $("#check_status").hide();
        $("#codetext").css("background-color", "lightgray");
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
            var attid = d['attid'];
            $("#check_status").html("Checking");
            $("#check_status").show();
            hitApi('/wait/for/verdict', {"attid": attid}, function (d,x,s){
                if(d['status']){
                    $("#check_status").html("Correct");
                    $("#codetext").css("background-color", "lightgreen");
                }else{
                    $("#check_status").html("Incorrect");
                    $("#codetext").css("background-color", "pink");
                }

                update_score();
            }); // -----wait for verdict to be made
        }); // ---- submit code
    });
    // ---------------------------what to do when LB is clicked
    $("#leaderboard").click(function (){
        $("#content_question_space").html('');
        $("#submission_form").hide();
        // -----------get data
        var canvas = $("<canvas id='myChart' width='400' height='200'></canvas>");
        $("#content_question_space").append(canvas);
        $.ajax({url: '/leader', type: 'get',
                success: function (d, x, s){
                    console.log(d);
                    // create a sorted array of epoch timestamps
                    var labels = new Set();
                    for (var key in d) {
                        if (d.hasOwnProperty(key)) {           
                            for(var i=0; i<d[key].length; i++){
                                labels.add(d[key][i][0]);
                            }
                        }
                    }
                    let array = Array.from(labels);
                    labels = array;
                    labels.sort();
                    // plot each point on this x axis
                    var datasets = [];
                    for (var key in d) {
                        if (d.hasOwnProperty(key)) {           
                            var plot_points = [];
                            var mapping = {};
                            for(var i=0; i<d[key].length; ++i){
                                mapping[d[key][i][0]] = i+1;
                            }
                            var last = 0;
                            for(var i=0; i<labels.length; ++i){
                                if(mapping[labels[i]] === undefined){
                                    plot_points.push(last);
                                }else{
                                    var point = mapping[labels[i]];
                                    last = point;
                                    plot_points.push(point);
                                }

                            }
                            var data = {label: key,
                                        data: plot_points};
                            datasets.push(data);
                        }
                    }
                    console.log(labels);
                    console.log(datasets);
                    var chartData = {'labels': labels, 'datasets': datasets};
                    var ctx = document.getElementById("myChart");
                    var myChart = new Chart(ctx, {"type": "line", "data": chartData});
                }});
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
    $("#check_status").hide();
    if(gettoken() !== undefined){
        $("#login").hide();
        $("#logout").show();
    }
    else{
        $("#login").show();
        $("#logout").hide();
    }
    update_score();
}); // MAIN on ready
