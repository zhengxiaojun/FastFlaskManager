# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from ftxml import *
from models import *
from forms import *
from jsoncompare import jsoncompare
from werkzeug.utils import secure_filename
from ext import myfile
import hashlib, json, os

from apps.tools import tool


@tool.route('/formatXml', methods=['GET', 'POST'])
@login_required
def formatXml():
    if request.method == 'GET':
        return render_template('tools/formatXML.html')
    else:
        fdata = ""
        try:
            xdata = request.form.get('xdata', '')
            fdata = format_xml(xdata)
        except Exception as error:
            fdata = str(error)
        finally:
            return fdata


@tool.route('/widget', methods=['GET'])
@login_required
def widget():
    return render_template('tools/widget.html')


@tool.route('/genmd5', methods=['POST'])
@login_required
def genmd5():
    a = request.form['inpmd5']
    a = a.encode('utf-8')
    md5 = hashlib.md5(a)
    md5 = md5.hexdigest()
    result = {}
    result['md5low32'] = md5
    result['md5upe32'] = md5.upper()
    result['md5low16'] = md5[8:24]
    result['md5upe16'] = md5.upper()[8:24]
    return jsonify(md5low32=result['md5low32'], md5upe32=result['md5upe32'], md5low16=result['md5low16'],
                   md5upe16=result['md5upe16'])


@tool.route('/comparejson', methods=['GET', 'POST'])
@login_required
def comparejson():
    if request.method == 'GET':
        return render_template('tools/jsoncompare.html')
    else:
        ljson = request.form.get('ljson', '')
        rjson = request.form.get('rjson', '')
        try:
            expect_json = json.loads(ljson, encoding='utf-8')
            actual_json = json.loads(rjson, encoding='utf-8')
            # result = jsoncompare.are_same(expect_json, actual_json,False,["status"])[0]
            if isinstance(expect_json, dict) and isinstance(actual_json, dict):
                result = jsoncompare.are_same(expect_json, actual_json)[1]
                if jsoncompare.are_same(expect_json, actual_json)[0]:
                    result = "No different."
            else:
                result = "the data is not a json format."
        except Exception as error:
            result = str(error)
        finally:
            return str(result)


@tool.route('/formatjson', methods=['POST'])
@login_required
def formatjson():
    data = request.form.get('data', '')
    data = data.encode('utf-8')
    try:
        data = eval(data)
        result = json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
    except Exception as error:
        result = str(error)
    finally:
        return result


@tool.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        files = Filelist.query.paginate(page, 5, False).items
        pagination = Filelist.query.paginate(page, 5, True)
        return render_template('tools/upload.html', form=form, files=files, pagination=pagination)
    else:
        if form.validate_on_submit():
            filename = secure_filename(form.file.data.filename)
            md5_filename = Filelist.get_md5_filename(filename)
            # 请注意保存文件时是用了UploadSet对象调用了save方法，而且这个save方法的第一个参数是文件对象，第二个参数是文件名
            myfile.save(form.file.data, name=md5_filename)

            file = Filelist(filename, md5_filename, myfile.path(md5_filename), myfile.url(md5_filename))
            db.session.add(file)
            db.session.commit()
            flash('您上传了一个文件!')
            Notifications.notify(current_user.username, u"文件", u"上传了一个新文件")
        else:
            flash(form.errors)
        return redirect(url_for('tool.upload'))


@tool.route('/remove/<int:id>')
@login_required
def remove(id):
    file = Filelist.query.filter_by(id=id).first_or_404()
    os.remove(file.path)
    db.session.delete(file)
    db.session.commit()
    flash('您成功删除一个文件!')
    Notifications.notify(current_user.username, u"文件", u"删除了一个文件")
    return redirect(url_for('tool.upload'))
