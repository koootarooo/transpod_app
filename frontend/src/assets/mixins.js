import axios from 'axios'

export default {
    methods: {
        refresh_token() {
            return new Promise(function(resolve, reject) {
                console.log('refresh_token取得中(mixin）')
                const data = ""
                const refresh_token = localStorage.getItem("refresh_token")
                const options = {headers:{"Authorization":`Bearer ${refresh_token}`}}

                axios
                    .post('http://127.0.0.1:5000/refresh', data, options)
                    .then(response => {
                        console.log(response.data)
                        localStorage.setItem('access_token', response.data.access_token)
                        localStorage.setItem('refresh_token', response.data.refresh_token)
                        localStorage.setItem('user_id', response.data.user_id)
                        resolve('refreshed')
                    })
                    .catch(err => {
                        console.log(err)
                        // ログインし直しが必要なので、ログインページへ遷移
                        // 本当は「ログインが必要です」みたいなメッセージを出したい
                        // this.$router.push('/login')
                        reject(err)
                    })
                
                // if(result == "成功") {
                //     resolve()
                // }else {
                //     reject()
                // }
            })
        }
    }
}