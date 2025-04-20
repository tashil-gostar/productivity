{
    'name': 'Podcast',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Manage podcasts, channels, and episodes in Sazmanyar',
    'description': """
    Core module for podcast management in Sazmanyar.
    
    This module provides the data models and backend functionalities for handling podcasts. It allows users to create podcast channels, add episodes with audio files, and manage metadata such as descriptions, categories, and publication dates.
    
    Key Features:
    - Podcast channels and episode management
    - Audio link support
    - Integration with Shenoto platform (easily import your podcasts from shenoto.com by copying the episode url)
    - Episode metadata (duration, tags, release date, etc.)
    - Designed for integration with frontend modules like `website_podcast`
    """,
    'author': 'Tashilgostar',
    'website': 'https://tashilgostar.com',
    'license': 'AGPL-3',
    'depends': [
        'website',
        'mail',
    ],
    'data': [
        # Security Access Control
        'security/security.xml',
        'security/ir.model.access.csv',

        # Wizard views
        'wizards/podcast_episode_wizard.xml',

        # Views and Templates
        'views/channel_views.xml',
        'views/episode_views.xml',
        'views/link_views.xml',

        # Menu items
        'views/podcast_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'podcast/static/src/scss/podcast_styles.scss',
        ]
    },
}
