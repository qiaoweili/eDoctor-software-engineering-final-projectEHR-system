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

function user_info_success_callback(response) {
    let r = JSON.parse(response);
    console.log(r);
    if (r["code"] === "200") {
        let info = r["data"];
        document.getElementById("account").innerHTML = info["account"];
        document.getElementById("name").innerHTML = info["name"];
        document.getElementById("birth").innerHTML = info["birth"];
        document.getElementById("phone").innerHTML = info["phone"];
        if (info["sex"] === 0) {
            document.getElementById("sex").innerHTML = "男";
        } else {
            document.getElementById("sex").innerHTML = "女";
        }

        if (info["u_type"] === 0) {
            document.getElementById("u_type").innerHTML = "病人";
        } else {
            if (info["u_type"] === 1) {
                document.getElementById("u_type").innerHTML = "医生";
            } else {
                document.getElementById("u_type").innerHTML = "第三方合作商";
            }
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

function record_success_callback(response) {
    let r = JSON.parse(response);
    if (r["code"] === "200") {
        if(r["data"].length === 0){

        } else {
            var node_history = document.getElementById("history");

            for (var i = 0; i < r["data"].length; i++)
            {
                let od = r["data"][i];
                var ele_li = document.createElement("li");
                ele_li.className = "layui-timeline-item";
                var ele_i = document.createElement("i");
                ele_i.className = "layui-icon layui-timeline-axis";
                ele_i.innerHTML = "&#xe63f;";
                var ele_div = document.createElement("div");
                ele_div.className = "layui-timeline-content layui-text";
                var ele_h3 = document.createElement("h3");
                ele_h3.className = "layui-timeline-title";
                ele_h3.innerHTML = od["date"];
                var ele_p = document.createElement("p");
                ele_p.innerHTML = "Symptom: " + od["symptom"] + " med: " + od["medicine"];

                ele_div.appendChild(ele_h3);
                ele_div.appendChild(ele_p);
                ele_li.appendChild(ele_i);
                ele_li.appendChild(ele_div);

                node_history.appendChild(ele_li);
            }

            var ele_li = document.createElement("li");
            ele_li.className = "layui-timeline-item";
            var ele_i = document.createElement("i");
            ele_i.className = "layui-icon layui-timeline-axis";
            ele_i.innerHTML = "&#xe63f;";
            var ele_div = document.createElement("div");
            ele_div.className = "layui-timeline-content layui-text";
            var ele_inner_div = document.createElement("div");
            ele_inner_div.className = "layui-timeline-title";
            ele_inner_div.innerHTML = "past";
            ele_div.appendChild(ele_inner_div);
            ele_li.appendChild(ele_i);
            ele_li.appendChild(ele_div);
            node_history.appendChild(ele_li);
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


function init() {
    layui.use('element', function(){
      var element = layui.element;
    });

    console.log("js init completed");
    var xhr = gen_xhr(user_info_success_callback, universal_fail_callback);
    xhr.open("GET", "/api/data/user", true);
    xhr.send();

    xhr = gen_xhr(record_success_callback, universal_fail_callback);
    xhr.open("GET", "/api/record/search?limit=5&direct=-1", true);
    xhr.send();
}

init();