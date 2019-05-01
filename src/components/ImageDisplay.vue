<template>
<div id="wrapper" style="color:darkblue; background-color: powderblue;">
  <body style="color:darkblue; background-color: powderblue;">
  <div id="app">
<h1> What a Masterpiece!</h1>
    <div id="imgBody">
<img v-if="imageData" class="image-container"
               :src="imageData"
               alt="" />
      </div>

<button v-if="displayButton" class="btn"
                @click="clearCanvas">
          <span class="clear"></span>
          <span>Clear</span>
        </button>
<button v-if="displayButton" class="btn"
                @click="displayImage">
          <span class="display"></span>
          <span>Display</span>
        </button>

<button class="btn"
           @click="playMusic">
          <span class="play"></span>
          <span>Play</span>
        </button>
<div class="overlay"
         v-if="showWaitModal">
      <div class="half-circle-spinner">
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
      </div>
      <div class="content">
        {{ modalContent }}
      </div>
    </div>

</div>
</body>
  </div>
</template>
<script>

import DrawingBoard from "./DrawingBoard.vue";
import ImageItem from "./ImageItem.vue";
import axios from "axios";
import Vue from "vue";
import VueSwal from "vue-swal";
import ToggleButton from "vue-js-toggle-button";
import * as mm from '@magenta/music';
import AudioVisual from 'vue-audio-visual'

Vue.use(AudioVisual)

Vue.use(VueSwal);
Vue.use(ToggleButton);

const axiosStyle =
  process.env.NODE_ENV === "development"
    ? axios.create({ baseURL: "http://localhost:5002" })
    : axios.create({ baseURL: "https://dip.imfing.com/style" });


export default {
  name: "ImageDisplay",

  data() {
    return {
      msg: "Welcome",
      imageData: "",
      modalContent: "Waiting for a few seconds...",
      isData: false,
      timer: '',
      displayButton: false,
      play: false,
      modalContent: "Waiting for a few seconds...",
      showWaitModal: false,
      music_vae: null,
      vaePlayer: null
    };
  },

  mounted: function() {
     this.displayImage()
     this.timer = setInterval(this.displayImage, 5000)
     this.play = true
     axiosStyle({
          url: "/get-image",
          method: "GET",
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }).then(response => {
          this.isData = true;
          this.imageData = response.data
        });
        /*var audio = new Audio(require('../../server/m.mp3'));
        audio.play();*/
        this.setupMusicVAE();


  },
  methods: {
    clearCanvas() {
      this.isData = false
      this.imageData = ""
          },

    displayImage(){
      axiosStyle({
          url: "/get-image",
          method: "GET",
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }).then(response => {
          this.isData = true;
          this.imageData = response.data
        });

    },
     playMusic(){
     this.showWaitModal = true

     axiosStyle({
          url: "/create-music",
          method: "POST",
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }).then(response => {
          this.showWaitModal = false;
          this.playInterpolation();
          console.log("music created")
        }).catch((err) => {
          console.log("music stopped")
        });
    },

    setupMusicVAE() {
      // Initialize model.
      this.music_vae = new mm.MusicVAE('https://storage.googleapis.com/magentadata/js/checkpoints/music_vae/mel_2bar_small');
      this.music_vae.initialize();

      // Create a player to play the sampled sequence.
      this.vaePlayer = new mm.Player();
    },
    playVAE(event) {
      if (this.vaePlayer.isPlaying()) {
        this.vaePlayer.stop();
        event.target.textContent = 'Play';
        return;
      }
      this.music_vae
      .sample(1, 1.5)
      .then((sample) => this.vaePlayer.start(sample[0]));
    },

    async playInterpolation() {
      if (this.vaePlayer.isPlaying()) {
        vaePlayer.stop();
        this.return;
      }
      // Music VAE requires quantized melodies, so quantize them first.
      const twi = await mm.urlToNoteSequence("static/generated.midi");
      const abc = await mm.urlToNoteSequence("static/standard.mid");
      console.log("Note sequences produced");
      const star = await mm.sequences.quantizeNoteSequence(twi, 2);
      const teapot = await mm.sequences.quantizeNoteSequence(abc, 2);

      this.music_vae
      .interpolate([star, teapot], 5)
      .then((sample) => {
            this.vaePlayer.start(sample[3])
           });
      console.log("Played");

    }
  }
};
</script>
<style scoped>
.btn {
  background-color: #008cba;
  border: none;
  border-radius: 0.3em;
  color: white;
  padding: 0.5em 1em;
  margin: 0.5em;
  margin-left: 45%;
  margin-top:20px;
  width: 120px;

  font-size: 1rem;
  font-family: inherit;
  font-weight: 400;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  -webkit-transition-duration: 0.4s; /* Safari */
  transition-duration: 0.4s;
  cursor: pointer;
}

.btn:hover {
  background: #34495e;
}

.btn.disabled,
.btn[disabled],
fieldset[disabled] .btn {
  pointer-events: none;
  cursor: not-allowed;
  box-shadow: none;
  opacity: 0.5;
}

.overlay {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  color: #bdc3c7;
}

.overlay .content {
  margin: 1rem;
}


.image-container {
  display: flex;
  height: 750px;
  width: 750px;
  max-width:1500px;
  max-height: 850px;
  justify-content: center;
  flex-wrap: wrap;
  margin: 0 auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.055);
  transition: all 0.2s ease-in-out;
}

.image-container .image-item {
  display: flex;
  width: 100%;
  height: 100%;
  margin: 3px;
  padding: 2px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.055);
  transition: all 0.2s ease-in-out;
}

.image-container .image-item img {
  display: flex;
  width: 100%;
  height: 100%;
  object-fit: cover;
  overflow: hidden;
}


.half-circle-spinner,
.half-circle-spinner * {
  box-sizing: border-box;
}

.half-circle-spinner {
  width: 4rem;
  height: 4rem;
  border-radius: 100%;
  position: relative;
}

.half-circle-spinner .circle {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 100%;
  border: calc(60px / 10) solid transparent;
}

.half-circle-spinner .circle.circle-1 {
  border-top-color: #bdc3c7;
  animation: half-circle-spinner-animation 1s infinite;
}

.half-circle-spinner .circle.circle-2 {
  border-bottom-color: #bdc3c7;
  animation: half-circle-spinner-animation 1s infinite alternate;
}

@keyframes half-circle-spinner-animation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
