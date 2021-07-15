#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
# request フォームから送信した情報を扱うためのモジュール
# redirect  ページの移動
# url_for アドレス遷移
from flask import Flask, request, redirect, url_for
# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello, world'

if __name__ == '__main__':
    app.run()# -*- coding: utf-8 -*-
from flask import Flask


# 画像のアップロード先のディレクトリ
UPLOAD_FOLDER = './static/json'
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['json'])

app = Flask(__name__,static_folder='static')


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if __name__ == '__main__':
    app.run(port=8080)

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# ファイルを受け取る方法の指定
@app.route('/', methods=['GET', 'POST'])
def uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        # データの取り出し
        file = request.files['file']
        # ファイル名がなかった時の処理
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        # ファイルのチェック
        if file and allwed_file(file.filename):
            # 危険な文字を削除（サニタイズ処理）
            filename = secure_filename(file.filename)
            # ファイルの保存
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # アップロード後のページに転送
            return redirect(url_for('static', filename='index.html',json = filename[0:filename.rfind('.')]))

    return '''
    <!doctype html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title>
                SquareDrop JSON アップロード
            </title>
        </head>
        <body>
            <h1>
                SquareDrop JSON アップロード
            </h1>
            <form method = post enctype = multipart/form-data>
            <p><input type=file name = file>
            <input type = submit value = Upload>
            </form>
        </body>
    '''
