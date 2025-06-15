/** @odoo-module **/

import { Component, useState, onMounted, useRef } from '@odoo/owl';
import { registry } from '@web/core/registry';

export class AudioPlayer extends Component {
    static template = 'website_podcast.audio_player'

    static props = {
        audioUrl: {type: String, required: false, default: null},
    };

    setup() {
        this.state = useState({
            audioUrl: this.props.audioUrl,
            isPlaying: false,
            playbackRate: 1,
            currentTime: 0,
            progress: 0,
            duration: 0,
        });

        this.progressBarContainer = useRef('progress-container');
        this.audio = useRef('audio');
        this.speeds = [0.5, 1, 1.5, 2];
        this.currentSpeedIndex = 1;

        onMounted(this.updateTime.bind(this));
    }
    togglePlayPause() {
        if (this.audio.el.paused) {
            this.audio.el.play();
            this.state.isPlaying = true;
        } else {
            this.audio.el.pause()
            this.state.isPlaying = false;
        }
    }

    changeSpeed() {
        this.currentSpeedIndex = (this.currentSpeedIndex + 1) % this.speeds.length;
        this.audio.el.playbackRate = this.speeds[this.currentSpeedIndex];
        this.state.playbackRate = this.speeds[this.currentSpeedIndex];
    }

    rewind() {
        this.audio.el.currentTime = Math.max(0, this.audio.el.currentTime - 15);
        this.updateProgress();
    }

    forward() {
        this.audio.el.currentTime = Math.min(this.audio.el.duration, this.audio.el.currentTime + 30);
        this.updateProgress();
    }

    seek(event) {
        const clickX = event.offsetX;
        const width = this.progressBarContainer.el.offsetWidth;
        this.audio.el.currentTime = (clickX / width) * this.audio.el.duration;
        this.updateProgress();
    }

    updateProgress() {
        this.state.progress = (this.audio.el.currentTime / this.audio.el.duration) * 100;
        this.state.currentTime = this.audio.el.currentTime;
    }

    updateTime() {
        this.state.currentTime = this.audio.el.currentTime;
        this.state.duration = this.audio.el.duration || 0;
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60).toString().padStart(2, '0');
        return `${mins}:${secs}`;
    }
}

registry.category('public_components').add('website_podcast.audio_player', AudioPlayer);
