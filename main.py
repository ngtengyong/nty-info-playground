from flask import Flask ,redirect ,url_for

# app = Flask(__name__)
app = Flask(__name__, static_folder='img')

# fetch SEA currency rates api
from routes.exchange_rates_api import exchange_rates_api_bp
app.register_blueprint(exchange_rates_api_bp)

# display exchanges rates on web page
from routes.exchange_rates import exchange_rates_bp
app.register_blueprint(exchange_rates_bp)

@app.route('/')
def index():
    return redirect(url_for('exchange_rates.display_exchange_rates'))

if __name__ == '__main__':
    app.run()
