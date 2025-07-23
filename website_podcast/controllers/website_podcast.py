import math

from odoo import _, http
from odoo.http import request
from werkzeug.exceptions import NotFound


class WebsitePodcast(http.Controller):
    @http.route(
        [
            "/podcasts",
            "/podcasts/page/<int:page>",
            '/podcasts/<model("website.podcast.channel"):channel>',
            '/podcasts/<model("website.podcast.channel"):channel>/page/<int:page>',
        ],
        type="http",
        auth="public",
        website=True,
        csrf=False,
    )
    def list_channels(self, channel=None, page=1, **kwargs):
        channels = request.env["website.podcast.channel"].search([
            ('is_published', '=', True)
        ])
        not_empty_channels = channels.filtered(
            lambda c: c.episodes.filtered(lambda e: e.is_published)
        )

        has_episodes_channels = []
        for ch in not_empty_channels:
            has_episodes_channels.append({
                'id': ch.id,
                'title': ch.title,
            })

        links = request.env["website.podcast.link"].search_read(
            [], fields=["name", "url"]
        )
        for link in links:
            link["icon_url"] = (
                f"/web/image/website.podcast.link/{link['id']}/icon"
                if link.get("id")
                else "/web/static/img/placeholder.png"
            )

        response_data = {
            "channels": has_episodes_channels,
            "links": links,
            "active_channel_id": channel["id"] if channel else None,
        }

        return request.render("website_podcast.podcasts_home", response_data)

    @http.route(
        '/podcast/<model("website.podcast.channel"):channel>/episode/<model("website.podcast.episode"):episode>',
        type="http",
        auth="public",
        website=True,
    )
    def show_episode(self, channel, episode, **kwargs):
        episode = (
            request.env["website.podcast.episode"].sudo().browse(episode.id).exists()
        )
        channels = request.env["website.podcast.channel"].search([
            ('is_published', '=', True)
        ])
        not_empty_channels = channels.filtered(
            lambda c: c.episodes.filtered(lambda e: e.is_published)
        )

        has_episodes_channels = []
        for ch in not_empty_channels:
            has_episodes_channels.append({
                'id': ch.id,
                'title': ch.title,
            })
        episode_ids = (
            request.env["website.podcast.episode"]
            .search([("channel_id", "=", channel["id"])], order="id asc")
            .ids
        )

        try:
            target_index = episode_ids.index(episode.id)
        except ValueError:
            return NotFound()

        previous_id = episode_ids[target_index - 1] if target_index > 0 else None
        next_id = (
            episode_ids[target_index + 1]
            if target_index < len(episode_ids) - 1
            else None
        )

        return request.render(
            "website_podcast.podcasts_episode",
            {
                "active_channel_id": channel["id"],
                "channels": has_episodes_channels,
                "channel": channel,
                "episode": episode,
                "episode_of": target_index + 1,
                "next_episode": next_id,
                "previous_episode": previous_id,
            },
        )

    @http.route("/get-podcasts", type="json", auth="public", website=True)
    def handle_podcasts(self, **kwargs):
        try:
            search_query = kwargs.get("query", None)
            channel_id = int(kwargs.get("channelId") or 0)
            page = max(int(kwargs.get("page") or 1), 1)
            limit = 10
            offset = (page - 1) * limit

            domain = [("is_published", "=", True), ("channel_id.is_published", "=", True)]
            if search_query:
                domain.append('|')
                domain.append(("title", "ilike", search_query))
                domain.append('|')
                domain.append(('short_description', 'ilike', search_query))
                domain.append(('description', 'ilike', search_query))
            if channel_id:
                domain.append(("channel_id", "=", channel_id))

            episodes = (
                request.env["website.podcast.episode"]
                .sudo()
                .search(domain, order="id desc", limit=limit, offset=offset)
            )
            total_episodes = (
                request.env["website.podcast.episode"].sudo().search_count(domain)
            )
            has_more = offset + limit < total_episodes
            episodes_data = [
                {
                    "id": episode.id,
                    "title": episode.title,
                    "channel_id": {
                        "id": episode.channel_id.id,
                        "title": episode.channel_id.title,
                        "seo_name": episode.channel_id.seo_name,
                    },
                    "description": episode.description,
                    "create_date": episode.create_date.isoformat(),
                    "image_256": episode.image_256,
                    "short_description": episode.short_description,
                    "contributors": [
                        {"id": user.id, "name": user.name}
                        for user in episode.contributors
                    ],
                    "seo_name": episode.seo_name,
                }
                for episode in episodes
            ]

            return {
                "episodes": episodes_data,
                "has_more": has_more,
                "pages": math.ceil(total_episodes / limit),
                "current_page": page,
            }
        except ValueError:
            error_message = _("Invalid input parameters! Please provide a valid input.")
            return {"error_message": error_message}
