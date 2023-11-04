<template>
    <div>
        <h1>ログイン画面</h1>
        <p class="err_msg">{{ store.message }}</p>
        <form>
            <div class="group">
                <input type="email" v-bind:class="{ 'used': isUsed_mail }" @blur="handleBlur_mail" v-model="inputValue_mail">
                <span class="highlight"></span><span class="bar"></span>
                    <label>メールアドレス</label>
            </div>
            <div class="group">
                <input type="password" v-bind:class="{ 'used': isUsed_password }" @blur="handleBlur_password" v-model="inputValue_password">
                <span class="highlight"></span><span class="bar"></span>
                    <label>パスワード</label>
                <div class="password_alert" v-show="!rightPassword">※パスワードは半角英数字を各1種類以上含む8文字以上が必要です。</div>
            </div>
            <button type="button" class="login_btn" @click="login()" v-bind:disabled="!disabledJudge">ログイン</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios'
import { useMessageStore } from '../stores/message'

export default {
    name: 'LogIn',
    data(){
        return{
            inputValue_mail: '',
            inputValue_password: '',
            isUsed_mail: false,
            isUsed_password: false
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
            return right_pattern.test(this.inputValue_mail)
        },
        rightPassword: function(){
            const right_password = new RegExp(/^(?=.*?[a-z])(?=.*?\d)[a-z\d]{8,100}$/i);
            return right_password.test(this.inputValue_password)
        },
        disabledJudge: function(){
            const judge = this.rightEmail && this.rightPassword ? true: false 
            return judge
        },
        isErrorMsg: function(){
            const isEror = this.err_msg != "" ? true: false
            return isEror 
        }
    },
    methods: {
        handleBlur_mail() {
            this.isUsed_mail = this.inputValue_mail ? true : false
        },
        handleBlur_password() {
            this.isUsed_password = this.inputValue_password ? true : false
        },
        login() {
            const base_url = "https://transpod-c78d3a6a1c42.herokuapp.com/"  //process.env.VUE_APP_API_BASE_URL
            const request_url = `${base_url}login`
            const data = {
                email: this.inputValue_mail,
                password: this.inputValue_password
            }

            const options = {headers:{ 'Content-Type': 'application/json'}}

            axios
                .post(request_url, data, options)
                .then(response => {
                    localStorage.setItem('access_token', response.data.access_token)
                    localStorage.setItem('refresh_token', response.data.refresh_token)
                    localStorage.setItem('user_id', response.data.user_id)
                    // トップへリダイレクト
                    this.store.delete_message()
                    this.$router.push('/')
                })
                .catch(err => {
                    alert(err)
                })
        }
    }
}
</script>


<style scoped>
form {
    width: 380px;
    margin: 4em auto;
    padding: 3em 2em 2em 2em;
    background: #fafafa;
    border: 1px solid #ebebeb;
    box-shadow: rgba(0,0,0,0.14902) 0px 1px 1px 0px,rgba(0,0,0,0.09804) 0px 1px 2px 0px;
}

.group { 
    position: relative; 
    margin-bottom: 45px; 
}

input {
    font-size: 18px;
    padding: 10px 10px 10px 5px;
    display: block;
    background: #fafafa;
    color: #636363;
    width: 100%;
    border: none;
    border-radius: 0;
    border-bottom: 1px solid #757575;
}

input:focus { outline: none; }

.err_msg {
    color: red;
    font-size: 20px;
    font-weight: bold;
}

/* Label */

label {
    color: #999; 
    font-size: 14px;
    font-weight: normal;
    position: absolute;
    pointer-events: none;
    left: 5px;
    top: 10px;
    transition: all 0.2s ease;
}

/* active */

input:focus ~ label, input.used ~ label {
    top: -20px;
    transform: scale(.75); left: -2px;
    /* font-size: 14px; */
    color: #4a89dc;
}


/* Underline */

.bar {
    position: relative;
    display: block;
    width: 100%;
}

.bar:before, .bar:after {
    content: '';
    height: 2px; 
    width: 0;
    bottom: 1px; 
    position: absolute;
    background: #4a89dc; 
    transition: all 0.2s ease;
}

.bar:before { left: 50%; }

.bar:after { right: 50%; }


/* active */

input:focus ~ .bar:before, input:focus ~ .bar:after { width: 50%; }

/* Highlight */

.highlight {
    position: absolute;
    height: 60%; 
    width: 100px; 
    top: 25%; 
    left: 0;
    pointer-events: none;
    opacity: 0.5;
}

input:focus ~ .highlight {
    animation: inputHighlighter 0.3s ease;
}


/* Animations */

@keyframes inputHighlighter {
    from { background: #4a89dc; }
    to  { width: 0; background: transparent; }
}

/* Button */
.login_btn {
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

.login_btn:hover {
	color: #27acd9;
	background: #fff;
}

.login_btn:disabled {
    border: gray;
    background: gray;
    color: rgb(66, 66, 66);
    pointer-events: none;
}

.password_alert {
    color:#4f5152;
    font-size: 12px;
    margin-top: 20px;
}

</style>