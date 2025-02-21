from app.service.qrService import QRService
from app.models.qrModels import QRData
from flask import Blueprint, render_template, request, current_app
import uuid
import os
import tldextract
import logging

qr_bp = Blueprint('qr', __name__)
logger = logging.getLogger(__name__)


# Thêm hàm validate mới
def validate_qr_data(data: str):
    """ Kiểm tra dữ liệu đầu vào """
    MAX_LENGTH = 2048
    MALICIOUS_DOMAINS = {'phishing.com', 'malware.net'}

    if len(data) > MAX_LENGTH:
        raise ValueError(f"Dữ liệu vượt quá {MAX_LENGTH} ký tự")

    if not data.startswith(('http://', 'https://')):
        raise ValueError("Chỉ hỗ trợ URL HTTP/HTTPS")

    domain = tldextract.extract(data).registered_domain
    if domain in MALICIOUS_DOMAINS:
        raise ValueError(f"Domain {domain} bị chặn")


@qr_bp.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    if request.method == 'POST':
        try:
            data = request.form.get('data')

            # Validate dữ liệu mới
            validate_qr_data(data)

            # Ghi log
            logger.info(f"Attempting to generate QR for: {data[:50]}...")

            filename = f"qr_{uuid.uuid4().hex}.png"
            qr_data = QRData(
                content=data,
                size=request.form.get('size', 200),
                error_correction=request.form.get('error_correction', 'L')
            )

            os.makedirs('app/static/qr_codes', exist_ok=True)
            qr_path = QRService.generate_qr(qr_data, filename)

            # Thêm cảnh báo vào template
            warning = None
            if not data.startswith('https://'):
                warning = "CẢNH BÁO: Kết nối không an toàn"

            return render_template(
                'index.html',
                qr_image=f"/static/qr_codes/{filename}",
                warning=warning
            )

        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            return render_template('error.html', error=str(e))
        except Exception as e:
            logger.critical(f"System error: {str(e)}")
            return render_template('error.html', error="Lỗi hệ thống")

    return render_template('index.html', qr_image=qr_image)
