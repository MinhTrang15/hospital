from hospital.models import  Benh, List, Admin, Phieu, PhieuThuoc, HoaDon
from hospital import db
from sqlalchemy import func
import hashlib


def add_patient(name, sex, birthday, address):
    b = Benh(name=name.strip(), sex=sex.strip(), birthday=birthday.strip(), address=address.strip())

    db.session.add(b)
    db.session.commit()


def add_phieu(trieu_chung, loai_benh, benh_id):
    p = Phieu(trieu_chung=trieu_chung, loai_benh=loai_benh, benh_id=benh_id)

    db.session.add(p)
    db.session.commit()


def add_phieu_thuoc(phieu_id, thuoc_id, so_luong):
    pt = PhieuThuoc(phieu_id=phieu_id, thuoc_id=thuoc_id, so_luong=so_luong)

    db.session.add(pt)
    db.session.commit()


def add_date(ngay):
    d = List(ngay_kham=ngay)

    db.session.add(d)
    db.session.commit()


def update_date(benh_id,id):
    Benh.query.filter_by(id=benh_id).first().list_id = id
    db.session.commit()


def tinh_tien(tienKham, tienthuoc):
    return tienKham + tienthuoc


def pay(tienkham, tienthuoc, tongtien, benh_id):
    p = HoaDon(tien_kham=tienkham, tien_thuoc=tienthuoc, tong_tien=tongtien, benh_id=benh_id)

    db.session.add(p)
    db.session.commit()


def stats_revenue(mounth = None):
    query = db.session.query(HoaDon.ngay_kham,Benh.id, func.sum(HoaDon.tien_kham + HoaDon.tien_thuoc))\
                      .join(HoaDon, HoaDon.benh_id.__eq__(Benh.id))

    return query.group_by(HoaDon.ngay_kham,Benh.id).all()
