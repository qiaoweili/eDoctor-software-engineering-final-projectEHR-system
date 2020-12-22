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

function get_select_value(name){
    let select = document.getElementById(name);
    return  select.options[select.selectedIndex].text;
}

function universal_fail_callback(response) {
    alert("network error");
}

function profile_post_success_callback(response) {
    let r = JSON.parse(response);
    if (r["code"] === "200") {
        alert("更新个人资料成功");
        window.location = r["data"]["href"];
    } else {
        if (r["code"] === "500") {
            alert(r["err_msg"])
        }
    }
}

function post_profile() {
    let xhr = gen_xhr(profile_post_success_callback, universal_fail_callback);

    xhr.open("POST", "/api/data/user", true);

    let phone = document.getElementById("phone").value;
    let email = document.getElementById("email").value;
    let age = document.getElementById("age").value;
    let birth = document.getElementById("birth").value;
    let blood_type = get_select_value("blood_type");
    let height = document.getElementById("height").value;
    let weight = document.getElementById("weight").value;
    let allergy = document.getElementById("allergy").value;

    xhr.send(JSON.stringify({"phone": phone,
                             "email": email,
                             "age": age,
                             "birth": birth,
                             "blood_type": blood_type,
                             "height": height,
                             "weight":weight,
                             "allergy": allergy}));
}

function rewrite(){
    console.log("rewrite() working...")
    let phone = document.getElementById("phone").value="";
    let birth = document.getElementById("birth").value="";
    let age = document.getElementById("age").value="";
    let blood_type = document.getElementById("blood_type").value="";
    let height = document.getElementById("height").value="";
    let weight = document.getElementById("weight").value="";
    let allergy = document.getElementById("allergy").value="";
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

function init() {
    layui.use('element', function(){
      var element = layui.element;
    });
}

init();