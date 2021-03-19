<template>
  <div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Getter } from 'vuex-class';
import User from '@/models/user';

@Component
export default class Chat extends Vue {
  @Getter('GET_CURRENT_USER')
  currentUser!: User;

}
</script>

<style scoped lang="less">
</style>
