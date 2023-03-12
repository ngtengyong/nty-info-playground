from flask import Flask

app = Flask(__name__)

# Import and register blueprints
from routes.exchange_rates import exchange_rates_bp
app.register_blueprint(exchange_rates_bp)

@app.route('/')
def index():
    return 'Welcome to the Exchange Rate API!'

if __name__ == '__main__':
    app.run()
