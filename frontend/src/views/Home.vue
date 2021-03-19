<template>
  <div>
      <div>
        <input v-model="GLOBAL.currentUser.name" type="text" :disabled="socketestablishing"/>
        <input v-model="GLOBAL.currentUser.roomname" type="text" placeholder="ex. 53436" :disabled="socketestablishing"/>
        <button @click="socketcreate(GLOBAL.currentUser)" :disabled="socketestablishing" >opret</button>
        <button @click="socketjoin(GLOBAL.currentUser)" :disabled="socketestablishing" >join</button>
      </div>
  </div>
</template>

<script lang="ts">
import { io } from 'socket.io-client';
import { Component, Vue} from 'vue-property-decorator';
import User from '@/models/user';
import HttpReponse from '@/models/httpResponse';
import router from '@/router';
import { GLOBAL } from '@/global'


@Component({
  components: {
  },
})
export default class Home extends Vue {
  GLOBAL = GLOBAL;

  socketestablishing = false;

  socketcreate(user: User){
    if(!GLOBAL.currentSocket) return;

    GLOBAL.currentSocket.emit("createroom", JSON.stringify(user), (resp: string) => {
      const response = JSON.parse(resp) as HttpReponse

      if(response.success){
        router.push('game')
      }
    });
  }

  socketjoin(user: User){
    if(!GLOBAL.currentSocket) return;

    GLOBAL.currentSocket.emit("joinroom", JSON.stringify(user), (resp: string) => {
       const response = JSON.parse(resp) as HttpReponse
    
      if(response.success){
        router.push('game')
      }
    });
  }

  mounted(){
    this.socketestablishing = true;
    GLOBAL.currentSocket = io('ws://' + location.hostname + ':5005');
    GLOBAL.currentSocket.on('connect', () => {
      if(!GLOBAL.currentSocket) return;
      this.socketestablishing = false;
    });
  }
}
</script>

<style scoped>

</style>