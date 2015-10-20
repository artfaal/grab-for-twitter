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
    def getFullWall(self, owner_id, count):
        response = authVk().method('wall.get', {'owner_id':
                                                owner_id, 'count': count})
        return response


if __name__ == '__main__':
    # authVk()
    # authTwitter()
    get = GetVk()
    print get.getFullWall('-56333679', 1)
