import json
from qr_common.qr import QRCode, Message


if __name__ == '__main__':
    qr_message = input('ingrese el string del qr\n')
    m = Message.from_string(qr_message)
    qr = QRCode.from_message(m.message)
    d = qr.to_dict()
    print(json.dumps(d, ensure_ascii=False))