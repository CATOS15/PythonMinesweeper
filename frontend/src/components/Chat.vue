<template>
  <div>
    {{name}}
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class Chat extends Vue {
  @Prop({required: true})
  public name!: string;
}
</script>

<style scoped lang="less">
</style>
