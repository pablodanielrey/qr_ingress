import datetime
import random
import os
import hmac
import hashlib
import secrets
import base64
from typing import OrderedDict

from .exceptions import InvalidHash, InvalidMessage

def timestamp_to_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

class QRCode:
    
    def __init__(self, firstname, lastname, grade=None, timestamp=None):
        self.firstname = firstname
        self.lastname = lastname
        self.grade = grade if grade else 0
        self.timestamp = timestamp if timestamp else int(datetime.datetime.utcnow().timestamp())

    def _has_access(self):
        return int(self.grade) == 10

    def to_message(self):
        data = [ f"{k}:{v}" for k,v in self.to_dict().items()]
        sdata = ';'.join(data)
        bdata = base64.b64encode(bytes(sdata,'utf8')).decode('utf8')
        return bdata
        #return f"FN:{self.firstname};LN:{self.lastname};C:{self.grade};D:{self.timestamp};R:{self.salt}"

    def to_dict(self):
        return OrderedDict({
            'FN': self.firstname,
            'LN': self.lastname,
            'C': self.grade,
            'D': self.timestamp
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
        grade = float(d['C']) if 'C' in d else None
        timestamp = int(d['D']) if 'D' in d else None
        qr = QRCode(d['FN'], d['LN'], grade, timestamp)
        return qr

    @classmethod
    def from_message(cls, data:str):
        bdata = base64.b64decode(data).decode('utf8')
        decoded = cls._str_to_dict(bdata)
        qr = cls.from_dict(decoded)
        return qr


class Message:

    SECRET_KEY = bytes(os.environ.get('MESSAGE_SECRET','1234567890'), 'utf-8')
    SALT_LEN = 4

    @classmethod
    def _get_hmac_signature(cls, salt:str, data:str):
        return hmac.new(cls.SECRET_KEY, bytes(f"{salt}{data}",'utf8'), hashlib.sha1).hexdigest()

    def __init__(self, data:str, salt=None):
        self.message = data
        self.salt = salt if salt else secrets.token_hex(self.SALT_LEN)
        self.hash_ = self._get_hmac_signature(self.salt, self.message)

    @classmethod
    def from_string(cls, data:str):
        try:
            salt, message_data, hash_ = data.split(';')
        except ValueError as e:
            raise InvalidMessage()

        message = Message(message_data, salt)
        if hmac.compare_digest(message.hash_,hash_):
            return message
        raise InvalidHash(f'{message.hash_} != {hash_}')

    def to_string(self):
        return f"{self.salt};{self.message};{self.hash_}"