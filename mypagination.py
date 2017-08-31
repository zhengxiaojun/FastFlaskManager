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
