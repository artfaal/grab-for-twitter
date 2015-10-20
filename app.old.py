# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
# Trick for unicode symbols
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import vk_api
import config


def main():
    """ Пример получения последнего сообщения со стены """

    login, password = config.LOGIN_VK, config.PASS_VK
    vk = vk_api.VkApi(login, password)

    try:
        vk.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return

    response = vk.method('wall.get', {'owner_id': '-56333679',
                                      'count': 1, 'offset': 2})
    if response['items']:
        print(response['items'][0])


def twitter():


    import tweepy

    # == OAuth Authentication ==
    #
    # This mode of authentication is the new preferred way
    # of authenticating with Twitter.

    # The consumer keys can be found on your application's Details
    # page located at https://dev.twitter.com/apps (under "OAuth settings")
    consumer_key = config.TWIKEY
    consumer_secret = config.TWISECRET

    # The access tokens can be found on your applications's Details
    # page located at https://dev.twitter.com/apps (located
    # under "Your access token")
    access_token = config.TWITOKEN
    access_token_secret = config.TWITOKENSECRET

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # If the authentication was successful, you should
    # see the name of the account print out
    print(api.me().name)

    # If the application settings are set for "Read and Write" then
    # this line should tweet out the message to your account's
    # timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
    # api.update_status(status='Updating using OAuth authentication via Tweepy!')

if __name__ == '__main__':
    # main()
    twitter()