#!/usr/bin/env python3
'''module to hash password'''
import bcrypt


def _hash_password(password: str) -> bytes:
    """a method to harsh password"""
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password
