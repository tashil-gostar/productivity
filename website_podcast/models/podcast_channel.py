from odoo import api, fields, models


class PodcastChannel(models.Model):
    _name = "website.podcast.channel"
    _description = "Podcast Channel"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
        "image.mixin",
        "website.seo.metadata",
        "website.published.multi.mixin",
    ]
    _rec_name = "title"

    title = fields.Char(string="Title", required=True)
    short_description = fields.Text(string="Short Description")
    description = fields.Html(string="Description")
    duration = fields.Integer(
        string="Total Duration (minutes)", compute="_compute_total_duration", store=True
    )
    formatted_duration = fields.Char(
        string="Duration",
        compute="_compute_formatted_duration",
        store=True,
        readonly=False,
    )
    listen_without_login = fields.Boolean(string="Listen Without Login", default=False)
    contributors = fields.One2many("res.partner", "channel_id", string="Contributors")
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(
        "Color Index", default=0, help="Used to decorate kanban view"
    )
    episodes = fields.One2many(
        "website.podcast.episode", "channel_id", string="Episodes"
    )
    total_episodes = fields.Integer(compute="_compute_episodes_length", store=False)
    links_length = fields.Integer(
        string="Links Length", compute="_compute_links_length", store=False, copy=False
    )

    @api.depends("episodes")
    def _compute_episodes_length(self):
        for record in self:
            record.total_episodes = len(record.episodes)

    @api.depends("episodes")
    def _compute_total_duration(self):
        for record in self:
            record.duration = sum(record.episodes.mapped("duration"))

    def _compute_links_length(self):
        links_length = self.env["website.podcast.link"].search_count([])
        for record in self:
            record.links_length = links_length

    def action_view_episodes(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "website_podcast.website_podcast_episode_action"
        )
        action["context"] = {
            "search_default_published": 1,
            "default_channel_id": self.id,
        }
        action["domain"] = [("channel_id", "=", self.id)]
        return action

    @api.depends("duration")
    def _compute_formatted_duration(self):
        for record in self:
            seconds = record.duration or 0
            # Convert to MM:SS or HH:MM:SS
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            if hours > 0:
                record.formatted_duration = f"{hours:02}:{minutes:02}:{seconds:02}"
            else:
                record.formatted_duration = f"{minutes:02}:{seconds:02}"

    def _compute_website_url(self):
        for record in self:
            record.website_url = f"/podcasts/{record.id}"
