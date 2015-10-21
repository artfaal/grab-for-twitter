# -*- coding: utf-8 -*-

import sys
import vk_api
import tweepy
import config

# Trick for normal unicode symbols
reload(sys)
sys.setdefaultencoding("utf-8")

# TEMPORATY LIST OF GROUP
GROUP_ID = '-56333679'


def auth_vk():
    vk = vk_api.VkApi(config.LOGIN_VK, config.PASS_VK)
    try:
        vk.authorization()
    except vk_api.AuthorizationError as error_msg:
        print error_msg
        return
    return vk


def auth_twitter():
    auth = tweepy.OAuthHandler(config.TWIKEY, config.TWISECRET)
    auth.secure = True
    auth.set_access_token(config.TWITOKEN, config.TWITOKENSECRET)
    api = tweepy.API(auth)
    return api


class GetVk(object):
    """
    Список методов VK: https://vk.com/dev/methods

    Атрибуты:
    owner_id: идентификатор пользователя или сообщества
    count: количество записей, которое необходимо получить (но не более 100)
    offset: смещение, необходимое для выборки определенного подмножества записей
    """
    def __init__(self, owner_id, count, offset):
        self.owner_id = owner_id
        self.count = count
        self.offset = offset

    def get_raw_post(self):
        response = auth_vk().method('wall.get',
                                    {'owner_id': self.owner_id,
                                     'count': self.count,
                                     'offset': self.offset})
        return response

    def get_img(self):
        raw = self.get_raw_post()
        raw_attachments = raw['items'][0]['attachments']
        if len(raw_attachments) > 1:
            for i in raw_attachments:
                print i['photo']['photo_2560']
        else:
            print raw_attachments[0]['photo']['photo_2560']


if __name__ == '__main__':
    # auth_vk()
    # auth_twitter()
    get = GetVk(owner_id=GROUP_ID, count=1, offset=4)
    # print get.get_raw_post()
    get.get_img()
