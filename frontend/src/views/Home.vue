<template>
  <div>
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import HelloWorld from '../components/HelloWorld.vue';

@Component({
  components: {
    HelloWorld,
  },
})
export default class Home extends Vue {}
</script>

<style scoped>

</style>