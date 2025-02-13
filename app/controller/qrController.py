
from app.service.qrService import QRService
from app.models.qrModels import QRData

from flask import Blueprint, render_template, request
import uuid
import os

qr_bp = Blueprint('qr', __name__)


@qr_bp.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    if request.method == 'POST':
        data = request.form.get('data')

        # 1. Tạo tên file ngẫu nhiên và an toàn
        filename = f"qr_{uuid.uuid4().hex}.png"

        # 2. Khởi tạo model với đầy đủ tham số
        qr_data = QRData(
            content=data,
            size=request.form.get('size', 200),
            error_correction=request.form.get('error_correction', 'L')
        )

        # 3. Tạo thư mục nếu chưa tồn tại
        os.makedirs('app/static/qr_codes', exist_ok=True)

        # 4. Gọi service và xử lý đường dẫn
        try:
            qr_path = QRService.generate_qr(qr_data, filename)
            qr_image = f"/static/qr_codes/{filename}"  # Đường dẫn URL đúng
        except Exception as e:
            return render_template('error.html', error=str(e))

    return render_template('index.html', qr_image=qr_image)
