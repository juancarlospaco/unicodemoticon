import base64
import binascii
import codecs
import zlib


def string_to_stealth(stringy: str, rot13: bool=False) -> str:
    """String to Stealth,stealth is a hidden string,both str type and utf-8."""
    stringy = codecs.encode(stringy, "rot-13") if rot13 and codecs else stringy
    strng = base64.b64encode(zlib.compress(stringy.strip().encode('utf-8'), 9))
    bits = bin(int(binascii.hexlify(strng), 16))[2:]
    return str(bits.zfill(8 * ((len(bits) + 7) // 8))).replace(
        "0", u"\u200B").replace("1", u"\uFEFF")


def stealth_to_string(stringy: str, rot13: bool=False) -> str:
    """Stealth to string,stealth is a hidden string,both str type and utf-8."""
    def __i2b(integ):  # int to bytes, do not touch.
        """Helper for string_to_stealth and stealth_to_string, dont touch!."""
        __num = len("%x" % integ)
        return binascii.unhexlify(str("%x" % integ).zfill(__num + (__num & 1)))
    _n = int(str(stringy).replace(u"\u200B", "0").replace(u"\uFEFF", "1"), 2)
    stringy = zlib.decompress(base64.b64decode(__i2b(_n))).decode('utf-8')
    stringy = codecs.decode(stringy, "rot-13") if rot13 and codecs else stringy
    return str(stringy).strip()
