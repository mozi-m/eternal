import sys

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


if len(sys.argv) != 2: # you can use  1024, 2048, 3072, or 4096
    print(f"Usage: python3 {sys.argv[0]} [size]")
    exit()

try:
    key_size = int(sys.argv[1])
except:
    print("Size must be an integer")
    exit()

private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)

private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

with open("private.key", "wb") as file:
    file.write(private_pem)

print(f"Private key ({key_size}-bit) saved as 'private.key'")
