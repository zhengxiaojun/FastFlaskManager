/**
 * Created by jack_zheng on 17/8/29.
 */
var flag = null;
var poll_flag = null;

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

function genmd5() {
    $.post('genmd5', {inpmd5: $('input[name="inp"]').val()},
        function (data) {
            $('#result16low').text('16位小写：' + data.md5low16);
            $('#result16upe').text('16位大写：' + data.md5upe16);
            $('#result32low').text('32位小写：' + data.md5low32);
            $('#result32upe').text('32位大写：' + data.md5upe32);
        }
    );
}

function time_rfs() {
    var myDate = new Date();
    $("#c_time").text(myDate.toLocaleString());
    $("#u_time").text(Math.round(myDate.getTime() / 1000));
}

function get_current_time() {
    var gct = document.getElementById("get_ctime").value;
    if (gct.trim() == '停止') {
        clearInterval(flag);
        document.getElementById("get_ctime").value = '查看当前时间';
    }
    else {
        flag = self.setInterval("time_rfs()", 1000);
        document.getElementById("get_ctime").value = '停止';
    }
}

function time_to_sec() {
    ipt_ctime = $("#ipt_ctime").val();
    myDate = new Date();
    myDate.setFullYear(ipt_ctime.substring(0, 4));
    myDate.setMonth(Number(ipt_ctime.substring(4, 6)) - 1);
    myDate.setDate(ipt_ctime.substring(6, 8));
    myDate.setHours(ipt_ctime.substring(8, 10));
    myDate.setMinutes(ipt_ctime.substring(10, 12));
    myDate.setSeconds(ipt_ctime.substring(12, 14));
    myDate.setMilliseconds(ipt_ctime.substring(14, 17));
    $("#opt_utime").text(Math.round(myDate.getTime() / 1000));
}

function sec_to_time() {
    var myDate = new Date(Number($("#ipt_utime").val()) * 1000);
    $("#opt_ctime").text(myDate.toLocaleString());
}

function comparejson() {
    var ljson_data = ljson.getValue();
    var rjson_data = rjson.getValue();

    $.post("comparejson", {"ljson": ljson_data, "rjson": rjson_data}, function (rp) {
        document.getElementById("cmpjsonresult").innerHTML = rp;
    });
}

function clearJson() {
    ljson.setValue('');
    rjson.setValue('');
}

function fmtJson() {
    formatjson(ljson, ljson.getValue());
    formatjson(rjson, rjson.getValue());
}

function formatjson(obj, data) {
    try {
        f = JSON.parse(data);
    } catch (e) {
        toastr.info("格式或语法错误，具体信息：" + e);
        return;
    }
    $.post("formatjson", {"data": data}, function (rp) {
        obj.setValue(rp);
    });
}

function poll() {
    $.post('/ntfy/poll', {}, function (rp) {
            if (rp != "0") {
                document.getElementById("notifications-menu").innerHTML = rp;
            } else {
                nf_view = "<a href='#' class='dropdown-toggle' data-toggle='dropdown'>";
                nf_view += "<i class='fa fa-bell-o'></i>";
                nf_view += "</a>";
                document.getElementById("notifications-menu").innerHTML = nf_view;
            }
        }
    );
}

function ntfy_poll() {
    poll_flag = self.setInterval("poll()", 5000);
}

function switchNotify() {
    if ($("input[id='sNotify']").prop("checked") == true) {
        //当前为选中状态
        clearInterval(poll_flag);
    } else {
        //当前为不选中状态
        ntfy_poll();
    }
}