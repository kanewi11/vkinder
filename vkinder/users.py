import logging
from pathlib import Path
from typing import Union, List

import requests


class Users:
    """Retrieving information and searching for users"""
    _V = '5.131'
    _DEFAULT_USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'

    _BASE_DIR = Path(__file__).parent
    _LOGS_DIR = _BASE_DIR.joinpath('logs')

    _METHOD_URL = 'https://api.vk.com/method/'
    _GET_PHOTOS_URL = _METHOD_URL + 'photos.getAll'
    _SEARCH_USERS_URL = _METHOD_URL + 'users.search'
    _GET_USERS_URL = _METHOD_URL + 'users.get'

    def __init__(self, user_token: str):
        """Initializer class

        :param user_token: User access key
        """
        self.__token = user_token

        self._LOGS_DIR.mkdir(exist_ok=True)
        self._logger = logging.getLogger('users')
        self._logger.setLevel(logging.WARNING)
        log_filepath = self._LOGS_DIR.joinpath('users.log')
        handler = logging.FileHandler(log_filepath, mode='w')
        formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def get_user_info(self, user_id: Union[int, str]) -> Union[None, dict]:
        """ Getting information about the user

        :param user_id: id from numbers or screen name.
        :return: 'None' or user information in the dictionary
        """
        params = {
            'user_ids': user_id,
            'fields': 'sex,city,bdate'
        }

        response = self.__get_response(url=self._GET_USERS_URL, params=params)
        if response is None:
            return None
        return response[0]

    def get_users_by_criteria(self, offset: Union[int, str], count: Union[int, str], city: Union[int, str],
                              age: Union[int, str], sex: Union[int, str] = 0) -> Union[None, List[dict]]:
        """Getting a list of users by criteria

        :param offset: [int | str] - digital
        :param count: [int | str] - digital
        :param city: [int | str] - city code (digital)
        :param age: [int | str] - digital
        :param sex: [int | str] - digital (0, 1, 2)
        :return: 'None' or users
        """
        params = {
            'sort': 0,
            'offset': offset,
            'count': count,
            'city': city,
            'sex': sex,
            'age_from': age,
            'age_to': age,
            'has_photo': 1,
        }

        response = self.__get_response(url=self._SEARCH_USERS_URL, params=params)
        if response is None:
            return None

        items = response.get('items')
        return items

    def get_user_thumb_photos(self, owner_id: Union[int, str]):
        """Get the last three photos

        :param owner_id: user id (numbers only)
        :return:
        """
        params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'no_service_albums': 0,
            'count': 3,
            'rev': 1,
        }

        response = self.__get_response(url=self._GET_PHOTOS_URL, params=params)
        if response is None:
            return None

        items = response.get('items')
        return items

    def __get_response(self, url: str, params: dict) -> Union[None, Union[dict, list]]:
        """Retrieving query data with error handling

        :param url: api url
        :param params: query parameters
        :return: 'None' or dict or list
        """
        params.update({
            'access_token': self.__token,
            'v': self._V,
        })
        try:
            response = requests.get(url=url, params=params, headers=self.__headers, timeout=10)
        except TimeoutError:
            self._logger.warning(f'TimeoutError:\n{url}\n{params}')
            return None

        if response.status_code != 200:
            self._logger.warning(f'Response {response.status_code}:\n{url}\n{params}\n\n{response.text}')
            return None

        response_data = response.json()
        error = response_data.get('error')
        if error:
            self._logger.warning(f'Error:\n{url}\n{params}\n\n{error}')
            return None

        data = response_data.get('response')
        if not data:
            return None
        return data

    @property
    def __headers(self) -> dict:
        return {'User-Agent': self._DEFAULT_USERAGENT}
