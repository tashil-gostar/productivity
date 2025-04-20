from odoo import models, fields, api, _


class PodcastEpisode(models.Model):
    _name = 'podcast.episode'
    _description = 'Podcast Episode'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
    _rec_name = "title"

    channel_id = fields.Many2one('podcast.channel', string='Channel', required=True, ondelete='cascade', tracking=True)
    title = fields.Char(string='Title', required=True)
    short_description = fields.Text(string='Short Description')
    description = fields.Html(string='Description')
    active = fields.Boolean(string='Active', default=True)
    duration = fields.Integer(string='Duration', help='Total duration in seconds')
    formatted_duration = fields.Char(string='Formated Duration', compute='_compute_formatted_duration', store=True,
                                     readonly=False)
    iframe_url = fields.Char(string='Embed URL')
    external_episode_id = fields.Char(string='External Episode ID',
                                      help='This is the episode ID to fetch from the external API', )
    file_url = fields.Char(string='File URL', help='This is the file URL to fetch from the external API', tracking=True)
    color = fields.Integer('Color Index', default=0, help='Used to decorate kanban view')
    contributors = fields.Many2many('res.users', relation='podcast_contributor_rel', column1='episode_id',
                                    column2='user_id', string='Contributors', tracking=True)

    def action_visit_channel(self):
        action = self.env['ir.actions.actions']._for_xml_id('podcast.action_website_podcast_channel')
        action['context'] = {
            'search_default_published': 1,
            'default_id': self.channel_id.id
        }
        action['domain'] = [('id', '=', self.channel_id.id)]
        return action

    def action_podcast_episode_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Import from Shenoto'),
            'res_model': 'podcast.episode.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('podcast.podcast_episode_wizard_form').id,
            'target': 'new',
            'context': self.env.context,
        }

    @api.depends('duration')
    def _compute_formatted_duration(self):
        for record in self:
            seconds = record.duration or 0
            # Convert to MM:SS or HH:MM:SS
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            if hours > 0:
                record.formatted_duration = f'{hours:02}:{minutes:02}:{seconds:02}'
            else:
                record.formatted_duration = f'{minutes:02}:{seconds:02}'
