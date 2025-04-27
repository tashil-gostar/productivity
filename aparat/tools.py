# -*- encoding: utf-8 -*-

import json
import re

import requests

from odoo import _
from odoo.addons.web_editor import tools
from odoo.tools import image_process

# To detect if we have a valid URL or not
valid_url_regex = r'^(http://|https://|//)[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(/.*)?$'

# Regex for few of the widely used video hosting services
player_regexes = {
    'aparat': r'^(?:(?:https?:)?\/\/)?(?:www\.)?(?:aparat\.com\/(?:v\/))((\w|-){5,7})(?:\S+)?$',
    'aparat_iframe': r'^(?:(?:https?:)?\/\/)?(?:www\.)?aparat\.com\/video/video/embed/videohash/((\w|-){5,7})/vt/frame'
}

get_video_thumbnail_super = tools.get_video_thumbnail
get_video_source_data_super = tools.get_video_source_data
get_video_url_data_super = tools.get_video_url_data
get_video_embed_code_super = tools.get_video_embed_code


def get_video_source_data(video_url):
    """ Computes the valid source, document ID and regex match from given URL
        (or None in case of invalid URL).
    """
    if not video_url:
        return None

    aparat_match = re.search(player_regexes['aparat'], video_url)
    if aparat_match:
        return 'aparat', aparat_match.group(1), aparat_match

    aparat_iframe_match = re.search(player_regexes['aparat_iframe'], video_url)
    if aparat_iframe_match:
        return 'aparat', aparat_iframe_match.group(1), aparat_iframe_match

    return get_video_source_data_super(video_url)


def get_video_url_data(video_url, autoplay=False, loop=False, hide_controls=False, hide_fullscreen=False,
                       hide_yt_logo=False, hide_dm_logo=False, hide_dm_share=False):
    """ Computes the platform name and embed_url from given URL
        (or error message in case of invalid URL).
    """
    source = get_video_source_data(video_url)
    if source is None:
        return {'error': True, 'message': _('The provided url is invalid')}

    platform, video_id, platform_match = source
    if platform == 'aparat':
        return {'platform': platform, 'embed_url': f'//www.aparat.com/video/video/embed/videohash/{video_id}/vt/frame'}

    return get_video_url_data_super(video_url, autoplay, loop, hide_controls, hide_fullscreen, hide_yt_logo,
                                    hide_dm_logo, hide_dm_share)


def get_video_thumbnail(video_url):
    source = get_video_source_data(video_url)
    if source is None:
        return None

    response, poster = None, None
    platform, video_id = source[:2]
    if platform == 'aparat':
        content = requests.get(f'https://www.aparat.com/etc/api/video/videohash/{video_id}/',
                               timeout=10).content.decode('UTF-8')
        response = requests.get(json.loads(content)['video']['big_poster'], timeout=10)

    if response:
        return image_process(response.content)
    return get_video_thumbnail_super(video_url)


def get_video_embed_code(video_url, aparat=False):
    if not video_url:
        return False

    aparat_match = re.search(player_regexes['aparat_iframe'], video_url)
    if aparat_match:
        embed_url = aparat_match.group()
        return '<iframe class="embed-responsive-item" src="%s" allowFullScreen="true" frameborder="0"></iframe>' % embed_url
    elif aparat:
        return False
    return get_video_embed_code_super(video_url)


tools.get_video_thumbnail = get_video_thumbnail
tools.get_video_source_data = get_video_source_data
tools.get_video_url_data = get_video_url_data
tools.get_video_embed_code = get_video_embed_code
