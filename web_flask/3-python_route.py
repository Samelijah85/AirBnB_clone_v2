#!/usr/bin/python3
"""A script that starts a Flask web application"""
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Displays: 'Hello HBNB'"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Displays: 'HBNB'"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """
    Displays: 'C ' followed by the value of the 'text' variable and replaces
    underscore '_' symbol with a space ' '
    """
    txt = text.replace('_', ' ')
    return f"C {txt}"


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text):
    """
    Displays: 'Python ' followed by the value of the 'text' variable and
    replaces underscore '_' symbol with a space ' '. The default values
    of 'text' is 'is cool'
    """
    txt = text.replace('_', ' ')
    return f'Python {txt}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
