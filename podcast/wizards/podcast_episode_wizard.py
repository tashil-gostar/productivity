import requests
import base64

from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api, _
from odoo.addons.podcast.tools.shenoto_api import ShenotoApi


class PodcastEpisodeWizard(models.TransientModel):
    _name = 'podcast.episode.wizard'
    _description = 'Create Episode from Shenoto API'

    full_url = fields.Char(string='Full Shenoto URL', required=True, readonly=False, trim=True)

    def _get_url_context(self):
        extracted_id = ShenotoApi.extract_shenoto_id(self.full_url)
        if not extracted_id:
            raise UserError(_('Something wrong while fetching the data!'))
        fetched_data = ShenotoApi.fetch_episode_data(extracted_id)
        return fetched_data

    def action_confirm(self):
        self.ensure_one()

        if not self.full_url:
            raise UserError(_('You cannot continue without filling the required field!'))

        fetched_data = self._get_url_context()

        if not fetched_data:
            raise UserError(_('Something wrong while fetching the data!'))

        image_response = requests.get(fetched_data['cover_url'], timeout=10)

        if image_response.status_code != 200:
            raise UserError(_('Something wrong while fetching the data!'))

        self.env['podcast.episode'].create({
            'title': fetched_data['title'],
            'description': fetched_data['description'],
            'duration': fetched_data['duration'],
            'image_1920': base64.b64encode(image_response.content),
            'file_url': fetched_data['medias'],
            'iframe_url': self.full_url,
        })
