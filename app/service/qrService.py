import qrcode
import os
from PIL import Image, ImageDraw
import logging

logger = logging.getLogger(__name__)


class QRService:
    @staticmethod
    def generate_qr(data, filename=None):
        QR_DIR = 'app/static/qr_codes'
        RELATIVE_STATIC_PATH = '/static/qr_codes/'

        qr = qrcode.QRCode(
            version=1,
            error_correction=getattr(qrcode.constants, f'ERROR_CORRECT_{data.error_correction}'),
            box_size=10,
            border=4,
        )
        qr.add_data(data.content)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Thêm watermark nếu không dùng HTTPS
        if not data.content.startswith('https://'):
            draw = ImageDraw.Draw(img)
            draw.text((10, 10), "KHÔNG BẢO MẬT", fill="red")
            logger.warning(f"Generated insecure QR for: {data.content[:50]}...")

        os.makedirs(QR_DIR, exist_ok=True)

        if filename:
            physical_path = os.path.join(QR_DIR, filename)
            img.save(physical_path)
            logger.info(f"QR saved to: {physical_path}")
            return f"{RELATIVE_STATIC_PATH}{filename}"

        return img
