from qr.qr import QRCode, Message

if __name__ == '__main__':
    print('QR de acceso permitido')
    qr = QRCode('Pablo', 'Rey', 10.0)
    m = Message(qr.to_message())
    print(m.to_string())

    print('QR de acceso no permitido')
    qr = QRCode('Pablo', 'Rey', 1.3)
    m = Message(qr.to_message())
    print(m.to_string())