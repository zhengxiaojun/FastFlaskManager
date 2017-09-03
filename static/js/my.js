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