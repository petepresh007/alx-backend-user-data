#!/usr/bin/env python3
'''a module for authentication'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''authentication class'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''require auth'''
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure path ends with a slash for comparison
        if not path.endswith('/'):
            path += '/'

        # Normalize excluded_paths to ensure all paths end with a slash
        excluded_paths = [
                ep if ep.endswith('/') else ep + '/' for ep in excluded_paths
        ]

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        '''authorized headers'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''current user'''
        return None
