/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { X2ManyMediaViewer } from "@html_editor/others/x2many_media_viewer";
import { getVideoUrl } from "@aparat/utils/url";


patch(X2ManyMediaViewer.prototype, {
    onVideoSave(videoInfo) {
        const url = getVideoUrl(videoInfo[0].platform, videoInfo[0].videoId, videoInfo[0].params);
        const videoList = this.props.record.data[this.props.name];
        videoList.addNewRecord({ position: "bottom" }).then((record) => {
            record.update({ name: videoInfo[0].platform + " - [Video]", video_url: url.href });
        });
    }
})
