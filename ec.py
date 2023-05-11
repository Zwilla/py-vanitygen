import ecdsa
import os
import hashlib
from ecdsa.util import string_to_number, number_to_string

# from bitcoin import *

# secp256k1, https://www.oid-info.com/get/1.3.132.0.10
_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
_r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
_b = 0x0000000000000000000000000000000000000000000000000000000000000007
_a = 0x0000000000000000000000000000000000000000000000000000000000000000
_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
curve_secp256k1 = ecdsa.ellipticcurve.CurveFp(_p, _a, _b)
generator_secp256k1 = ecdsa.ellipticcurve.Point(curve_secp256k1, _Gx, _Gy, _r)
oid_secp256k1 = (1, 3, 132, 0, 10)
SECP256k1 = ecdsa.curves.Curve("SECP256k1", curve_secp256k1, generator_secp256k1, oid_secp256k1)
ec_order = _r

curve = curve_secp256k1
generator = generator_secp256k1


def random_secret():
    convert_to_int = lambda array: int("".join(array).encode("hex"), 16)

    # Collect 256 bits of random data from the OS's cryptographically secure random generator
    byte_array = os.urandom(32)

    return convert_to_int(byte_array)


def get_point_pubkey(pointGP):
    if point.y() & 1:
        key = '03' + '%064x' % pointGP.x()
    else:
        key = '02' + '%064x' % pointGP.x()
    return key.decode('hex')


def get_point_pubkey_uncompressed(pointGp):
    key = '04' + \
          '%064x' % pointGp.x() + \
          '%064x' % pointGp.y()
    return key.decode('hex')


# Generate a new private key.
secret = random_secret()
print("Secret: {}".format(secret))

# Get the public key point.
point = secret * generator
print("EC point: {}".format(point))

# Given the point (x, y) we can create the object using:
point1 = ecdsa.ellipticcurve.Point(curve, point.x(), point.y(), ec_order)
assert point1 == point
count = 0

pubkey = get_point_pubkey(point1).encode("hex")
print("BTC public key: {}".format(pubkey))

checksum = (hashlib.sha256(hashlib.sha256(pubkey).digest()).digest()).encode("hex")
print("Checksum: {}".format(checksum))

address_base = '00' + pubkey + checksum[:4]
print("Address base: {}".format(address_base))

# print "BTC addres", hex_to_b58check(address_base)
