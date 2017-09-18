# -*- coding: utf-8 -*-
from flask import render_template, request
from flask_login import login_required
from ftxml import *

from apps.tools import vxml


@vxml.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('tools/formatXML.html')


@vxml.route('/formatXml', methods=['POST'])
@login_required
def formatXml():
    fdata = ""
    try:
        xdata = request.form.get('xdata', '')
        fdata = format_xml(xdata)
    except Exception as error:
        fdata = str(error)
    finally:
        return fdata
