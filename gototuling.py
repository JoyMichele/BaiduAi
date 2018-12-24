import requests
# 图灵人工智能档案 : https://www.kancloud.cn/turing/www-tuling123-com/718227

url = 'http://openapi.tuling123.com/openapi/api/v2'

data_dict = {
    "reqType": 0,
    "perception": {
        "inputText": {
            "text": "意大利"
        },
    },
    "userInfo": {
        "apiKey": "32d5105c3860458e8ce6f3eace905f42",
        "userId": "01"
    }
}


def tuling(test, uid):
    # 填入要对话的字符串
    data_dict['perception']["inputText"]["text"] = test
    # 用户id
    data_dict['userInfo']["userId"] = uid
    # 发送请求给图灵机器人
    res = requests.post(url, json=data_dict)
    result = res.json()
    return result.get('results')[0]['values']['text']
