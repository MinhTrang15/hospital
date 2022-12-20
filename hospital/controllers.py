from flask import render_template, request, redirect, session
from hospital import utils, app, models
from hospital.models import List
from hospital.models import PhieuThuoc, Phieu, QuyDinh
from twilio.rest import Client
from hospital.admin import *


def index():
    success_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        sex = request.form.get('sex')
        birthday = request.form.get('birthday')
        address = request.form.get('address')

        try:
            utils.add_patient(name=name,
                              sex=sex,
                              birthday=birthday,
                              address=address)
            success_msg = 'Đăng ký thành công'
        except:
            success_msg = 'Đăng ký thất bại'
    return render_template('index.html', success_msg=success_msg)


def create_list():
    b = models.Benh.query.all()
    return render_template('createList.html', benh=b)


def add_date():
    success_msg = ''
    dem = 0
    if request.method.__eq__('POST'):
        day = request.form.get('day')
        b = models.Benh.query.all()
        d = models.List.query.all()
        data = models.QuyDinh.query.all()
        for s in data:
            if s.id == 2:
                BenhNhan = s.price
        for c in d:
            if c.ngay_kham == day:
                for benh in b:
                    if benh.list_id == c.id:
                        dem = dem + 1
                if dem >= BenhNhan:
                    success_msg = 'Ngày khám đã đủ bệnh nhân'
                    return render_template('createList.html', benh=b, success_msg=success_msg)
                else:
                    for e in b:
                        if not e.list_id:
                            id = List.query.filter_by(ngay_kham=day).first().id
                            utils.update_date(e.id, id)
                            dem = dem + 1
                        if (dem >= BenhNhan):
                            break
                    success_msg = 'Lập danh sách thành công'
                    SID = 'AC3a27d16d424e54ae6a115f16c0b7a865'
                    Auth_Token = '8816eb30589f88d2b0adaf4943848864'
                    cl = Client(SID, Auth_Token)
                    cl.messages.create(body='Bạn có lịch khám tại bệnh viện Lâm Hoàng Yến vào ngày ' + day,
                                       from_='+12058507103', to='+84336334143')
                return render_template('createList.html', benh=b, success_msg=success_msg)
        utils.add_date(day)
        count = 0
        for e in b:
            if not e.list_id:
                id = List.query.filter_by(ngay_kham=day).first().id
                utils.update_date(e.id, id)
                count = count + 1
            if (count >= BenhNhan):
                break
            success_msg = 'Lập danh sách thành công'
            SID = 'AC3a27d16d424e54ae6a115f16c0b7a865'
            Auth_Token = '127ed1de9dfe3fdb054eefa598203e3c'
            cl = Client(SID, Auth_Token)
            cl.messages.create(body='Bạn có lịch khám tại bệnh viện Lâm Hoàng Yến vào ngày ' + day,
                               from_='+12058507103', to='+84336334143')
        return render_template('createList.html', benh=b, success_msg=success_msg)


def login():
    return render_template('login.html')


def admin_user():
    err_msg = ''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        import hashlib
        passw = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        p = models.Admin.query.all()
        for i in p:
            if username == i.username and passw == i.password:
                return redirect('/admin')
        err_msg = 'Sai mật khẩu hoặc tên đăng nhập'
        return render_template('login.html', err_msg=err_msg)


def phieukham():
    b = models.Benh.query.all()
    return render_template('createPK.html', benh=b)


def create():
    data = request.json
    id = str(data['id'])
    name = str(data['name'])
    object = {
        'id' : id,
        'name' : name
    }
    session['user_infor'] = object
    return {
        'status': 200,
        'data': name
    }


def thuoc():
    data = request.json
    t = models.Thuoc.query.all()
    sl = str(data['sl'])
    name = str(data['name'])
    for i in t:
        if name == i.name:
            thuoc_id = i.id
            break
    key = app.config['THUOC_KEY']
    datas = session[key] if key in session else {}
    datas[thuoc_id] = {
        'name': name,
        'sl': sl
    }
    session[key] = datas


def phieu():
    t = models.Thuoc.query.all()
    if request.method.__eq__('POST'):
        id = session['user_infor']['id']
        trieuChung = request.form.get('trieuChung')
        benh = request.form.get('benh')
        utils.add_phieu(trieu_chung=trieuChung, loai_benh=benh, benh_id=id)
        phieu = models.Phieu.query.all()
        for c in phieu:
            if c.loai_benh == benh:
                phieu_id = c.id
                break
        key = app.config['THUOC_KEY']
        if key in session and session[key]:
            for d in session[key]:
                for i in t:
                    if d.name == t.name:
                        thuoc_id = i.id
                        break
                utils.add_phieu_thuoc(phieu_id=phieu_id, thuoc_id=thuoc_id, so_luong=d.sl)
    return render_template('phieu.html',thuoc=t)


def pay():
    benh_id = ''
    tongtien = ''
    tienthuoc = 0
    data = models.QuyDinh.query.all()
    for s in data:
        if s.id == 1:
            tienKham = s.price
    if request.method.__eq__('POST'):
        benh_id = request.form.get('id')
        phieu = models.Phieu.query.filter(Phieu.id.__eq__(benh_id)).all()
        for p in phieu:
            phieu_id = p.id
            phieu_thuoc = models.PhieuThuoc.query.filter(PhieuThuoc.id.__eq__(phieu_id)).all()
            for pt in phieu_thuoc:
                price = models.Thuoc.query.filter(Thuoc.id.__eq__(pt.thuoc_id)).first()
                tienthuoc = tienthuoc + (int(price.price) * int(pt.so_luong))
            tongtien = utils.tinh_tien(tienKham=tienKham, tienthuoc=tienthuoc)
            obj = {
                'benh_id': benh_id,
                'tienthuoc' : tienthuoc,
                'tienKham' : tienKham,
                'tongtien' : tongtien
            }
            session['recept'] = obj
    return render_template('pay.html', tongtien=tongtien, benh_id=benh_id, tienthuoc=int(tienthuoc), tienkham=int(tienKham))


def payall():
    data = models.QuyDinh.query.all()
    for s in data:
        if s.id == 1:
            tienKham = s.price
    success_msg = 'Thanh toán thành công'
    tongtien =''
    utils.pay(tienkham=tienKham,tienthuoc=session['recept']['tienthuoc'],tongtien=session['recept']['tongtien'],benh_id=session['recept']['benh_id'])
    return render_template('pay.html', success_msg=success_msg, tongtien=tongtien)