import requests
import const
import json


def getStatus(id):
    status = requests.post(const.url, {'secret_key': const.order_key, 'id': id})
    return json.loads(status.text)
