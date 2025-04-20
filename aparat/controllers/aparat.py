import werkzeug.exceptions
import werkzeug.urls
import werkzeug.wrappers

from odoo.http import request, route

from odoo.addons.html_editor.controllers.main import HTML_Editor
from odoo.addons.aparat.tools import get_video_url_data


class HTML_Editor_Aparat(HTML_Editor):
    @route()
    def video_url_data(self, video_url, autoplay=False, loop=False,
                       hide_controls=False, hide_fullscreen=False,
                       hide_dm_logo=False, hide_dm_share=False):
        if not request.env.user._is_internal():
            raise werkzeug.exceptions.Forbidden()
        return get_video_url_data(
            video_url, autoplay=autoplay, loop=loop,
            hide_controls=hide_controls, hide_fullscreen=hide_fullscreen,
            hide_dm_logo=hide_dm_logo, hide_dm_share=hide_dm_share
        )
