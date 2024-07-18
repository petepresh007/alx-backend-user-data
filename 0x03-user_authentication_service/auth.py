#!/usr/bin/env python3
'''module to hash password'''
import bcrypt
from db import DB
from typing import Union
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """a method to harsh password"""
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password


def _generate_uuid() -> str:
    """Generate a new UUID and return its string representation."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_password = _hash_password(password)
            usr = self._db.add_user(
                    email=email,  hashed_password=hashed_password
                    )
            return usr

    def valid_login(self, email: str, password: str) -> bool:
        """validate user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(
                        password.encode('utf-8'), user.hashed_password
                        )
        except NoResultFound:
            return False
        return True

    def create_session(self, email: str) -> str:
        '''returns the email'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        '''get users by session id'''
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        '''a mothod that update session id to none'''
        user = self._db.find_user_by(id=user_id)
        if user_id is None or not user:
            return None
        if user:
            self._db.update_user(user.session_id=None)
