<template>
  <div id="app">
    <MainHeader/>
    <TranslatePodcast/>
  </div>
</template>

<script>
import MainHeader from './components/MainHeader.vue'
import TranslatePodcast from './components/TranslatePodcast.vue'

export default {
  name: 'App',
  components: {
    TranslatePodcast,
    MainHeader
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
