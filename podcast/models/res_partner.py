from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Podcast Contributor'

    channel_id = fields.Many2one('podcast.channel', string='Channel', ondelete='set null')
    host = fields.Boolean(string='Is Host', default=False)
