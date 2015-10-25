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


class HandlerRawPost(object):
    """Обработчик полученных из ВК постов. Разделено на классы,
    что бы исключить множесвенные запросы."""
    def __init__(self, raw):
        self.raw = raw

    def best_photo_pars(self, input):
        # Парсер на предмет нахождения фотки лучшего качества
        # + Поиск текста Оriginal специфичного для паблика
        text = input['text']
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
            for key, value in input.iteritems():
                # Находим ключи фотографий
                if key.find('photo_') == 0:
                    # Добавляем цифры в конце ключа в список
                    list_of_photo.append(int(key[6:]))
            # Выявляем максимальное число и сразу преобразуем обратно
            max_size_photo_key = 'photo_'+str(max(list_of_photo))
            # Возвращаем значение ключа
            return input[max_size_photo_key]

    def get_img(self):
        # Беря за основу get_raw_post извлекаем все картинки из поста
        # в максимальном качестве.
        raw = self.raw
        links = []
        for item in raw['items']:
            # Проверяем, не галимый ли это репост или видео
            if 'attachments' in item and 'photo' in item['attachments'][0]:
                attachments = item['attachments']
                # Проверяем длинну листа фотографий и пцскаем по ним цикл
                i = 0
                while i < len(attachments):
                    links.append(self.best_photo_pars(attachments[i]['photo']))
                    i += 1
            else:
                pass
        return links

    def get_txt(self):
        # Если длинна текста больше  1, то отправляет значение
        raw = self.raw
        text = raw['items'][0]['text']
        if len(text) > 1:
            return text
        else:
            pass


# TODO Косяк с длинной сообщения. Показывает больше чем есть.
def check_msg_len(message):
    # Функция для проверки длинны сообщения перед отправкой.
    if len(message) <= 140:
        return message
    else:
        # TODO Захардкодил. Пока не работает.
        # print 'Too long message, "%s" - too much \n' % len(message), message
        # sys.exit(1)
        return message


def prepare_tweet():
    # Вытаскиваем необходимые посты, засовывая raw в get
    get = GetVk(owner_id=GROUP_ID, count=1, offset=4).get_raw_post()
    # Опеределяем переменну в классе HandlerRawPost
    handler = HandlerRawPost(get)
    # Вытаксиваем текст
    txt = handler.get_txt()
    # Вытаскиваем картинки
    imgs = handler.get_img()
    # Если нету текста в сообщении, то просто пропускаем.
    if txt is not None:
        result = str(txt) + '\n' + str('\n'.join(imgs))
        return check_msg_len(result)
    else:
        result = str(' \\n'.join(imgs))
        return check_msg_len(result)


def send_tweet():
    # auth_twitter().update_status(status=prepare_tweet())
    print ' Отправлено: ' + '\n' + prepare_tweet()


if __name__ == '__main__':
    send_tweet()
