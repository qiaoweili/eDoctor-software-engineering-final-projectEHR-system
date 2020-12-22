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

function get_checked_radio_value(name) {
    let radios = document.getElementsByName(name);
    for (var i=0; i<radios.length; i++) {
        if(radios[i].checked == true) {
            return radios[i].value;
        }
    }
}

function login_success_callback(response) {
    let r = JSON.parse(response);
    console.log("login_success_call_back");
    if (r["code"] === "200") {
        alert("Login Success");
        window.sessionStorage.setItem("account", r["data"]["account"]);
        window.sessionStorage.setItem("token", r["data"]["token"]);
        document.cookie = "token=" + r["data"]["token"];
        window.location = r["data"]["href"];
    } else {
        if (r["code"] === "500") {
            alert(r["err_msg"]);
        }
    }
}

function login_fail_callback(response) {
    alert("network error");
}

function do_login() {
    let xhr = gen_xhr(login_success_callback, login_fail_callback);
    xhr.open("POST", "/api/auth/login", true);
    let account = document.getElementById("account").value;
    let password = document.getElementById("password").value;
    xhr.send(JSON.stringify({"account": account, "password": password}));
}

function register_success_callback(response) {
    let r = JSON.parse(response);
    console.log(r);
    if (r["code"] === "200") {
        alert("Register Success");
        window.location = r["data"]["href"];
    } else {
        if (r["code"] === "500") {
            alert(r["err_msg"])
        }
    }
}

function register_fail_callback(response) {
    alert("net error");
}

function do_register() {
    let xhr = gen_xhr(register_success_callback, register_fail_callback);
    xhr.open("POST", "/api/auth/register", true);
    let account = document.getElementById("reg_account").value;
    let password = document.getElementById("reg_password").value;
    let name = document.getElementById("name").value;
    let sex = get_checked_radio_value("sex");
    let birth = document.getElementById("birth").value;
    let phone = document.getElementById("phone").value;

    let u_type = get_checked_radio_value("u_type");
    let key;
    if (u_type == 0) {
        key = "";
    } else {
        if (u_type == 1) {
            key = document.getElementById("emp_key").value;
        } else {
            if (u_type == 2) {
                key = document.getElementById("tbp_key").value;
            }
        }
    }

    xhr.send(JSON.stringify({"account": account, "password": password,
              "name": name, "sex": sex, "birth": birth, "phone": phone, "u_type": u_type, "key": key}));
}

function init() {
    layui.use('element', function(){
      var element = layui.element;
    });
}

init();