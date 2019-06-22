import json
from datetime import datetime

import pytz
import requests

from utils import *

utc = pytz.utc
local = pytz.timezone('Asia/Shanghai')
datefmt = '%Y-%m-%d %H:%M:%S'

def parse_response(dynamic_type, dynamic_id):
    if dynamic_type == 'h':
        api_url = 'https://api.vc.bilibili.com/link_draw/v1/doc/detail'
        params = (
            ('doc_id', dynamic_id),
        )
        response = requests.get(api_url, headers=headers, params=params)
        dynamic = response.json()

        data = dynamic['data']
        item = data['item']

        return {
            'user_name' : data['user']['name'],
            'user_avatar' : data['user']['head_url'],
            'user_url' : 'https://space.bilibili.com/{}'.format(data['user']['uid']),
            'dynamic_url' : 'https://h.bilibili.com/{}'.format(item['doc_id']),
            'publish_date' : item['upload_time'],
            'content_text' : item['description'],
            'pictures' : item['pictures'],
            'origin': {}
        }

    elif dynamic_type == 't':
        api_url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail'
        params = (
            ('dynamic_id', dynamic_id),
        )
        response = requests.get(api_url, headers=headers, params=params)
        dynamic = response.json()

        card = dynamic['data']['card']

        user_name = card['desc']['user_profile']['info']['uname']
        user_avatar = card['desc']['user_profile']['info']['face']
        user_url = 'https://space.bilibili.com/{}'.format(card['desc']['uid'])
        dynamic_url = 'https://t.bilibili.com/{}'.format(card['desc']['dynamic_id_str'])


        inner_card = json.loads(card['card'])

        if 'origin' in inner_card.keys():
            item = inner_card['item']
            publish_date = int(item['timestamp'])
            publish_date = utc.localize(datetime.utcfromtimestamp(publish_date)).astimezone(local).strftime(datefmt)
            content_text = item['content']
            pictures = []

            origin_card = json.loads(inner_card['origin'])
            origin_item = origin_card['item']
            origin_user = origin_card['user']

            origin_publish_date = int(origin_item['upload_time'])
            origin_publish_date = utc.localize(datetime.utcfromtimestamp(origin_publish_date)).astimezone(local).strftime(datefmt)

            origin = {
                'user_name': origin_user['name'],
                'user_url': 'https://space.bilibili.com/{}'.format(origin_user['uid']),
                'publish_date': origin_publish_date,
                'content_text': origin_item['description'],
                'pictures': origin_item['pictures']
            }

        else:
            item = inner_card['item']
            publish_date = int(item['upload_time'])
            publish_date = utc.localize(datetime.utcfromtimestamp(publish_date)).astimezone(local).strftime(datefmt)

            content_text = item['description']
            pictures = item['pictures']
            origin = {}

        return {
            'user_name': user_name,
            'user_avatar': user_avatar,
            'user_url': user_url,
            'dynamic_url': dynamic_url,
            'publish_date': publish_date,
            'content_text': content_text,
            'pictures': pictures,
            'origin': origin
        }
