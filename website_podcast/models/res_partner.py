from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Podcast Contributor"

    channel_id = fields.Many2one(
        "website_podcast_channel", string="Channel", ondelete="set null"
    )
    host = fields.Boolean(string="Is Host", default=False)
