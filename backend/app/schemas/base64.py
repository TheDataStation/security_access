# blatantly ripped off from https://github.com/samuelcolvin/pydantic/pull/698/files
import base64
import binascii
from contextlib import contextmanager
from typing import Any, Type, Generator

from pydantic import PydanticTypeError, errors

ExcType = Type[Exception]


@contextmanager
def change_exception(
    raise_exc: ExcType, *except_types: ExcType
) -> Generator[None, None, None]:
    try:
        yield
    except except_types as e:
        raise raise_exc from e


class Base64Error(PydanticTypeError):
    msg_template = "value is not valid base64"

class Base64Bytes(bytes):
    @classmethod
    def encode(cls, data: Any) -> "Base64Bytes":
        if isinstance(data, str):
            data = data.encode()
        elif not isinstance(data, int):
            data = bytes(data)
        return cls(base64.b64encode(data))

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> "Base64Bytes":
        if isinstance(value, (bytes, bytearray, memoryview)):
            pass
        elif isinstance(value, str):
            value = value.encode()
        else:
            if isinstance(value, int):
                raise Base64Error
            with change_exception(Base64Error, TypeError):
                value = bytes(value)
        with change_exception(Base64Error, binascii.Error):
            base64.b64decode(value, validate=True)
        return cls(value)
