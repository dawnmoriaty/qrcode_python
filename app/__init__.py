import logging

from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    logging.basicConfig(
        filename=app.config['SECURITY_LOGGING']['filename'],
        level=app.config['SECURITY_LOGGING']['level'],
        format=app.config['SECURITY_LOGGING']['format']
    )
    # Khởi tạo thư mục lưu trữ QR Code
    import os
    if not os.path.exists(app.config['QR_CODE_DIR']):
        os.makedirs(app.config['QR_CODE_DIR'])

    # Đăng ký Blueprints
    from app.controller.qrController import qr_bp
    app.register_blueprint(qr_bp)

    # Xử lý CORS (nếu cần)
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    return app
