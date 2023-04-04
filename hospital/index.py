from flask import render_template, request, redirect, session
from hospital import utils, app, models, controllers
from hospital.models import DanhSach
from hospital.models import DonThuoc, PhieuKham, QuyDinh
from twilio.rest import Client
from hospital.admin import *
from flask_login import current_user


app.add_url_rule('/', 'index', controllers.index, methods=['get', 'post'])

app.add_url_rule('/create', 'create_list', controllers.create_list)

app.add_url_rule('/add-date', 'add_date', controllers.add_date, methods=['get', 'post'])

app.add_url_rule('/login', 'login', controllers.login)

app.add_url_rule('/admin-user', 'admin_user', controllers.admin_user, methods=["POST"])

app.add_url_rule('/phieu-kham', 'phieukham', controllers.phieukham)

app.add_url_rule('/api/create', 'create', controllers.create, methods=["POST"])

app.add_url_rule('/api/add-thuoc', 'thuoc', controllers.thuoc, methods=["POST"])


app.add_url_rule('/don-thuoc', 'donthuoc', controllers.donthuoc, methods=['get', 'post'])

app.add_url_rule('/pay', 'pay', controllers.pay, methods=['get', 'post'])

app.add_url_rule('/payall', 'payall', controllers.payall, methods=['get', 'post'])


if __name__ == '__main__':
    app.run(debug=True)
