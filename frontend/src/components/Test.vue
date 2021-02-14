<template>
  <div>
    {{test}}
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Test extends Vue {
  test = "ja";

  created(){
    this.test = "123 bla";
  }
}
</script>

<style scoped lang="less">

</style>
