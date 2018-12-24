import os
from aip import AipSpeech, AipNlp
from uuid import uuid4

APP_ID = '15217111'
API_KEY = 'jE38mGiHGGe8LnmK2YdbGGoX'
SECRET_KEY = 'KaoFdHZoaUWQsmpRgIEgxIGhdkDbW2V4'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
nlp_client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


# 读取文件
def get_file_content(filePath):
    os.system(f"ffmpeg -y -i {filePath} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm")
    with open(f'{filePath}.pcm', 'rb')as fp:
        return fp.read()


def audio2text(filename):
    # 识别本地文件
    print(filename)
    res = client.asr(get_file_content(filename), 'pcm', 16000, {
        'dev_pid': 1536,
    })

    return res.get("result")[0]


def text2audio(A):
    # 文本转音频
    result = client.synthesis(A, 'zh', 1, {
        "per": 4,
        "pit": 8,
        "spd": 4,
        'vol': 5,
    })
    if not isinstance(result, dict):
        filename = f"{uuid4()}.mp3"
        filepath = os.path.join("audios", filename)
        with open(filepath, 'wb') as f:
            f.write(result)

        return filename


def my_nlp(Q):
    if nlp_client.simnet(Q, '你叫什么名字').get('score') >= 0.7:
        A = '我的名字是源氏'

    else:
        import gototuling
        A = gototuling.tuling(Q, '001')
    return A
