import requests
import re

from odoo.exceptions import UserError
from odoo import _


class ShenotoApi:
    """
    A helper class for fetching and processing podcast data from Shenoto API.
    """

    BASE_URL = 'https://shenoto.com/service/api/mss/podcast/album/'

    @classmethod
    def fetch_episode_data(cls, episode_id):
        """
        Fetch episode data from Shenoto API.

        :param episode_id: The ID of the episode to fetch.
        :return: Parsed JSON data from the API response.
        :raises: UserError if the request fails or data is invalid.
        """
        url = f'{cls.BASE_URL}{episode_id}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            serialized_json = response.json()
            data = {
                'title': serialized_json['title'],
                'description': serialized_json['content'],
                'duration': serialized_json['duration'],
                'medias': serialized_json['medias'][0]['file'],
                'cover_url': serialized_json['asset']['children']['thumbnail']['1000'],
            }
            return data
        except requests.RequestException as e:
            raise UserError(_('Failed to fetch episode data: %s') % e)

    @classmethod
    def extract_shenoto_id(cls, url):
        """
        Extract the numeric ID from a Shenoto podcast URL.
        Handles URLs with or without http/https and www.

        :param url: The Shenoto podcast episode URL.
        :return: The numeric ID.
        """
        # Regex pattern to match the numeric ID in the Shenoto URL
        pattern = r'(?:https?://)?(?:www\.)?shenoto\.com/album/podcast/(\d+)/?'

        match = re.search(pattern, url)

        if match:
            return match.group(1)
        return None
