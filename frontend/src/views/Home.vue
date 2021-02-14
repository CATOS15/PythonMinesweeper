<template>
  <div>
      <Test />
      <div>Besked fra backend (socket): {{socketMsg}}</div>
  </div>
</template>

<script lang="ts">
import Test from '../components/Test.vue';
import SocketResponse from '../models/socketResponse'
import { io, Socket } from "socket.io-client";
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {
    Test
  },
})
export default class Home extends Vue {
  socket: Socket = io("ws://" + location.hostname + ":5005");

  socketMsg = '';

  mounted(){
    this.socket.on("emitTest", (resp: SocketResponse) => {
      this.socketMsg = resp.data;
    });
  }
}
</script>

<style scoped>

</style>