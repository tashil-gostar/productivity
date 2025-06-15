{
    "name": "Podcast Manager - Professional Podcast Management for Odoo",
    "version": "18.0.2.0.0",
    "category": "Marketing/Podcast",
    "summary": "Comprehensive Podcast Management System with Shenoto Integration",
    "description": """
                   
                       Professional Podcast Management Solution for Odoo - Create, Manage and Publish Podcasts with Ease

                                          Elevate your podcasting workflow with this powerful Odoo module designed for podcast creators, media companies, and content marketers. The Podcast Manager provides everything you need to manage your podcast channels and episodes efficiently.

                                          Key Features:
                                          • Complete Podcast Ecosystem with channel and episode management
                                          • Advanced audio management with support for external links
                                          • Seamless Shenoto.com integration - import episodes with just a URL
                                          • Professional publishing tools with scheduling capabilities
                                          • Optimized for Persian podcasters and RTL content

                                          Special Shenoto Integration:
                                          - Direct import from shenoto.com by pasting episode URLs
                                          - Preserves all Shenoto metadata and audio quality
                                          - Perfect for Persian podcasters using Shenoto platform
                                          - Sync episode details without leaving Odoo

                                          The module maintains all standard podcast management features while offering special integration capabilities with Shenoto, Iran's leading podcast platform.
                                          """,
    "author": "Tashilgostar",
    "website": "https://tashilgostar.com",
    "support": "support@tashilgostar.com",
    "license": "AGPL-3",
    "depends": ["website", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "wizards/podcast_episode_wizard.xml",
        "views/channel_views.xml",
        "views/episode_views.xml",
        "views/link_views.xml",
        "views/website_podcast_menus.xml",
        # Website templates
        "views/website_podcast_templates_homepage.xml",
        "views/website_podcast_templates_episodepage.xml",
    ],
    "assets": {
        "web.assets_backend": ["website_podcast/static/src/scss/podcast_styles.scss"],
        "web.assets_frontend": [
            "website_podcast/static/src/js/*",
            "website_podcast/static/src/scss/*",
            "website_podcast/static/src/xml/*",
            "website_podcast/static/src/components/**/*",
        ],
    },
    "application": True,
    "installable": True,
    "price": 4.99
}
