##############  FE  #########################
flask_sqlalchemy  ,  pagination


需要修改
~/python-envs/eve-rest/lib/python2.7/site-packages/flask_login$vim config.py

#: The default flash message to display when users need to log in.
LOGIN_MESSAGE = u'未登录，请先登录.'

~/python-envs/eve-rest/lib/python2.7/site-packages/flask_bootstrap/templates/bootstrap/base.html
<!--{% block scripts %}
    <script src="{{bootstrap_find_resource('jquery.js', cdn='jquery')}}"></script>
    <script src="{{bootstrap_find_resource('js/bootstrap.js', cdn='bootstrap')}}"></script>
    {%- endblock scripts %} -->


###############  REST API ###################

curl -i http://127.0.0.1:5000/api/auth/v1/users
curl -i http://127.0.0.1:5000/api/auth/v1/users/1
curl -i -H "Content-Type: application/json" -X POST -d '{"username":"api1","password":"api1","role":"0"}' http://127.0.0.1:5000/api/auth/v1/users
curl -i -H "Content-Type: application/json" -X PUT -d '{"role":"1"}' http://127.0.0.1:5000/api/auth/v1/users/5
curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/api/auth/v1/users/5

########### add auth  ###############
curl -i http://127.0.0.1:5000/api/auth/v1/users/5 -u admin:admin
curl -i -H "Content-Type: application/json" -X POST -d '{"username":"api1","password":"api1","role":"0"}' http://127.0.0.1:5000/api/auth/v1/users -u admin:admin
curl -i -H "Content-Type: application/json" -X PUT -d '{"password":"123456"}' http://127.0.0.1:5000/api/auth/v1/users/5 -u admin:admin
curl -i -H "Content-Type: application/json" -X DELETE http://127.0.0.1:5000/api/auth/v1/users/5 -u admin:admin


curl -i -H "Content-Type: application/json" http://127.0.0.1:5000/api/auth/token/1 -u demo:demo
curl -i http://127.0.0.1:5000/api/auth/v1/users/3 -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTUwNDUyMDgzNiwiaWF0IjoxNTA0NTIwMjM2fQ.eyJpZCI6MX0.41s2z4O8oUsdfofzznPyZh0tqDSM5nAYpMEWcVNvAd4:x


###############  FILE UPLOAD ###################
from flask_wtf.file import FileField

FileField 取自 flask_wtf.file 不能取 wtforms,不然会提示 'FileField' object has no attribute 'has_file'