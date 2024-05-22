from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import crypto

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/encrypt', methods=["GET","POST"])
def encrypt():
    if request.method =="POST":
        plain=request.form.get("plain")
        key=request.form.get("key")
        
        try:
            encrypted=crypto.substitution(plain,key)
            return render_template('encrypt.html', encrypted=encrypted, plain=plain, key=key)
        except ValueError as err:
            error=str(err)
            return render_template('encrypt.html', error=error, plain=plain, key=key)
    return render_template("encrypt.html")