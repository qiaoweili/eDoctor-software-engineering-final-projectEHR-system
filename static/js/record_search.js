function gen_xhr(success_callback, fail_callback) {
    let xmlhttp;

    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            success_callback(xmlhttp.responseText);
        }
        if (xmlhttp.readyState === 4 && xmlhttp.status === 500) {
            fail_callback(xmlhttp.responseText);
        }
    };
    return xmlhttp;
}


function universal_fail_callback(response) {
    alert("network error");
}

function logout_success_callback(response) {
    let r = JSON.parse(response);
    if (r["code"] === "200") {
        if (r["data"]["href"] !== undefined) {
            alert("登出成功");
            window.location = r["data"]["href"];
        }
    } else {
        if (r["code"] === "500") {
            alert(r["err_msg"]);
            if (r["data"]["href"] !== undefined) {
                window.location = r["data"]["href"];
            }
        }
    }
}

function logout() {
    let xhr = gen_xhr(logout_success_callback, universal_fail_callback);
    xhr.open("POST", "/api/auth/logout", true);
    xhr.send();
}


function rewrite(){
    document.getElementById("disease_name").value="";
    let select = document.getElementById('disease_cat');
    select.selectedIndex=0;
}



//  YUAN LOAD TABLE
function render_table(){
    layui.use('table', function(){
      var table = layui.table;

      table.render({
        elem: '#record'
        ,height: 312
        ,url: '/api/record/search'
        ,response: {
            statusCode: "200"
        }
        ,page: true
        ,cols: [[
          {field: 'date', title: 'date', width:180, sort: true, fixed: 'left'}
          ,{field: 'doctor_id', title: 'doctor account', width:180}
          ,{field: 'patient_id', title: 'patient account', width:180}
          ,{field: 'disease_category', title: 'disease category', width:180}
          ,{field: 'disease_name', title: 'disease name', width:180}
          ,{field: 'symptom', title: 'symptom', width:180}
          ,{field: 'medicine', title: 'medicine', width:180}
        ]]
        ,id: 'testReload'
      });
//        var $ = layui.$, active = {
//        reload: function(){
//        //        var demoReload = $('#demoReload');
//        var date = $('#date').val();
//        var disease_name = $('#disease_name').val();
//        var disease_category = $('#disease_cat').val();
//        console.log("reload vars:",date,disease_name,disease_category);
//

//      var $ = layui.$, active = {
//        //注释：layui 搜索模块 Start
//            reload: function(){
//                var date = $('#date').val();
//                var disease_name = $('#disease_name').val();
//                var disease_category = $('#disease_cat').val();
//                console.log("reload vars:",date,disease_name,disease_category);
//                table.reload('testReload', {
//                    page: {
//                        curr: 1
//                    }
//                    ,where: {
//                             date: date
//                            ,disease_name: disease_name
//                            ,disease_category: disease_cat
//                    }
//                });
//            },


    });
}






//function init() {
//    render_table();
//    Number.prototype.toPercent = function () {
//        return (Math.round(this * 10000) / 100).toFixed(2) + '%';
//    };
//}
//
//init();