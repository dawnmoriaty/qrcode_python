import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    QR_CODE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/qr_codes')

    # Thêm cấu hình bảo mật
    BLACKLIST_DOMAINS = {
        'phishing.com',
        'malware.net',
        'danger-domain.org'
    }

    SECURITY_LOGGING = {
        'filename': 'security.log',
        'level': 'WARNING',
        'format': '%(asctime)s - %(levelname)s - %(message)s'
    }
