<template>
  <div>
      <div>Besked fra backend (socket): {{socketMsg}}</div>
      <div>
        <input v-model="$globaldata.user.name" type="text" :disabled="socketestablishing"/>
        <input v-model="$globaldata.user.roomname" type="text" placeholder="ex. 53436" :disabled="socketestablishing"/>
        <button @click="socketcreate($globaldata.user)" :disabled="socketestablishing" >opret</button>
        <button @click="socketjoin($globaldata.user)" :disabled="socketestablishing" >join</button>
      </div>
  </div>
</template>

<script lang="ts">
import { io } from 'socket.io-client';
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
  socketestablishing = false;
  socketMsg = '';

  socketcreate(user: User){
    this.$globaldata.socket.emit("createroom", JSON.stringify(user), (resp: string) => {
      const response = JSON.parse(resp) as HttpReponse

      if(response.success){
        router.push('game')
      }
      console.log(response)
    });
  }

  socketjoin(user: User){
    this.$globaldata.socket.emit("joinroom", JSON.stringify(user), (resp: string) => {
       const response = JSON.parse(resp) as HttpReponse
    
      if(response.success){
        router.push('game')
      }
    });
  }

  mounted(){
    debugger // eslint-disable-line
    this.socketestablishing = true;
    this.$globaldata.socket = io('ws://' + location.hostname + ':5005');
    this.$globaldata.socket.on('connect', () => {
      this.socketestablishing = false;
      this.$globaldata.socket.on('emitTest', (resp: SocketResponse) => {
        this.socketMsg = resp.data;
      });
    });
  }
}
</script>

<style scoped>

</style>