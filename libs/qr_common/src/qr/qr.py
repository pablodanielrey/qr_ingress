import datetime
import random
import os
import hmac
import hashlib
from typing import OrderedDict

from .exceptions import InvalidHash

def timestamp_to_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

class QRCode:
    
    def __init__(self, firstname, lastname, grade=None, timestamp=None, salt=None):
        self.firstname = firstname
        self.lastname = lastname
        self.grade = grade if grade else 0
        self.timestamp = timestamp if timestamp else int(datetime.datetime.utcnow().timestamp())
        self.salt = salt if salt else random.randint(0,999999)

    def _has_access(self):
        return int(self.grade) == 10

    def to_message(self):
        data = [ f"{k}:{v}" for k,v in self.to_dict().items()]
        return ';'.join(data)
        #return f"FN:{self.firstname};LN:{self.lastname};C:{self.grade};D:{self.timestamp};R:{self.salt}"

    def to_dict(self):
        return OrderedDict({
            'FN': self.firstname,
            'LN': self.lastname,
            'C': self.grade,
            'D': self.timestamp,
            'R': self.salt
        })

    @classmethod
    def _str_to_dict(cls, data:str):
        decoded = {}
        sdata = data.split(';')
        for field in sdata:
            field_data = field.split(':')
            try:
                decoded[field_data[0]] = field_data[1]
            except IndexError as e:
                pass
        return decoded

    @classmethod
    def from_dict(cls, d:dict):
        salt = int(d['R'])
        grade = float(d['C']) if 'C' in d else None
        timestamp = int(d['D']) if 'D' in d else None
        qr = QRCode(d['FN'], d['LN'], grade, timestamp, salt)
        return qr

    @classmethod
    def from_message(cls, data:str):
        decoded = cls._str_to_dict(data)
        qr = cls.from_dict(decoded)
        return qr


class Message:

    SECRET_KEY = bytes(os.environ.get('QR_SECRET','1234567890'), 'utf-8')

    @classmethod
    def _get_hmac_signature(cls, data:str):
        bdata = bytes(data,'utf-8')
        return hmac.new(cls.SECRET_KEY, bdata, hashlib.sha1).hexdigest()

    def __init__(self, data:str):
        self.message = data
        self.hash_ = self._get_hmac_signature(self.message)

    @classmethod
    def from_string(cls, data:str):
        process = data.split(';')
        hash_ = process[-1]
        message_data = ';'.join(process[0:-1])
        message = Message(message_data)
        if message.hash_ == hash_:
            return message
        raise InvalidHash(f'{message.hash_} != {hash_}')

    def to_string(self):
        return f"{self.message};{self.hash_}"