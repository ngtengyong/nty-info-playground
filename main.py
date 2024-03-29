from flask import Flask,render_template
from datetime import datetime

# app = Flask(__name__)
app = Flask(__name__, static_folder='img')

# fetch SEA currency rates api
from routes.exchange_rates_api import exchange_rates_api_bp
app.register_blueprint(exchange_rates_api_bp)

# display exchanges rates on web page
from routes.exchange_rates import exchange_rates_bp
app.register_blueprint(exchange_rates_bp)

# import and register get_country_data blueprint
from routes.get_country_data_api import get_country_data_api_bp
app.register_blueprint(get_country_data_api_bp)

from routes.get_country_data import get_country_data_bp
app.register_blueprint(get_country_data_bp)

from routes.setup_api import setup_api_bp
app.register_blueprint(setup_api_bp)

@app.route('/')
def index():
    current_year = datetime.now().year
    return render_template('index.html', current_year=current_year)

if __name__ == '__main__':
    app.run()
