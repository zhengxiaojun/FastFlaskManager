/**
 * Created by jack_zheng on 17/8/29.
 */
function queryForPages(page) {
    $.post("getusers", {"page": page}, function (rp) {
        document.getElementById("tbody").innerHTML = rp;
    });
}

function queryContacts(page, per_page, kword) {
    $.ajax({
        url: "getcontacts",
        type: 'post',
        dataType: 'html',
        data: {"page": page, "per_page": per_page, "kword": kword},
        success: function callbackFun(data) {
            document.getElementById("pagi").innerHTML = data;
        },
        error: function callbackErr() {
            document.getElementById("pagi").innerHTML = "<span style='color: red'>NO DATA.</span>";
        }
    });
}

function queryTodolist(page, per_page) {
    $.ajax({
        url: "gettodolist",
        type: 'post',
        dataType: 'html',
        data: {"page": page, "per_page": per_page},
        success: function callbackFun(data) {
            document.getElementById("todo").innerHTML = data;
        },
        error: function callbackErr() {
            document.getElementById("todo").innerHTML = "<span style='color: red'>NO DATA.</span>";
        }
    });
}

function showCount() {
    var per_page = $("#perPage option:selected").text();
    queryContacts(1, per_page);
}

function deletePrompt() {
    if (confirm('确定删除吗？')) {
        return true;
    } else {
        return false;
    }
}

function formatXML() {
    xdata = document.getElementById("xmlData").value;
    $.ajax({
        url: "formatXml",
        type: 'post',
        dataType: 'html',
        data: {"xdata": xdata},
        beforeSend: function () {
            $("#fmtxml").attr({disabled: "disabled"});
            loaddiv = '<div id="pload" style="position:fixed;top:30%;z-index:1200;background:url(/static/img/loading.gif) top center no-repeat;width:100%;height:140px;margin:auto auto;" aria-hidden="true"></div>'
            $("body").append(loaddiv);
        },
        complete: function () {
            $("#fmtxml").removeAttr("disabled");
            $("#pload").remove();
        },
        success: function callbackFun(data) {
            document.getElementById("ftxmlData").value = data;
        },
        error: function callbackErr() {
            document.getElementById("ftxmlData").value = "未知错误.";
        }
    });
}

function copyftdata() {
    var ftxmlData = document.getElementById("ftxmlData");
    ftxmlData.select(); // 选择对象
    document.execCommand("Copy"); // 执行浏览器复制命令
}

function clearXML() {
    document.getElementById("xmlData").value = "";
    document.getElementById("ftxmlData").value = "";
}