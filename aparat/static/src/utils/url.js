import { getVideoUrl as _getVideoUrl } from '@html_editor/utils/url';

export function getVideoUrl(platform, videoId, params) {
    if (platform === "aparat") {
        const url = new URL(`https://www.aparat.com/video/video/embed/videohash/${videoId}/vt/frame`);
        url.search = new URLSearchParams(params);
        return url
    }
    return _getVideoUrl(...arguments);
}
