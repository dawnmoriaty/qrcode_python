import qrcode
import os
from io import BytesIO
from PIL import Image
class QRService:
    @staticmethod
    def generate_qr(data, filename=None):
        # Đường dẫn thư mục QR
        QR_DIR = 'app/static/qr_codes'  # Đổi tên thư mục sang snake_case
        RELATIVE_STATIC_PATH = '/static/qr_codes/'  # Đường dẫn URL tĩnh

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(QR_DIR, exist_ok=True)

        if not filename:
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)
            return buffer
        else:
            # Tạo đường dẫn file vật lý
            physical_path = os.path.join(QR_DIR, filename)

            # Tạo đường dẫn URL truy cập
            url_path = f"{RELATIVE_STATIC_PATH}{filename}"

            img.save(physical_path)
            return url_path  # Tra ve url