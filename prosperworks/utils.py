from datetime import datetime

import exceptions


EPOCH = datetime(1970, 1, 1)


def validate_fields(fields, valid_fields, field_name=''):
    for field in fields.keys():
        if field not in valid_fields:
            raise exceptions.ProsperWorksApplicationException(
                u"%s is not a valid %s field." % (field, field_name)
            )


def timestamp(dt, convert_to_int=True):
    stamp = (dt - EPOCH).total_seconds()
    return int(stamp) if convert_to_int else stamp


class Data(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
