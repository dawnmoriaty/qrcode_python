from dataclasses import dataclass

@dataclass
class QRData:
    content: str
    size: int = 200
    error_correction: str = 'L'
