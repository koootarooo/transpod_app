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
        <!-- <div v-for="file in mp3" :key="file">
            <audio controls>
                <source :src="mp3">
            </audio> -->
        <!-- </div> -->
    </div>
</template>

<script>
// import axios from 'axios'

export default {
    name: 'MyPage',
    data(){
        return{
            mp3 : []
        }
    },
    mounted: function(){
        const mp3 = [
            {
                id: 1,
                file_name: "msuk_test.mp3",
                url: "https://transpod.s3.ap-northeast-1.amazonaws.com/musk_news.mp3"
            },
            {
                id: 2,
                file_name: "test_mark_zuckerberg.mp3",
                url: "https://transpod.s3.ap-northeast-1.amazonaws.com/test_mark_zuckerberg.mp3"   
            }
        ]
        this.mp3 = mp3
    },
    methods: {
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