<template>
  <div>
      <Test />
      <div>Besked fra backend (socket): {{socketMsg}}</div>
  </div>
</template>

<script lang="ts">
import Test from '../components/Test.vue';
import { io, Socket } from "socket.io-client";
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {
    Test
  },
})
export default class Home extends Vue {
  //TODO:: Så det også virker i produktion
  socket: Socket = io("http://127.0.0.1:5000");

  socketMsg = '';

  mounted(){
    this.socket.on("emitTest", (resp: any) => {
      this.socketMsg = resp.data;
    });
  }
}
</script>

<style scoped>

</style>