from flask import Flask, flash, url_for, redirect, render_template, request, session
from flask_session import Session
import crypto
import io
from helpers import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db= SQL("sqlite:///crypto.db")

@app.route('/')
def index():
    try:
        username=db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]
        return render_template('index.html', username=username)
    except:
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
    mode = request.form.get("mode","known")
    encrypted = request.form.get("encrypted", "")
    key = request.form.get("key", "a")
    attempt = request.form.get("attempts")
    keylength=request.form.get("keylength")
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
        
        
        elif mode=='guess':
            keyguess=request.form.get("keyguess")
            if attempt and keylength:
                guesses=crypto.guessVigenere(encrypted, key_length=int(keylength), attempts=int(attempt))
                if keyguess:
                    plainguess=crypto.desubstitution(encrypted,keyguess)
                    return render_template('decrypt.html', plain=guesses, encrypted=encrypted, mode=mode, plainguess=plainguess, attempt=attempt, keylength=keylength, keyguess=keyguess)
                return render_template('decrypt.html', plain=guesses, encrypted=encrypted, mode=mode, attempt=attempt, keyguess=keyguess ,keylength=keylength)
            else:
                return render_template("decrypt.html", mode=mode)


    return render_template("decrypt.html", mode=mode)

@app.route("/analysis", methods=["GET","POST"])
def analysis():
    if request.method =="POST":
        encrypted=request.form.get("encrypted")
        keylength=int(request.form.get("keylength"))
        row=int(request.form.get("row"))
        try:
            row = int(row)
            if row <= 0:
                raise ValueError
        except (ValueError, TypeError):
            row = 1

        encryptedrows=crypto.splitRows(encrypted,keylength)

        analysis=crypto.frequencyAnalysisVigenere(encrypted,keylength)
        
        if row:
            img=io.BytesIO()
            crypto.histFreqAnalysis(encryptedrows[(row-1)]).savefig(img, format='png')
            img.seek(0)

            img_path = 'static/images/analysis.png'
            with open(img_path, 'wb') as f:
                f.write(img.getbuffer())


            return render_template("analysis.html", analysis=analysis, img_path=img_path, encrypted=encrypted, keylength=keylength)
        
        else:
            return render_template("analysis.html", analysis=analysis, encrypted=encrypted, keylength=keylength)
    return render_template("analysis.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        
        return redirect("/")
    else:
        return render_template("login.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 0:
            return apology("username already exists", 400)

        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        session["user_id"] = db.execute(
            "SELECT id FROM users WHERE username=?", request.form.get("username"))[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/chat", methods=["GET", "POST"])
@login_required
def search():
    myuserid=session["user_id"]
    chats=db.execute("SELECT username FROM users WHERE (id = (SELECT sender_id FROM chats WHERE receiver_id=?) OR (SELECT receiver_id FROM chats WHERE sender_id=?))", myuserid, myuserid)
    if request.method=="POST":
       user=request.form.get("user")
       useractive=request.form.get("user-active")
       if useractive:
           useractiveid=db.execute("SELECT id FROM users WHERE username = ?", useractive)[0]["id"]
           chatid=db.execute("SELECT id FROM chats WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)", useractiveid, myuserid, myuserid, useractiveid)
           return redirect(url_for("chat",chatid=chatid[0]["id"], user=useractive))
       
       elif user:
        userid=db.execute("SELECT id FROM users WHERE username = ?", user)
        if userid:
            userid=userid[0]["id"]
            chatid=db.execute("SELECT id FROM chats WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?)", userid, myuserid, myuserid, userid)
            if chatid:
                return redirect(url_for("chat",chatid=chatid[0]["id"], user=user))
            else:
                db.execute("INSERT INTO chats(sender_id,receiver_id) VALUES(?,?)", myuserid, userid)
                chatid=db.execute("SELECT id FROM chats WHERE sender_id=? AND receiver_id=?", myuserid, userid)
                return redirect(url_for("chat",chatid=chatid[0]["id"], user=user))
        else:
            return apology("user not found",400)
    else:
       return render_template("chatsearch.html",chats=chats)
   
@app.route("/chat/<chatid>", methods=["GET", "POST"])
@login_required
def chat(chatid):
    messages=db.execute("SELECT * FROM messages WHERE chat_id=?", chatid)
    user=request.args.get("user")
    if request.method=="POST":
        text=request.form.get("text")
        key=request.form.get("key")
        message_key=request.form.get("message-key")
        message_text=request.form.get("message-text")
        user=request.form.get("user")

        if message_key and message_text:
            message_id=int(request.form.get("message-id"))
            decrypted=crypto.desubstitution(message_text,message_key)
            return render_template("chat.html", chatid=chatid, messages=messages, user=user, decrypted=decrypted, messageid=message_id)


        if text and key:
            encrypted=crypto.substitution(text,key)
            sender_username=db.execute("SELECT username FROM users WHERE id=? ", session["user_id"])[0]["username"]
            db.execute("INSERT INTO messages (chat_id,sender_id,message,datetime,sender_username) VALUES(?,?,?,datetime(),?)", chatid, session["user_id"], encrypted,sender_username)
            messages=db.execute("SELECT * FROM messages WHERE chat_id=?", chatid)
            return render_template("chat.html", chatid=chatid, messages=messages, user=user)
        
        else:
            return render_template("chat.html", chatid=chatid, messages=messages, user=user)

    else:
        return render_template("chat.html", chatid=chatid,messages=messages, user=user)


'''CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE chats(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
sender_id INTEGER NOT NULL,
receiver_id INTEGER NOT NULL,
FOREIGN KEY(sender_id) REFERENCES users(id),
FOREIGN KEY(receiver_id) REFERENCES users(id));
CREATE TABLE messages(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
chat_id INTEGER NOT NULL,
sender_id INTEGER NOT NULL,
message TEXT NOT NULL,
datetime NUMERIC,
FOREIGN KEY(chat_id) REFERENCES chats(id),
FOREIGN KEY(sender_id) REFERENCES users(id)
);'''