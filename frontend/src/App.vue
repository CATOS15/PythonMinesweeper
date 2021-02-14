<template>
  <div>
    <div>
      <router-link to="/">Hjem</router-link>
    </div>
    <router-view />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {},
})
export default class App extends Vue {
}
</script>

<style lang="less">

</style>
