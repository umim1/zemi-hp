from flask import Flask, render_template, session, redirect, url_for
import os
import smtplib
from email.mime.text import MIMEText
from forms import Input
from dotenv import load_dotenv

#.env ファイルの環境変数を読み込む
load_dotenv()


app = Flask(__name__)

#環境変数からメール設定を読み込む
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

#セッションを使うための秘密鍵を設定
app.config["SECRET_KEY"] = os.urandom(24)

#メール送信関数（質問内容を先生に送る）
def send_mail(content, email):
    msg = MIMEText(f"【質問内容】\n{content}\n\n【送信者メールアドレス】\n{email}")
    msg["Subject"] = "ゼミ質問フォームからの質問"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    
    try:
        #Gmail の SMTP サーバーを使って送信
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # セキュアな接続を確立
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

        print("📨 メール送信成功")
    except Exception as e:
        print(f"⚠️ メール送信失敗: {e}")

#ルーティング
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    return render_template('page3.html')

#フォーム入力処理
@app.route('/input', methods = ["GET", "POST"])
def input():
    form = Input()
    
    #POSTリクエストでバリデーションOKならセッションに保存してリダイレクト
    if form.validate_on_submit():
        session["content"] = form.content.data
        session["email"] = form.email.data
        
        #先生にメールを送信
        send_mail(form.content.data, form.email.data)
        
        return redirect(url_for("output"))
    
    #GETリクエスト時、またはバリデーションエラー時
    if "content" in session:
        form.content.data = session["content"]
    if "email" in session:
        form.email.data = session["email"]
        
    return render_template("input.html", form = form)

#出力ページ(保存された情報を表示
@app.route("/output")
def output():
    return render_template("output.html")
    
if __name__ == '__main__':
    app.run(debug=True)