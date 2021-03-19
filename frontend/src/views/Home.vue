<template>
  <div>
      <div>
        <input v-model="currentUser.name" type="text" :disabled="socketLoading"/>
        <input v-model="currentUser.roomname" type="text" placeholder="ex. 53436" :disabled="socketLoading"/>
        <button @click="socketcreate()" :disabled="socketLoading" >opret</button>
        <button @click="socketjoin()" :disabled="socketLoading" >join</button>
      </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue} from 'vue-property-decorator';
import User from '@/models/user';
import router from '@/router';
import { Action } from 'vuex-class'
import SocketResponse from '@/models/socketResponse';


@Component({
  components: {
  },
})
export default class Home extends Vue {
  @Action("CONNECT_SOCKET")
  connectSocket!: () => Promise<SocketResponse>;
  
  @Action("CREATE_ROOM")
  createRoom!: (user: User) => Promise<SocketResponse>;

  @Action("JOIN_ROOM")
  joinRoom!: (user: User) => Promise<SocketResponse>;
  
  currentUser: User = new User();
  socketLoading = false;

  mounted(){
    this.socketLoading = true;
    this.connectSocket().then((resp: SocketResponse) => {
      console.log(resp.msg);
    }).catch((resp: SocketResponse) => {
      console.error(resp.msg);
    }).finally(() =>{
      this.socketLoading = false;
    });
  }

  socketcreate(){
    this.createRoom(this.currentUser).then((resp: SocketResponse) => {
      if(resp.success){
        router.push('game');
      }
    });
  }

  socketjoin(){
    this.joinRoom(this.currentUser).then((resp: SocketResponse) => {
      if(resp.success){
        router.push('game');
      }
    });
  }
}
</script>

<style scoped>

</style>