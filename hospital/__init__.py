from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
# import cloudinary
from flask import Flask
from flask_admin import Admin

app = Flask(__name__)


app.secret_key = '$%^*&())(*&%^%4678675446&#%$%^&&*^$&%&*^&^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/hospital?charset=utf8mb4' % quote('Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['THUOC_KEY'] = 'thuoc'

# cloudinary.config(cloud_name='dddmytz0i',
#                   api_key='148484514625777',
#                   api_secret='o8IME08ByccB7OqRbVTnRbHuIUk')

db = SQLAlchemy(app=app)
# admin = Admin(app=app, name='QUẢN TRỊ VIÊN', template_mode='bootstrap4')
# tienKham = int(100000)
# BenhNhan = 40
