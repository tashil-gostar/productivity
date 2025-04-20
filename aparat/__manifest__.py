{
    'name': 'Aparat',
    'category': 'Productivity',
    'summary': 'Aparat compatibility with odoo',
    'author': 'Tashilgostar',
    'website': 'https://tashilgostar.com',
    'support': 'support@tashilgostar.com',
    'live_test_url': 'https://sazmanyar.tashilgostar.com',
    'version': '18.0.1.0.0',
    'description': '''
Odoo Aparat module.
===================

This module provides a proper Aparat for Odoo.
    ''',
    'depends': [
        'html_editor',
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
