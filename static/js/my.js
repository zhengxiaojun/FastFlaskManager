/**
 * Created by jack_zheng on 17/8/29.
 */
function queryForPages(page) {
    $.post("getusers", {"page": page}, function (rp) {
        document.getElementById("tbody").innerHTML = rp;
    });
}

function queryUsers(page, per_page) {
    $.ajax({
        url: "getusers",
        type: 'post',
        dataType: 'html',
        data: {"page": page, "per_page": per_page},
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
    queryUsers(1, per_page);
}