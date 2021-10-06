from qr.qr import QRCode, Message

if __name__ == '__main__':
    qr = QRCode('Pablo', 'Rey', 10.0)
    m = Message(qr.to_message())
    print(m.to_string())