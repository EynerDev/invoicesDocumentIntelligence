from flask import Flask
from controllers.invoices_controller import factura_bp

# Crear la aplicación Flask
app = Flask(__name__)

# Registrar los blueprints (módulos de controladores)
app.register_blueprint(factura_bp, url_prefix='/api/factura')

if __name__ == '__main__':
    app.run(debug=True)
