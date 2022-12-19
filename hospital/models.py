from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Enum, DateTime
from hospital import db, app
from sqlalchemy.orm import relationship
from datetime import datetime

tienKham = int(100000)

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class List(BaseModel):

    ngay_kham = Column(String(50))
    benh = relationship('Benh', backref='list', lazy=True)

    def __str__(self):
        return self.name


class Admin(BaseModel):
    username = Column(String(50))
    password = Column(String(50), nullable=False)
    thuoc = relationship('Thuoc', backref='admin', lazy=True)
    quydinh = relationship('QuyDinh', backref='admin', lazy=True)


class QuyDinh(BaseModel):
    name = Column(String(50))
    price = Column(Integer)
    admin_id = Column(Integer, ForeignKey(Admin.id))

    def __str__(self):
        return self.name


class Benh(BaseModel):
    name = Column(String(50), nullable=False)
    sex = Column(String(50))
    birthday = Column(String(50))
    address = Column(String(100))
    list_id = Column(Integer, ForeignKey(List.id))
    phieu = relationship('Phieu', backref='benh', lazy=True)
    hoa_don = relationship('HoaDon', backref='benh', lazy=True)

    def __str__(self):
        return self.name


class PhieuThuoc(BaseModel):
    phieu_id = Column(Integer, ForeignKey('phieu.id'), primary_key=True)
    thuoc_id = Column(Integer, ForeignKey('thuoc.id'), primary_key=True)
    so_luong = Column(Integer, default=1)



class Phieu(BaseModel):
    ngay_kham = Column(DateTime, default=datetime.now())
    trieu_chung = Column(String(50))
    loai_benh = Column(String(50))
    thuoc = relationship("PhieuThuoc", backref='thuoc')
    benh_id = Column(Integer, ForeignKey(Benh.id))

    def __str__(self):
        return self.name


class Thuoc(BaseModel):
    name = Column(String(50), nullable=False)
    unit = Column(String(50))
    price = Column(Integer)
    using = Column(String(100))
    phieu = relationship("PhieuThuoc", backref='phieu')
    admin_id = Column(Integer, ForeignKey(Admin.id))

    def __str__(self):
        return self.name


class HoaDon(BaseModel):
    ngay_kham = Column(DateTime, default=datetime.now())
    tien_kham = Column(Float, default=tienKham)
    tien_thuoc = Column(Float)
    tong_tien = Column(Float)
    benh_id = Column(Integer, ForeignKey(Benh.id))

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # import hashlib
        # password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        # a = Admin(username="admin", password=password)
        # db.session.add(a)
        # db.session.commit()
        # b = Benh(name='Lê Văn Lâm', sex='Nam', birthday='01/02/2002', address='371 Nguyen Kiệm')
        # b1 = Benh(name='Huỳnh Minh Hoàng', sex='Nam', birthday='09/23/2001', address='835 Nguyen Kiệm')
        # b2 = Benh(name='Nguyễn Thị Ngọc Yến', sex='Nữ', birthday='01/22/2002', address='31 Vườn Lài')
        # db.session.add_all([b,b1,b2])
        # db.session.commit()
        # t = Thuoc(name='Paracetamol', unit='vỹ', price='20000', using='Trị đau đầu')
        # t1 = Thuoc(name='Motilum M', unit='chai', price='134000', using='Tiêu hóa')
        # t2 = Thuoc(name='Hapacol', unit='vien', price='1000', using='Hạ sốt')
        # t3 = Thuoc(name='Eurax', unit='chai', price='214000', using='Da liễu')
        # db.session.add_all([t, t1, t2, t3])
        # db.session.commit()
        # p = Phieu(trieu_chung='ho nhẹ', loai_benh='Sốt',benh_id='1')
        # p1 = Phieu(trieu_chung='sổ mũi', loai_benh='cảm cúm', benh_id='2')
        # p2 = Phieu(trieu_chung='đau tay', loai_benh='sưng tay', benh_id='3')
        # db.session.add_all([p, p1, p2])
        # db.session.commit()
        # pt = PhieuThuoc(phieu_id='1',thuoc_id='2',so_luong='4')
        # pt1 = PhieuThuoc(phieu_id='1', thuoc_id='4', so_luong='1')
        # pt2 = PhieuThuoc(phieu_id='1', thuoc_id='1', so_luong='3')
        # pt3 = PhieuThuoc(phieu_id='2', thuoc_id='2', so_luong='4')
        # pt4 = PhieuThuoc(phieu_id='2', thuoc_id='4', so_luong='3')
        # db.session.add_all([pt, pt1, pt2, pt3, pt4])
        # db.session.commit()
        # hd = HoaDon(tien_thuoc='200000',tong_tien='300000',benh_id='1')
        # hd1 = HoaDon(tien_thuoc='560000', tong_tien='660000', benh_id='2')
        # hd2 = HoaDon(tien_thuoc='420000', tong_tien='520000', benh_id='1')
        # hd3 = HoaDon(tien_thuoc='221000', tong_tien='321000', benh_id='1')
        # db.session.add_all([hd, hd1, hd2, hd3])
        # db.session.commit()
        qd = QuyDinh(name='Tiền khám', price=100000, admin_id=1)
        qd1 = QuyDinh(name='Bệnh nhân', price=40, admin_id=1)
        db.session.add_all([qd, qd1])
        db.session.commit()