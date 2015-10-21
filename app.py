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
    def __init__(self, owner_id, count):
        self.owner_id = owner_id
        self.count = count

    def get_full_wall(self):
        response = auth_vk().method('wall.get', {'owner_id':
                                                 self.owner_id,
                                                 'count': self.count})
        return response

    def get_img(self):
        post = self.get_full_wall()  # _       _
        return post['items'][0]['attachments'][0]['photo']['text']


if __name__ == '__main__':
    # auth_vk()
    # auth_twitter()
    get = GetVk(owner_id=GROUP_ID, count=1)
    # print get.get_full_wall()
    print get.get_img()
