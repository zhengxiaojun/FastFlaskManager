# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify
from flask_login import login_required
from ftxml import *
from jsoncompare import jsoncompare
import hashlib, json

from apps.tools import vxml


@vxml.route('/formatXml', methods=['GET', 'POST'])
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


@vxml.route('/widget', methods=['GET'])
@login_required
def widget():
    return render_template('tools/widget.html')


@vxml.route('/genmd5', methods=['POST'])
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


@vxml.route('/comparejson', methods=['GET', 'POST'])
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
            result = jsoncompare.are_same(expect_json, actual_json)[1]
            if jsoncompare.are_same(expect_json, actual_json)[0]:
                result = "No different."
        except Exception as error:
            result = str(error)
        finally:
            return str(result)
