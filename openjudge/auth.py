from hashlib import sha256
from .utils import random_string, normalize


async def is_authenticated(token, db):
    return await db.tokens.find_one({"token": token}) is not None


async def register(uname, pwd, db):
    uname = normalize(uname)
    if (await db.credentials.find_one({"uname": uname})) is not None:
        return False, 'Already Exists'
    else:
        salt = random_string(100)
        hsh = sha256((pwd + salt).encode()).hexdigest()
        data = {"uname": uname, 'salt': salt, 'hsh': hsh}
        await db.credentials.insert_one(data)
        return True, 'ok'


async def generate_token(uname, pwd, db):
    uname = normalize(uname)
    data = await db.credentials.find_one({"uname": uname})
    if data is None:
        return False, 'No such user'
    hsh = sha256((pwd + data['salt']).encode()).hexdigest()
    if hsh != data['hsh']:
        return False, 'Wrong PWD'
    token = random_string()
    await db.tokens.insert_one({"token": token, "uname": uname})
    return True, token


async def remove_token(token, db):
    await db.tokens.find_one_and_delete({"token": token})


async def get_user_from_token(token, db):
    u = await db.tokens.find_one({"token": token})
    if u is None:
        return None
    return u['uname']
