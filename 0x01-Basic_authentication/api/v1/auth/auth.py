#!/usr/bin/env python3
'''a module for authentication'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''authentication class'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''require auth'''
        return False

    def authorization_header(self, request=None) -> str:
        '''authorized headers'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''current user'''
        return None
