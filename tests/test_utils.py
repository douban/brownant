from pytest import raises

from brownant.utils import to_bytes_safe


UNICODE_STRING_SAMPLE = u"\u5b89\u5168 SAFE"
BYTES_SEQUENCE_SAMPLE = b"\xe5\xae\x89\xe5\x85\xa8 SAFE"


def test_to_bytes_safe():
    assert to_bytes_safe(UNICODE_STRING_SAMPLE) == BYTES_SEQUENCE_SAMPLE
    assert to_bytes_safe(BYTES_SEQUENCE_SAMPLE) == BYTES_SEQUENCE_SAMPLE
    assert to_bytes_safe(u"ABC") == b"ABC"
    assert to_bytes_safe(b"ABC") == b"ABC"

    assert type(to_bytes_safe(UNICODE_STRING_SAMPLE)) is bytes
    assert type(to_bytes_safe(BYTES_SEQUENCE_SAMPLE)) is bytes
    assert type(to_bytes_safe(u"ABC")) is bytes
    assert type(to_bytes_safe(b"ABC")) is bytes

    with raises(TypeError):
        to_bytes_safe(42)
