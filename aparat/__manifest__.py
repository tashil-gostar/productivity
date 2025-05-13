{
    'name': 'Aparat for Odoo',
    'category': 'Productivity',
    'summary': 'Free & Open Source Aparat.com Integration for Odoo - Embed Persian Videos',
    'description': """

                                                             Free Aparat Video Integration for Odoo - Persian Video Content Made Easy

                                                             This open source module provides seamless integration between Odoo and Aparat.com (آپارات), Iran's leading video sharing platform. Easily embed and manage Aparat videos directly within your Odoo website.

                                                             🎬 Key Features:

    • Free & Open Source:
      - 100% free to use
      - AGPL-3 licensed
      - Community-driven development

    • Aparat Integration:
      - Simple video embedding with Aparat URLs
      - Supports all Aparat video formats
      - Maintains original video quality

    • Easy to Use:
      - Insert videos in blog posts/products/pages
      - Responsive video player
      - Video preview in backend

    💡 Perfect For:
    - Iranian businesses using Aparat
    - Persian content creators
    - Educational institutions
    - Non-profit organizations

    📌 Requirements:
    - Odoo 18.0
    - web_editor module

    👥 Community Supported:
    - Maintained by Tashilgostar
    - Contributions welcome
    - Free community support
    """,
    'author': 'Tashilgostar',
    'website': 'https://tashilgostar.com',
    'support': 'support@tashilgostar.com',
    'version': '18.0.1.0.0',
    'depends': [
        'html_editor',
    ],
    'images': [
        'static/description/banner.gif',
    ],
    'assets': {
        'web_editor.assets_media_dialog': [
            'aparat/static/src/components/**/*',
        ],
        'web.assets_backend': [
            'aparat/static/src/scss/aparat_iframe_preview.scss',
        ],
        'web._assets_helpers': [
            'aparat/static/src/scss/style.scss',
        ],
    },
    'auto_install': True,
    'license': 'AGPL-3',
}
