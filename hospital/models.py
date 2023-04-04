from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Enum, DateTime
from hospital import db, app
from sqlalchemy.orm import relationship
from datetime import datetime

tienKham = int(100000)


class BaseModel(db.Model):
    __abstract__ = True


class DanhSach(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_kham = Column(String(50))
    benh_nhan = relationship('BenhNhan', backref='list', lazy=True)

    def __str__(self):
        return self.name


class NhanVien(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    password = Column(String(50), nullable=False)
    thuoc = relationship('Thuoc', backref='nhanvien', lazy=True)
    quydinh = relationship('QuyDinh', backref='nhanvien')


class QuyDinh(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    content = Column(Integer)
    admin_id = Column(Integer, ForeignKey(NhanVien.id))

    def __str__(self):
        return self.name


class BenhNhan(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    sex = Column(String(50), nullable=False)
    birthday = Column(String(50), nullable=False)
    phone = Column(String(12), nullable=False)
    address = Column(String(100))
    danh_sach_id = Column(Integer, ForeignKey(DanhSach.id))
    phieu_kham = relationship('PhieuKham', backref='benhnhan', lazy=True)
    hoa_don = relationship('HoaDon', backref='benhnhan', lazy=True)

    def __str__(self):
        return self.name


class PhieuKham(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_kham = Column(DateTime, default=datetime.now())
    trieu_chung = Column(String(50))
    loai_benh = Column(String(50))
    cach_dung = Column(String(100))
    # thuoc_id = relationship("DonThuoc", backref='thuoc')
    don_thuoc_id = relationship("DonThuoc", backref='phieukham')
    benh_nhan_id = Column(Integer, ForeignKey(BenhNhan.id))

    def __str__(self):
        return self.name


class LoaiThuoc(BaseModel):
    category = Column(String(50), primary_key=True, nullable=False)
    thuoc = relationship('Thuoc', backref='loaithuoc', lazy=True)


class DonViThuoc(BaseModel):
    unit = Column(String(50), primary_key=True, nullable=False)
    thuoc = relationship('Thuoc', backref='donvithuoc', lazy=True)


class Thuoc(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer)
    thuoc = relationship("DonThuoc", backref='thuoc')
    unit = Column(String(50), ForeignKey(DonViThuoc.unit))
    category_id = Column(String(50), ForeignKey(LoaiThuoc.category))
    nhan_vien_id = Column(Integer, ForeignKey(NhanVien.id))

    def __str__(self):
        return self.name


class DonThuoc(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    phieu_kham_id = Column(Integer, ForeignKey(PhieuKham.id), primary_key=True)
    thuoc_id = Column(Integer, ForeignKey(Thuoc.id), primary_key=True)
    so_luong = Column(Integer, default=1)


class HoaDon(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_kham = Column(DateTime, default=datetime.now())
    tien_kham = Column(Float, default=tienKham)
    tien_thuoc = Column(Float)
    tong_tien = Column(Float)
    benh_nhan_id = Column(Integer, ForeignKey(BenhNhan.id))

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # b = BenhNhan(name='Lê Văn Lâm', sex='Nam', birthday='01/02/2002', phone='123456', address='371 Nguyen Kiệm')
        # b1 = BenhNhan(name='Huỳnh Minh Hoàng', sex='Nam', birthday='09/23/2001', phone='123456', address='835 Nguyen Kiệm')
        # b2 = Benh(name='Nguyễn Thị Ngọc Yến', sex='Nữ', birthday='01/22/2002', phone='123456', address='31 Vườn Lài')
        # db.session.add_all([b,b1,b2])
        # db.session.commit()
        # t = Thuoc(name='Paracetamol', unit='vỹ', price='20000', using='Trị đau đầu')
        # t1 = Thuoc(name='Motilum M', unit='chai', price='134000', using='Tiêu hóa')
        # t2 = Thuoc(name='Hapacol', unit='vien', price='1000', using='Hạ sốt')
        # t3 = Thuoc(name='Eurax', unit='chai', price='214000', using='Da liễu')
        # db.session.add_all([t, t1, t2, t3])
        # db.session.commit()
        # p = PhieuKham(trieu_chung='ho nhẹ', loai_benh='Sốt',benh_id='1')
        # p1 = PhieuKham(trieu_chung='sổ mũi', loai_benh='cảm cúm', benh_id='2')
        # p2 = PhieuKham(trieu_chung='đau tay', loai_benh='sưng tay', benh_id='3')
        # db.session.add_all([p, p1, p2])
        # db.session.commit()
        # pt = DonThuoc(phieu_id='1',thuoc_id='2',so_luong='4')
        # pt1 = DonThuoc(phieu_id='1', thuoc_id='4', so_luong='1')
        # pt2 = DonThuoc(phieu_id='1', thuoc_id='1', so_luong='3')
        # pt3 = DonThuoc(phieu_id='2', thuoc_id='2', so_luong='4')
        # pt4 = PhieuThuoc(phieu_id='2', thuoc_id='4', so_luong='3')
        # db.session.add_all([pt, pt1, pt2, pt3, pt4])
        # db.session.commit()
        # hd = HoaDon(tien_thuoc='200000',tong_tien='300000',benh_id='1')
        # hd1 = HoaDon(tien_thuoc='560000', tong_tien='660000', benh_id='2')
        # hd2 = HoaDon(tien_thuoc='420000', tong_tien='520000', benh_id='1')
        # hd3 = HoaDon(tien_thuoc='221000', tong_tien='321000', benh_id='1')
        # db.session.add_all([hd, hd1, hd2, hd3])
        # db.session.commit()
        c1 = QuyDinh(name='Tiền khám', content=100000, admin_id=1)
        c2 = QuyDinh(name='Bệnh nhân', content=40, admin_id=1)
        db.session.add_all([c1, c2])
        db.session.commit()

