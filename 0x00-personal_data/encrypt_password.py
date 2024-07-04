#!/usr/bin/env python3
'''a module to use bcrypt in harshing'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''a function to harsh password'''
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode(), salt)
    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''a function to verify password'''
    return bcrypt.checkpw(password.encode(), hashed_password)
