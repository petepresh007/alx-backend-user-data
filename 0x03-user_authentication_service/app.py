#!/usr/bin/env python3
'''A simple Flask app with user authentication features.'''
from flask import Flask, jsonify, request, abort, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def index() -> str:
    """default page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def register():
    """register a user from auth"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    '''login valid users'''
    email = request.form.get("email")
    password = request.form.get("password")

    user = AUTH.valid_login(email, password)
    if not user:
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
        - Redirects to home route.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if not session_id:
        abort(403)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
