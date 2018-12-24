from flask import Flask, render_template, redirect, request, send_file, make_response, jsonify
from uuid import uuid4
from baiduAi import audio2text, text2audio, my_nlp
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('web.html')


@app.route('/toy_uploader', methods=['GET', 'POST'])
def toy_uploader():
    # response = make_response()
    # response.headers['Access-Control-Allow-Origin'] = '*'
    import os
    # 因为浏览器传来的音频是没有名字的;,所以给个目录命名一下
    file_path = os.path.join('audios', f'{uuid4()}.wav')
    request.files['record'].save(file_path)
    Q = audio2text(file_path)
    A = my_nlp(Q)
    content = text2audio(A)
    return jsonify({'content': content, 'answer': A})


@app.route('/get_audio/<filename>', methods=['GET', 'POST'])
def get_audio(filename):
    new_file = os.path.join('audios', filename)
    print(new_file)
    return send_file(new_file)


if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
