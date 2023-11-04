<template>
    <div>
        <h1>あなたが翻訳したpodcast</h1>
        <table>
            <tr>
                <th>ファイル名</th>
                <th>ファイル</th>
            </tr>
            <tr v-for="file in mp3" :key="file.id">
                <td>{{file.file_name}}</td>
                <td class="file">
                    <audio controls>
                        <source :src="file.url">
                    </audio>
                </td>
            </tr>
        </table>
    </div>
</template>

<script>
import axios from 'axios'
import mixins from '../assets/mixins'
import { useMessageStore } from '../stores/message'

export default {
    name: 'MyPage',
    mixins: [mixins],
    data(){
        return{
            mp3 : []
        }
    },
    setup() {
        const store = useMessageStore()

        return {
            store
        }
    },
    mounted: function(){
        this.get_myfile()
    },
    methods: {
        get_myfile() {
            console.log('get_myfile loaded')
            const base_url = "https://transpod-c78d3a6a1c42.herokuapp.com/"  //process.env.VUE_APP_API_BASE_URL
            const request_url = `${base_url}file`
            const access_token = localStorage.getItem("access_token")
            const options = {headers:{"Authorization":`Bearer ${access_token}`}}

            axios
                .get(request_url, options)
                .then(response => {
                    console.log(response.data)
                    const my_files = response.data
                    const mp3 = []
                    for(var i = 0; i < my_files.length; i++) {
                        var file = my_files[i]
                        var file_info = {}
                        file_info["id"] = i+1
                        file_info["file_name"] = file.file_name 
                        file_info["url"] = file.file_path
                        mp3.push(file_info)
                    }
                    this.mp3 = mp3
                })
                .catch(err => {
                    if (err.response.data.status == 'ACCESS_TOKEN_EXPIRED') {
                        console.log('token切れ')
                        this.refresh_token()
                        .then(result => {
                            console.log(result)
                            this.get_myfile()
                        })
                        .catch(err => {
                            console.log(err)
                            this.store.let_login()
                            this.$router.push('/login')
                        })
                    } else {
                        console.log('それ以外')
                        alert(err.response.data.status)
                    }
                })
        }
    }
}
</script>

<style scoped>

table{
    border-collapse:collapse;
    margin:0 auto;
    width: 70%;
}

th{
    background-color: rgb(216, 213, 213);

}
td{
    border-bottom:1px dashed #999;
    text-align: left;
}

td.file{
    text-align: center;
}

td,th{
    padding:10px;
}

tr:hover {
    background: #cbe2f1;
}

</style>