<template>
  <div>
      <div>
        <input v-model="currentUser.name" type="text" :disabled="connectSocketLoading"/>
        <input v-model="currentUser.roomname" type="text" placeholder="ex. 53436" :disabled="connectSocketLoading"/>
        <button @click="socketcreate()" :disabled="connectSocketLoading" >opret</button>
        <button @click="socketjoin()" :disabled="connectSocketLoading" >join</button>
        {{errorMsg}}
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
  connectSocketLoading = false;
  errorMsg = '';

  mounted(){
    this.connectSocketLoading = true;
    this.connectSocket().then((resp: SocketResponse) => {
      console.log(resp.msg);
    }).catch((resp: SocketResponse) => {
      console.error(resp.msg);
    }).finally(() => {
      this.connectSocketLoading = false;
    });
  }

  socketcreate(){
    this.createRoom(this.currentUser).then((resp: SocketResponse) => {
      if(resp.success){
        router.push('game');
      }else{
        this.errorMsg = resp.msg;
      }
    });
  }

  socketjoin(){
    this.joinRoom(this.currentUser).then((resp: SocketResponse) => {
      if(resp.success){
        router.push('game');
      }else{
        this.errorMsg = resp.msg;
      }
    });
  }
}
</script>

<style scoped>

</style>