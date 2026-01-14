import os
from flask import Flask
from src.controllers.invoices_controller import factura_bp
from src.controllers.provider_controller import provider_bp

# Crear la aplicación Flask
app = Flask(__name__)

# Registrar los blueprints (módulos de controladores)
app.register_blueprint(factura_bp, url_prefix='/api/factura')
app.register_blueprint(provider_bp, url_prefix='/api/provider')

if __name__ == '__main__':
    app.run(debug=True)
