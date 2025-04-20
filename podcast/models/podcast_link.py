from odoo import models, fields


class PodcastLink(models.Model):
    _name = 'podcast.link'
    _description = 'Podcast external website Link'

    name = fields.Char(string='Name', required=True, translate=True, copy=False, help='Name of podcast website link')
    url = fields.Char(string='URL', required=True, copy=False, help='URL of podcast website link', trim=True)
    icon = fields.Image(string='Icon', help='Icon of podcast website link', required=True, copy=False, default='')
