<template>
  <div class="app">
    <div class="routerLinks">
      <router-link to="/">Hjem</router-link> 
      <router-link to="/game">Game</router-link>
    </div>
    <div class="container">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {
  },
})
export default class App extends Vue {
}
</script>

<style lang="less">
html, body, .app{
  margin: auto;
  width: 100%;
  height: 100%;
}
.routerLinks > a{
  margin-left:5px;
}
</style>
