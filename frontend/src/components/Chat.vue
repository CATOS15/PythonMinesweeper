<template>
  <div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { GLOBAL } from '@/global';

@Component
export default class Chat extends Vue {
  GLOBAL = GLOBAL;
}
</script>

<style scoped lang="less">
</style>
