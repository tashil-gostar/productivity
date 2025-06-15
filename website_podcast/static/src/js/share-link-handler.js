/** @odoo-module **/

import { Component } from '@odoo/owl';
import { useService } from '@web/core/utils/hooks';
import { shareSocialLinks } from './share-social-links'
import { _t } from '@web/core/l10n/translation';
import { registry } from '@web/core/registry';

class ShareLinkHandler extends Component {
    static template = 'website_podcast.copy_link_modal';

    setup() {
        this.notification = useService('notification');
        shareSocialLinks()
    }

    show_dialog() {
        window.navigator.clipboard.writeText(
            window.location.href,
        );
        this.notification.add(_t('Copied'), {type: 'success', title: _t('Copy URL to Clipboard')});
    }
}

registry.category('public_components').add('website_podcast.copy_link_modal', ShareLinkHandler);
