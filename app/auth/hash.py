# _*_ coding:utf-8 _*_

#加盐哈希算法，保护密码
def salted_password(password, salt='$84<?.*&6k&^'):
    import hashlib

    def sha256(ascii_str):
        return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

    hash1 = sha256(password)
    hash2 = sha256(hash1 + salt)
    return hash2

