from hospital.models import  BenhNhan, DanhSach, PhieuKham, DonThuoc, HoaDon, Thuoc
from hospital import db
from sqlalchemy import func, extract
from flask_login import current_user


def add_patient(name, sex, birthday, phone, address):
    b = BenhNhan(name=name.strip(), sex=sex.strip(), birthday=birthday.strip(), phone=phone.strip(), address=address.strip())

    db.session.add(b)
    db.session.commit()


def add_phieu_kham(trieu_chung, loai_benh, benh_nhan_id):
    p = PhieuKham(trieu_chung=trieu_chung, loai_benh=loai_benh, benh_nhan_id=benh_nhan_id)

    db.session.add(p)
    db.session.commit()

def add_don_thuoc(phieu_kham_id, thuoc_id, so_luong):
    pt = DonThuoc(phieu_kham_id=phieu_kham_id, thuoc_id=thuoc_id, so_luong=so_luong)

    db.session.add(pt)
    db.session.commit()


def add_date(ngay):
    d = DanhSach(ngay_kham=ngay)

    db.session.add(d)
    db.session.commit()


def update_date(benh_nhan_id,id):
    BenhNhan.query.filter_by(id=benh_nhan_id).first().danh_sach_id = id
    db.session.commit()


def tinh_tien(tienKham, tienthuoc):
    return tienKham + tienthuoc


def pay(tienkham, tienthuoc, tongtien, benh_nhan_id):
    p = HoaDon(tien_kham=tienkham, tien_thuoc=tienthuoc, tong_tien=tongtien, benh_nhan_id=benh_nhan_id)

    db.session.add(p)
    db.session.commit()


def stats_revenue(month = None):
    query = db.session.query(HoaDon.ngay_kham, BenhNhan.id, func.sum(HoaDon.tien_kham + HoaDon.tien_thuoc))\
                      .join(HoaDon, HoaDon.benh_nhan_id.__eq__(BenhNhan.id))

    if month:
        query = query.filter(extract('month', HoaDon.ngay_kham).__eq__(month))

    return query.group_by(HoaDon.ngay_kham, BenhNhan.id).all()


def count_thuoc_by_cate(month = None):
    query = db.session.query(Thuoc.name, Thuoc.unit, func.count(Thuoc.id))\
            .join(DonThuoc, DonThuoc.thuoc_id.__eq__(Thuoc.id), isouter=True)
    if month:
        query = query.filter(extract('month', HoaDon.ngay_kham).__eq__(month))

    return query.group_by(Thuoc.name, Thuoc.unit).all()
