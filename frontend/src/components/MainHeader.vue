<template>
    <header class="header">
        <a href="">
            <img src="../assets/transpod_logo_lightblue.png" height="40" width="104" alt="transpod">
        </a>
        <router-link class="mypage_link" to="/mypage">マイページ</router-link>
    </header>
</template>

<script>
export default {
    name: 'MainHeader',
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.header {
    display: flex;
    justify-content: flex-start;
    /* border-bottom: solid 1px;
    border-bottom-color: rgb(219, 218, 218); */
}
.mypage_link {
    margin: 0 0 0 auto;
}
span {
    font-weight: bold;
    font-size: 20px;
}
</style>