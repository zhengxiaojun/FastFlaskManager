# -*- coding: utf-8 -*-

def my_pagination(pagination, endpoint, per_page):
    result_page = ""
    result_page += "<div style='text-align: center'>"
    result_page += "<ul class='pagination pagination-centered'>"
    if pagination.has_prev:
        result_page += "<li class='active'><a onclick='" + endpoint + "(1" + "," + str(per_page) + ");'>首页</a></li>"
        result_page += "<li class='active'><a onclick='" + endpoint + "(" + str(pagination.prev_num) \
                       + "," + str(per_page) + ");'>上一页</a></li>"
    else:
        result_page += "<li class='disabled'><a href='javascript:;'>首页</a></li>"
        result_page += "<li class='disabled'><a href='javascript:;'>上一页</a></li>"

    for page in pagination.iter_pages():
        if page:
            if page != pagination.page:
                result_page += "<li><a onclick='" + endpoint + "(" + str(page) + "," + str(per_page) + ");'>" \
                               + str(page) + " </a></li>"
            else:
                result_page += "<li class='active'><a href='javascript:;'>" + str(page) + "</a></li>"
        else:
            result_page += "<li><span class=ellipsis>…</span></li>"
    if pagination.has_next:
        result_page += "<li class='active'><a onclick='" + endpoint + "(" + str(pagination.next_num) \
                       + "," + str(per_page) + ");'>下一页</a></li>"
        result_page += "<li class='active'><a onclick='" + endpoint + "(" + str(pagination.pages) \
                       + "," + str(per_page) + ");'>末页</a></li>"
    else:
        result_page += "<li class='disabled'><a <a href='javascript:;'>下一页</a></li>"
        result_page += "<li class='disabled'><a <a href='javascript:;'>末页</a></li>"

    result_page += "</ul>"
    result_page += "</div>"
    result_page += "</div>"

    return result_page


def my_talbe(cols, data):
    result_table = ""
    result_table += "<table class='table table-hover'>"
    result_table += "<thead>"
    result_table += "<tr class='info'>"
    result_table += "<th>序号</th>"
    result_table += "<th>名</th>"
    result_table += "<th>姓</th>"
    result_table += "<th>电话</th>"
    result_table += "<th>邮箱</th>"
    result_table += "<th>操作</th>"
    result_table += "</tr>"
    result_table += "</thead>"
    result_table += "<tbody>"
    for line in data:
        result_table += "<tr>"
        for col in cols:
            result_table += "<td>" + str(getattr(line, col)) + "</td>"
        result_table += "<td><a href='/contact/change/" + str(line.id) + "'"
        result_table += " class='btn btn-success' role='button'>修改</a>"
        result_table += " "
        result_table += "<a href='/contact/delete/" + str(line.id) + "'"
        result_table += " class='btn btn-danger' role='button' onclick='javascript:return deletePrompt();'>删除</a></td>"
        result_table += "</tr>"
    result_table += "</tbody>"
    result_table += "</table>"

    return result_table
