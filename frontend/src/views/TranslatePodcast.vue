<template>
  <div class="translate">
    <div class="msg">
      <h1>海外podcastを日本語で聞こう。</h1>
    </div>
    <div class="drop_zone" @dragenter="dragEnter" @dragleave="dragLeave" @dragover.prevent @drop.prevent="dropFile" :class="{enter: isEnter}" v-if="!isLoading">
      <img src="../assets/upload_img_lightblue.png" width="60" height="60">
      <span class="main_message">ここにデータをドラッグ&ドロップしてください</span><br>
      <span class="available_format">.mp3 .mpeg only</span>
    </div>
    <div class="preview_zone">
      <p>{{file_title}}</p>
      <p>{{file_size}}</p>
    </div>
    <button class="translate_btn" @click="translate()" v-if="!isLoading" v-bind:disabled="!isFile">翻訳する</button>
    <div class="loading_contents" v-if="isLoading">
      <div class="loading_message">
        翻訳中...<br>
        翻訳が完了したらメールでお知らせします。<br>
        翻訳は数分かかることもあります。
      </div>
      <div class="fulfilling-bouncing-circle-spinner">
        <div class="circle"></div>
        <div class="orbit"></div>
      </div>
      <div class="translate_more" @click="reset()">
        <span class="translate_again_btn">他のファイルを翻訳する</span>
      </div>
    </div>
    <!-- <div class="overlay" v-if="showModal">
      <div class="overlay_contents">
        <button class="closeButton" @click="closeModal()">close×</button>
        <p>メールアドレスを入力してください。<br>翻訳が完了したらメールでお知らせします。</p>
        <input type="text" class="emailForm" v-model="userEmail" />
        <button class="translate_btn" @click="closeModal(); translate()" v-bind:disabled="!rightEmail">翻訳する</button>
      </div>
    </div> -->
  </div>
</template>

<script>
import axios from 'axios'
import mixins from '../assets/mixins'
import { useMessageStore } from '../stores/message'

export default {
  name: 'TranslatePodcast',
  mixins: [mixins],
  data() {
    return {
      file_data: "",
      file_title: "",
      file_size: "",
      isEnter: false,
      isLoading: false,
      isFile: false,
      showModal: false,
      userEmail: ""
    }
  },
  setup() {
    const store = useMessageStore()
    return {
      store
    }
  },
  computed: {
    rightEmail: function(){
      const right_pattern = new RegExp(/^[A-Za-z0-9]{1}[A-Za-z0-9_.-]*@{1}[A-Za-z0-9_.-]+.[A-Za-z0-9]+$/);
      return right_pattern.test(this.userEmail)
    }
  },
  mounted: function() {
    console.log(process.env.VUE_APP_TEST)
  },
  methods: {
    dragEnter() {
      this.isEnter = true;
    },
    dragLeave() {
      this.isEnter = false;
    },
    dropFile() {
      const file = event.dataTransfer.files[0]
      const formData = new FormData()
      formData.append('file',file)
      this.file_data = formData
      this.file_title = file.name
      const fs = file.size/1024/1024
      this.file_size = fs.toFixed(1) + "MB"
      this.isEnter = false
      this.isFile = true
    },
    translate() {
      console.log('translate called')
      this.isLoading = true
      const data = this.file_data
      const access_token = localStorage.getItem("access_token")
      const options = {headers:{"Authorization":`Bearer ${access_token}`}}
      const base_url = "https://transpod-c78d3a6a1c42.herokuapp.com/"  //process.env.VUE_APP_API_BASE_URL
      const request_url = `${base_url}file`
      console.log(request_url)

      axios
        .post(request_url, data, options)
        .then(response => {
          console.log(response.data)
          this.reset()
        })
        .catch(err => {
          if (err.response.data.status == 'ACCESS_TOKEN_EXPIRED') {
            console.log('token切れ')
            this.refresh_token()
            .then(result => {
              console.log(result)
              this.translate()
            })
            .catch(err => {
              console.log(err)
              // エラーメッセージの変更
              this.store.let_login()
              this.$router.push('/login')
            })
          } else {
            console.log('それ以外')
            alert(err.response.data.status)
          }
        })
    },
    reset() {
      this.file_data = ""
      this.file_title = ""
      this.file_size = ""
      this.isLoading = false
      this.isFile = false
    },
    openModal(){
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.translate {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
}
.msg {
  align-self: center;
}
.upload_zone {
  align-self: center;
}
.drop_zone {
  border: 3px dotted #d3d3d3;
  width: 50vw;
  height: 20vw;
  display:flex;
  align-self: center;
  flex-flow: column;
  align-items: center;
  justify-content: center;
  color: black;
  font-size: 20px;
  font-weight: bold;
}
.drop_zone p {
  color: black;
  font-size: 20px;
}
.enter {
  background-color:  rgb(26, 94, 240);
  opacity: 0.3;
}
.available_format {
  color: gray;
}
.translate_btn {
  display: block;
	text-align: center;
	text-decoration: none;
	width: 200px;
	margin: auto;
	padding: 1rem 4rem;
  font-size: 16px;
	font-weight: bold;  
	border: 2px solid #27acd9;
	background: #27acd9;
	color: #fff;
	border-radius: 100vh;
	transition: 0.5s;
}
.translate_btn:disabled {
  border: gray;
  background: gray;
  color: rgb(66, 66, 66);
  pointer-events: none;
}
.translate_btn:hover {
	color: #27acd9;
	background: #fff;
}
.loading_contents {
  display: flex;
  align-self: center;
  flex-flow: column;
  align-items: center;
  justify-content: center;
}
.main_message {
  color: #27acd9;
  font-size: 25px;
}
.loading_message {
  padding-bottom: 20px;
  font-weight: bold;
}
.translate_more {
  padding-top: 20px;
}
.translate_again_btn {
  text-decoration: underline;
  color: blue;
}

/* overlay */
.overlay{
  z-index:1;
  position:fixed;
  top:0;
  left:0;
  width:100%;
  height:100%;
  background-color:rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.overlay_contents {
  z-index: 2;
  width: 50%;
  height:50%;
  padding: 1em;
  background: #fff;
  display: flex;
  align-self: center;
  flex-flow: column;
  align-items: center;
  justify-content: center;
}
.overlay_contents p {
  font-weight: bold;
}
.emailForm {
  width: 200px;
  padding: 3px 7px;
  border-radius: 5px;
  border: 2px solid #ccc;
}
.emailForm:focus {
  outline: 0;
  border: 2px solid #2196f3;
}
.closeButton {
  align-self: flex-end;
  border: #fff;
  background-color: #fff;
}

/* loading animation */
.fulfilling-bouncing-circle-spinner, .fulfilling-bouncing-circle-spinner * {
  box-sizing: border-box;
}

.fulfilling-bouncing-circle-spinner {
  height: 60px;
  width: 60px;
	display: flex;
  align-self: center;
  animation: fulfilling-bouncing-circle-spinner-animation infinite 4000ms ease;
}

.fulfilling-bouncing-circle-spinner .orbit {
  height: 60px;
  width: 60px;
  position: absolute;
  top: 0;
  left: 0;
  border-radius: 50%;
  border: calc(60px * 0.03) solid #27acd9;
  animation: fulfilling-bouncing-circle-spinner-orbit-animation infinite 4000ms ease;
}

.fulfilling-bouncing-circle-spinner .circle {
  height: 60px;
  width: 60px;
  color: #27acd9;
  display: block;
  border-radius: 50%;
  position: relative;
  border: calc(60px * 0.1) solid #27acd9;
  animation: fulfilling-bouncing-circle-spinner-circle-animation infinite 4000ms ease;
  transform: rotate(0deg) scale(1);
}

@keyframes fulfilling-bouncing-circle-spinner-animation {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
  }

@keyframes fulfilling-bouncing-circle-spinner-orbit-animation {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1);
  }
  62.5% {
    transform: scale(0.8);
  }
  75% {
    transform: scale(1);
  }
  87.5% {
    transform: scale(0.8);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes fulfilling-bouncing-circle-spinner-circle-animation {
  0% {
    transform: scale(1);
    border-color: transparent;
    border-top-color: inherit;
  }
  16.7% {
    border-color: transparent;
    border-top-color: initial;
    border-right-color: initial;
  }
  33.4% {
    border-color: transparent;
    border-top-color: inherit;
    border-right-color: inherit;
    border-bottom-color: inherit;
  }
  50% {
    border-color: inherit;
    transform: scale(1);
  }
  62.5% {
    border-color: inherit;
    transform: scale(1.4);
  }
  75% {
    border-color: inherit;
    transform: scale(1);
    opacity: 1;
  }
  87.5% {
    border-color: inherit;
    transform: scale(1.4);
  }
  100% {
    border-color: transparent;
    border-top-color: inherit;
    transform: scale(1);
  }
} 

/* for smartphone */
@media screen and (max-width:480px) {
  .msg {
    margin-top: 30px;
  }
  .drop_zone {
    border: 3px dotted #d3d3d3;
    width: 90vw;
    height: 70vw;
    display:flex;
    align-self: center;
    flex-flow: column;
    align-items: center;
    justify-content: center;
    color: black;
    font-size: 20px;
    font-weight: bold;
  }
  .overlay{
    z-index:1;
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background-color:rgba(0,0,0,0.5);
    display: block;
  }
  .overlay_contents {
    z-index: 2;
    width: 75%;
    height:25%;
    background: #fff;
    margin: auto;
    margin-top: 80px;
  }

}
</style>
