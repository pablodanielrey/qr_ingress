import datetime
import random


def timestamp_to_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

class QRCode:

    def __init__(self, firstname, lastname, grade = None, timestamp = None):
        self.firstname = firstname
        self.lastname = lastname
        self.grade = grade
        self.timestamp = timestamp if timestamp else int(datetime.datetime.utcnow().timestamp())

    def _has_access(self):
        return self.grade == 10

    def encode(self):
        return f"A:{self._has_access()};FN:{self.firstname};LN:{self.lastname};C:{self.grade};D:{self.timestamp};R:{random.randint(0,999999)};"


    @classmethod
    def _decode_to_dict(cls, data:str):
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
    def decode(cls, data:str):
        decoded = cls._decode_to_dict(data)
        grade = decoded['C'] if 'C' in decoded else None
        timestamp = int(decoded['D']) if 'D' in decoded else None
        return QRCode(decoded['FN'], decoded['LN'], grade, timestamp)
