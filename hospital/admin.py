from hospital import app, db, utils
from flask_admin import Admin, BaseView, expose
from hospital.models import Thuoc, QuyDinh
from flask_admin.contrib.sqla import ModelView
from flask import request

class StatsView(BaseView):
    @expose('/')
    def index(self):
        stats = utils.stats_revenue(mounth=request.args.get('mounth'))
        return self.render('admin/stats.html', stats=stats)

admin = Admin(app=app, name='Quản trị bán hàng', template_mode='bootstrap4')
admin.add_view(ModelView(Thuoc, db.session, name='Thuốc'))
admin.add_view(ModelView(QuyDinh, db.session, name='Quy định'))
admin.add_view(StatsView(name='Thống kê'))