<template>
  <div>
      <div>Besked fra backend (socket): {{socketMsg}}</div>
      <div>
        <input v-model="user.name" type="text" :disabled="socketestablishing"/>
        <input v-model="user.roomname" type="text" placeholder="ex. 53436" :disabled="socketestablishing"/>
        <button @click="socketcreate(user)" :disabled="socketestablishing" >opret</button>
        <button @click="socketjoin(user)" :disabled="socketestablishing" >join</button>
      </div>
  </div>
</template>

<script lang="ts">
import { io, Socket } from 'socket.io-client';
import { Component, Vue} from 'vue-property-decorator';
import SocketResponse from '@/models/socketResponse';
import User from '@/models/user';
import HttpReponse from '@/models/httpResponse';
import router from '@/router';


@Component({
  components: {
  },
})
export default class Home extends Vue {
  user: User = new User();
  socket!: Socket;

  socketestablishing = false;
  socketMsg = '';

  socketcreate(user: User){
    this.socket.emit("createroom", JSON.stringify(user), (resp: string) => {
      const response = JSON.parse(resp) as HttpReponse

      if(response.success){
        router.push('game')
      }
      console.log(response)
    });
  }

  socketjoin(user: User){
    this.socket.emit("joinroom", JSON.stringify(user), (resp: string) => {
       const response = JSON.parse(resp) as HttpReponse
    
      if(response.success){
        router.push('game')
      }
    });
  }

  mounted(){
    this.socketestablishing = true;
    this.socket = io('ws://' + location.hostname + ':5005');
    this.socket.on('connect', () => {
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