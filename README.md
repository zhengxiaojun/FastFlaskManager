# mypage
flask_sqlalchemy,pagination


需要修改
~/python-envs/eve-rest/lib/python2.7/site-packages/flask_login$vim config.py

#: The default flash message to display when users need to log in.
LOGIN_MESSAGE = u'未登录，请先登录.'

~/python-envs/eve-rest/lib/python2.7/site-packages/flask_bootstrap/templates/bootstrap/base.html
<!--{% block scripts %}
    <script src="{{bootstrap_find_resource('jquery.js', cdn='jquery')}}"></script>
    <script src="{{bootstrap_find_resource('js/bootstrap.js', cdn='bootstrap')}}"></script>
    {%- endblock scripts %} -->