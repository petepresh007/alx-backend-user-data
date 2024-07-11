#!/usr/bin/env python3
'''basic autentication'''
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from api.v1.views.users import User


class BasicAuth(Auth):
    '''class that inherits from auth'''
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        '''method for auth'''
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """
        Decodes the Base64 part of the Authorization header.

        Args:
            base64_authorization_header (str): The Base64 part.

        Returns:
            str: The decoded value as a UTF-8 string, or None if invalid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
             self, decoded_base64_authorization_header: str
             ) -> (str, str):
        """
        Extracts the user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str): The decoded.

        Returns:
            tuple: The user email and password, or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_credentials = decoded_base64_authorization_header.split(':', 1)
        return user_credentials[0], user_credentials[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        '''method to authenticate credentials'''
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves current user"""
        if request is None:
            return None

        # Step 2: Get the Authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Step 3: Extract Base64 part of the header
        base64_auth_header = self.extract_base64_authorization_header(
                auth_header
                )
        if base64_auth_header is None:
            return None

        # Step 4: Decode the Base64 string
        decoded_auth_header = self.decode_base64_authorization_header(
                base64_auth_header
                )
        if decoded_auth_header is None:
            return None

        # Step 5: Extract user credentials
        user_email, user_pwd = self.extract_user_credentials(
                decoded_auth_header
                )
        if user_email is None or user_pwd is None:
            return None

        # Step 6: Retrieve the User object
        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
