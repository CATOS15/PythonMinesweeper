<template>
  <div>
      <div>Besked fra backend (socket): {{socketMsg}}</div>
      <div>
        <input v-model="roomname" type="text" placeholder="ex. 53436" :disabled="socketestablishing"/>
        <button @click="socketcreate(roomname)" :disabled="socketestablishing" >opret</button>
        <button @click="socketjoin(roomname)" :disabled="socketestablishing" >join</button>
      </div>
  </div>
</template>

<script lang="ts">
import { io, Socket } from 'socket.io-client';
import { Component, Vue } from 'vue-property-decorator';
import SocketResponse from '@/models/socketResponse';

@Component({
  components: {
  },
})
export default class Home extends Vue {
  socket!: Socket;
  roomname = '459';

  socketestablishing = false;

  socketMsg = '';

  socketcreate(roomname: string){
    this.socket.emit("createroom", JSON.stringify({
      "roomname": roomname
    }))
  }

  socketjoin(roomname: string){
    this.socket.emit("joinroom", JSON.stringify({
      "roomname": roomname
    }))
  }

  mounted(){
    this.socketestablishing = true;
    this.socket = io('ws://' + location.hostname + ':5005');
    this.socket.on('connect', () => {
      //debugger // eslint-disable-line
      this.socketestablishing = false;
      this.socket.on('emitTest', (resp: SocketResponse) => {
        this.socketMsg = resp.data;
      });
    });
  }
}
</script>

<style scoped>

</style>