# -*- coding: utf-8 -*-

import sys
import vk_api
import tweepy
import config

# Trick for normal unicode symbols
reload(sys)
sys.setdefaultencoding("utf-8")


def authVk():
    vk = vk_api.VkApi(config.LOGIN_VK, config.PASS_VK)
    try:
        vk.authorization()
    except vk_api.AuthorizationError as error_msg:
        print error_msg
        return
    return vk


def authTwitter():
    auth = tweepy.OAuthHandler(config.TWIKEY, config.TWISECRET)
    auth.secure = True
    auth.set_access_token(config.TWITOKEN, config.TWITOKENSECRET)
    api = tweepy.API(auth)
    return api


class GetVk:
    def __init__(self, owner_id, count):
        self.owner_id = owner_id
        self.count = count

    def getFullWall(self):
        response = authVk().method('wall.get', {'owner_id':
                                                self.owner_id,
                                                'count': self.count})
        return response


if __name__ == '__main__':
    # authVk()
    # authTwitter()
    get = GetVk(owner_id='-56333679', count=1)
    print get.getFullWall()
