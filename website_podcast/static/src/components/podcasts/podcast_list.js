/** @odoo-module **/

import {Component} from '@odoo/owl';
import {registry} from '@web/core/registry';

export class PodcastList extends Component {
    static template = 'website_podcast.podcastList'

    async removeSearchQuery() {
        await this.props.removeSearchQuery();
    }
}

registry.category('public_components').add('website_podcast.podcastList', PodcastList);
