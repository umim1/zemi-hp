from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email

# 入力クラス
class Input(FlaskForm):
    content = StringField("記入欄 :", validators=[DataRequired(message='必須入力です')])
    email = EmailField("メールアドレス :", validators=[DataRequired(message='メールアドレスを入力してください'), Email(message='正しいメールアドレスの形式ではありません')])
    submit = SubmitField("送信")
