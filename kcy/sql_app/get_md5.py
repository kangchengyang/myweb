import hashlib


# kcy
def generate_object_md5(data):
    m = hashlib.md5()
    m.update(data.getvalue())
    return str(m.hexdigest())
