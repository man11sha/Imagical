<template>
<div id="wrapper" style="color:darkblue; background-color: powderblue;">
  <body style="color:darkblue; background-color: powderblue;">
  <div id="app">
<h1> Hello</h1>
    <div id="imgBody">
<img v-if="imageData"
               :src="imageData"
               alt="" height='500px' width = '500px' align='middle'/>
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
      displayButton: false
    };
  },

  mounted: function() {
     this.timer = setInterval(this.displayImage, 5000)
     this.timer1 = setInterval(this.playMusic, 15000)
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
        // var audio = new Audio(require('../assets/m.mp3'));
        // audio.play();


  },
  methods: {
    clearCanvas() {
      this.isData = false
      this.imageData = ""
          },

    displayImage(){
      console.log("hello")
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
      axiosStyle({
          url: "/play-music",
          method: "POST",
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }).then(response => {
          console.log("music played")
        }).catch((err) => {
          console.log("music stopped")
        });
    }


  }
};
</script>
