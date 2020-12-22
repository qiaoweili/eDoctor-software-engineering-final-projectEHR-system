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

//function get_checked_radio_value(name) {
//    let radios = document.getElementsByName(name);
//    for (var i=0; i<radios.length; i++) {
//        if(radios[i].checked == true) {
//            return radios[i].value;
//        }
//    }
//}

function get_select_value(name){
    let select = document.getElementById(name);
    return  select.options[select.selectedIndex].text;
}

function record_post_success_callback(response) {
    let r = JSON.parse(response);
    if (r["code"] === "200") {
        alert("新建医疗记录成功");
        window.location = r["data"]["href"];
    } else {
        if (r["code"] === "500") {
            alert(r["err_msg"])
        }
    }
}

function record_post_fail_callback(response) {
    alert("net error");
}

function post_record() {
    var xhr = gen_xhr(record_post_success_callback, record_post_fail_callback);
    xhr.open("POST", "/api/record/upload", true);

    let patient_id = document.getElementById("patient_id").value;
//    let gender = get_checked_radio_value('sex');
    let disease_category = get_select_value("disease_cat");
    let disease_name = document.getElementById("disease_name").value;
    let symptom = document.getElementById("symptom").value;
    let medicine = document.getElementById("medicine").value;

    let data = JSON.stringify({"patient_id": patient_id,
//                             "gender": gender,
                             "disease_name": disease_name,
                             "disease_category": disease_category,
                             "symptom":symptom,
                             "medicine":medicine})

    xhr.send(data);
}

function rewrite(){
    document.getElementById("patient_id").value="";
    let select = document.getElementsByName('disease_cat');
    select.options[select.selectedIndex].value=1;
    let disease_name = document.getElementById("disease_name").value="";
    let symptom = document.getElementById("symptom").value="";
    let medicine = document.getElementById("medicine").value="";
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

function universal_fail_callback(response) {
    alert("network error");
}

function logout() {
    let xhr = gen_xhr(logout_success_callback, universal_fail_callback);
    xhr.open("POST", "/api/auth/logout", true);
    xhr.send();
}

function init() {
    layui.use('element', function(){
      var element = layui.element;
    });
}

init();