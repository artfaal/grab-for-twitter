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
        # Здесь мы получаем RAW поста по заданным параметрам
        response = auth_vk().method('wall.get',
                                    {'owner_id': self.owner_id,
                                     'count': self.count,
                                     'offset': self.offset})
        return response

    def best_photo_pars(self):
        # Парсер на предмет нахождения фотки лучшего качества
        pass

    def get_img(self):
        # Беря за основу get_raw_post извлекаем все картинки из поста
        # в максимальном качестве.
        # TODO photo_2560 Не всегда работает. Надо
        # запилить функцию, которая парсит это дело.
        # Плюс попадается текст Original и ссылка внутри. Надо это
        # тоже как-то отслеживать.
        raw = self.get_raw_post()
        attachments = raw['items'][0]['attachments']
        links = []
        if len(attachments) > 1:
            for i in attachments:
                try:
                    links.append(i['photo']['photo_2560'])
                except KeyError, e:
                    print 'Несуществующий ключ: %s' % str(e)
                    sys.exit(1)
        else:
            try:
                links.append(attachments[0]['photo']['photo_2560'])
            except KeyError, e:
                print 'Несуществующий ключ: %s' % str(e)
                sys.exit(1)

        return links

    def get_txt(self):
        raw = self.get_raw_post()
        text = raw['items'][0]['text']
        if len(text) > 1:
            return text
        else:
            return None


if __name__ == '__main__':
    get = GetVk(owner_id=GROUP_ID, count=1, offset=1)
    # print get.get_raw_post()
    print get.get_img()

# TODO json.dumps(response, indent=4, ensure_ascii=False,
#                         separators=(',', ': '))