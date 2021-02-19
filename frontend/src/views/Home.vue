<template>
  <div>
      <Test />
      <div>Besked fra backend (socket): {{socketMsg}}</div>
  </div>
</template>

<script lang="ts">
import Test from '../components/Test.vue';
import { io, Socket } from 'socket.io-client';
import { Component, Vue } from 'vue-property-decorator';
import SocketResponse from '@/models/socketResponse';

@Component({
  components: {
    Test
  },
})
export default class Home extends Vue {
  socket: Socket = io('ws://' + location.hostname + ':5005');

  socketMsg = '';

  mounted(){
    this.socket.on('emitTest', (resp: SocketResponse) => {
      this.socketMsg = resp.data;
    });
  }
}
</script>

<style scoped>

</style>