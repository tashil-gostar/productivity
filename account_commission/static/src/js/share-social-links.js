/** @odoo-module **/

import { onMounted } from '@odoo/owl';
import { _t } from '@web/core/l10n/translation';

export function shareSocialLinks() {
    const shareOnTwitterButton = document.querySelector('#share-twitter-btn');
    const shareOnLinkedinButton = document.querySelector('#share-linkedin-btn');
    const url = window.location.href;
    const title = document.title;

    onMounted(() => {
        shareOnTwitterButton?.addEventListener('click', shareOnTwitter);
        shareOnLinkedinButton?.addEventListener('click', shareOnLinkedIn);
    });

    function shareOnLinkedIn() {
        const linkedinUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
        window.open(
            linkedinUrl,
            '',
            'left=0,top=0,width=650,height=420,personalbar=0,toolbar=0,scrollbars=0,resizable=0'
        );
    }

    function shareOnTwitter() {
        const message = _t("🔥 New episode released! Don't miss \"%s\"").replace("%s", title);
        const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(message)}&url=${encodeURIComponent(url)}`;
        window.open(
            twitterUrl,
            '',
            'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=350,width=600'
        );
    }
}
