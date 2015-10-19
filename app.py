# -*- coding: utf-8 -*-


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

    response = vk.method('wall.get', {'owner_id':'-56333679', 'count': 1, 'offset': 2})
    if response['items']:
        print(response['items'][0])


if __name__ == '__main__':
    main()
