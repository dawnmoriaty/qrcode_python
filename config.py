import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    QR_CODE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/qrCodes')
