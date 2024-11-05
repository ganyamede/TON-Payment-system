from flask import Blueprint
from core.Application.api.views import ( 
    HomeView, 
    PayView,
    CheckPay
)

App = Blueprint('main', __name__, template_folder='core/Application/templates')

App.add_url_rule('/', 'Home', view_func=HomeView)
App.add_url_rule('/', 'Pay', view_func=PayView, methods=['POST'])
App.add_url_rule('/Check/', 'Check', view_func=CheckPay, methods=['POST'])