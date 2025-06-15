/** @odoo-module **/

import {Component, useState, onMounted} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import { rpc } from "@web/core/network/rpc";
import {registry} from '@web/core/registry';
import {PodcastList} from './podcast_list';

const {DateTime} = luxon;

export class PodcastContainer extends Component {
    static components = {
        PodcastList,
    }

    static template = 'website_podcast.podcastContainer';

    setup() {
        this.orm = useService('orm');
        this.state = useState({
            podcasts: [],
            currentChannel: null,
            query: '',
            hasMore: true,
            hasPrev: false,
            page: 1,
        });

        onMounted(async () => {
            await this.fetchData(this.getUrlSearchParameters())
        });
    }

    async fetchPodcasts(params) {
        const result = await rpc('/get-podcasts', params);
        result.episodes?.forEach((item) => {
            const rawDate = item.create_date;
            item.create_date = DateTime.fromISO(new Date(rawDate).toISOString(), {
                outputCalendar: 'persian',
            }).toLocaleString(DateTime.DATE_MED);
        });

        this.state.hasMore = result.has_more;
        this.state.hasPrev = result.has_prev;
        return result.episodes || [];
    }

    paramBuilder(params) {
        const prevParam = this.getUrlSearchParameters()
        prevParam.page = params.channelId ? 1 : prevParam.page;
        return Object.assign(prevParam, params);
    }

    getCurrentUrl() {
        return new URL(window.location.href);
    }

    addUrlSearchParameter(params) {
        const url = this.getCurrentUrl();
        for (let key in params) {
            if (key === 'page') {
                if (!params[key]) {
                    params[key] = 1
                }
            }
            url.searchParams.set(key, params[key]);
        }
        window.history.pushState(null, '', url.toString());
    }

    async fetchData(params) {
        const result = await rpc('/get-podcasts', params)
        result.episodes?.map(function (item) {
            const rawDate = item.create_date;
            item.create_date = DateTime.fromISO(new Date(rawDate).toISOString(), {outputCalendar: 'persian'}).toLocaleString(DateTime.DATE_MED)
        })
        this.state.query = params.query
        this.state.hasMore = result.has_more;
        this.state.currentChannel = Number(params.channelId);
        this.state.podcasts = result.episodes;
    }

    async fetchAndUpdate(params) {
        const newParams = this.paramBuilder(params);
        this.addUrlSearchParameter(newParams);
        await this.fetchData(newParams)
    }

    getUrlSearchParameters() {
        const url = new URL(window.location.href);
        return Object.fromEntries(url.searchParams.entries());
    }

    updateUrlSearchParameters(params) {
        const url = new URL(window.location.href);
        for (const key in params) {
            if (params[key]) {
                url.searchParams.set(key, params[key]);
            } else {
                url.searchParams.delete(key);
            }
        }
        window.history.pushState(null, '', url.toString());
    }

    async handleSearch() {
        const query = document.querySelector('#podcast_name_input').value;
        this.state.query = query;
        await this.fetchAndUpdate({query})
    }

    async handleChannelSelect(e) {
        const el = e.currentTarget;
        const channelId = el.dataset?.channelId;
        this.state.currentChannel = channelId;
        await this.fetchAndUpdate({channelId})
    }

    async removeSearchQuery() {
        const query = this.state.query.replaceAll('\n', '').trim()
        const url = this.getCurrentUrl();
        url.searchParams.delete('query', query)
        window.history.pushState(null, '', url.toString())
        await this.fetchAndUpdate(this.getUrlSearchParameters())
    }
}

registry.category('public_components').add('website_podcast.podcastContainer', PodcastContainer);
