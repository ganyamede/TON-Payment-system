import logging
from flask import Flask
from flask_cors import CORS
from config import SECRET_KEY
from datetime import timedelta
from core.Application.routes import App

logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S', 
    filename='core/storage/path/core.log',
    filemode='a'
)

app = Flask(__name__, template_folder='core/Application/templates')
CORS(app)
app.secret_key = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.register_blueprint(App) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
