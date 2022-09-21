import hashlib
def hashit(x: str):
    salt = '114514($#Y%PSQF($ahsdfk23OQWEUR('.encode()
    s = hashlib.sha3_224()
    s.update(x.encode()+salt)
    return s.hexdigest()