from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import crypto
import io

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    return render_template('index.html')


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

@app.route('/decrypt', methods=["GET","POST"])
def decrypt():
    mode = request.form.get("mode", "known")  # Default to "known" if not provided
    encrypted = request.form.get("encrypted", "")
    key = request.form.get("key", "a")
    attempt = int(request.form.get("attempts","1"))
    plain = ""
    error = ""
    

    if request.method =="POST":
        if mode=='known':
            try:
                plain=crypto.desubstitution(encrypted,key)
                return render_template('decrypt.html', plain=plain, encrypted=encrypted, key=key, mode=mode)
            except ValueError as err:
                error=str(err)
                return render_template('decrypt.html', error=error, encrypted=encrypted, key=key,mode=mode)
        elif mode=='caeser':
            guesses=crypto.guessCaeser(encrypted,attempts=attempt)
            return render_template('decrypt.html', plain=guesses, encrypted=encrypted, mode=mode, attempts=attempt)
            
    return render_template("decrypt.html")

@app.route("/analysis", methods=["GET","POST"])
def analysis():
    if request.method =="POST":
        encrypted=request.form.get("encrypted")
        analysis=crypto.frequencyAnalysis(encrypted)
        
        img=io.BytesIO()
        crypto.histFreqAnalysis(encrypted).savefig(img, format='png')
        img.seek(0)

        img_path = 'static/images/analysis.png'
        with open(img_path, 'wb') as f:
            f.write(img.getbuffer())

        return render_template("analysis.html", analysis=analysis, img_path=img_path)
    return render_template("analysis.html")