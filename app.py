# -*- coding: utf-8 -*-

import sys
import vk_api
import tweepy
import config
import json

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
        # return json.dumps(response, indent=4, ensure_ascii=False,
                          # separators=(',', ': '))
        return response

    def pretty_raw_post(self):
        return json.dumps(self.get_raw_post(), indent=4, ensure_ascii=False,
                          separators=(',', ': '))

    def best_photo_pars(self, raw):
        # Парсер на предмет нахождения фотки лучшего качества
        # + Поиск текста Оriginal специфичного для паблика
        text = raw['text']
        # Если находим текст "Original: http:" в поле text
        if text.find('Original: http:') == 0:
            begin = text.find('http:')  # Начало ссылки
            end = text.find('.jpg')+4  # Конец ссылки
            return text[begin:end]
        else:
            # Если в тексте не нашлось ссылки, работаем с миниатюрами
            # Создаем список, куда закинем все ключи миниатюр
            list_of_photo = []
            # Проходимся по всему списку
            for key, value in raw.iteritems():
                # Находим ключи фотографий
                if key.find('photo_') == 0:
                    # Добавляем цифры в конце ключа в список
                    list_of_photo.append(int(key[6:]))
            # Выявляем максимальное число и сразу преобразуем обратно
            max_size_photo_key = 'photo_'+str(max(list_of_photo))
            # Возвращаем значение ключа
            return raw[max_size_photo_key]

    def get_img(self):
        # Беря за основу get_raw_post извлекаем все картинки из поста
        # в максимальном качестве.
        # TODO Не отрабатывает посты, в которых нет картинок. Разобраться.
        raw = self.get_raw_post()
        links = []
        for item in raw['items']:
            # Проверяем, не галимый ли это репост или видео
            if 'attachments' in item:
                attachments = item['attachments']
                # Для каждой фотки отрабатывается функция
                links.append(self.best_photo_pars(attachments[0]['photo']))
            else:
                print "А тут нету фоточек"

        print 'Линки на фоточки: '+str(links)

    def get_txt(self):
        raw = self.get_raw_post()
        text = raw['items'][0]['text']
        if len(text) > 1:
            return text
        else:
            return None


if __name__ == '__main__':
    get = GetVk(owner_id=GROUP_ID, count=3, offset=2)
    # print get.pretty_raw_post()
    print get.get_img()
