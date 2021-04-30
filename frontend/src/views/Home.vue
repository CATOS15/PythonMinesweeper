<template>
  <div class="content">
    <div>
      <img src="../../src/assets/bomb_title.png" />
    </div>
    <div class="fieldset">

      <div @click="routerNavigate('highscores')" :disabled="connectSocketLoading" class="mb-2 trophy"></div>

      <div>
        <input v-model="currentUser.name" type="text" placeholder="Navn" @keyup.enter="nagivateEnter()"/>
      </div>
      <div v-if="state === HomeStateEnum.CREATE">
        <div class="buttons mt-2">
            <button @click="setDifficulty(Difficulty.EASY)"   :class="{backgroundGreen : difficulty === Difficulty.EASY}"    style="flex-grow:1;">Nem</button>
            <button @click="setDifficulty(Difficulty.MEDIUM)" :class="{backgroundGreen : difficulty === Difficulty.MEDIUM}"  style="flex-grow:1;">Middel</button>
            <button @click="setDifficulty(Difficulty.HARD)"   :class="{backgroundGreen : difficulty === Difficulty.HARD}"    style="flex-grow:1;">Svær</button>
        </div>
      </div>
      <div v-if="state === HomeStateEnum.JOIN" class="mt-1">
        <input class="mt-2" v-model="currentUser.room.roomname" type="text" placeholder="Rum nummer" @keyup.enter="nagivateEnter()" />
      </div>


      <div class="buttons mt-2" v-if="state === HomeStateEnum.DEFAULT">
          <button @click="navigate(HomeStateEnum.CREATE)" :disabled="connectSocketLoading" style="flex-grow:1">Opret</button>
          <button @click="navigate(HomeStateEnum.JOIN)" :disabled="connectSocketLoading" style="flex-grow:3;">Tilslut</button>
      </div>
      <div class="buttons mt-4" v-if="state === HomeStateEnum.CREATE">
          <button @click="navigate(HomeStateEnum.DEFAULT)" :disabled="connectSocketLoading" class="backgroundRed" style="flex-grow:1">Tilbage</button>
          <button @click="socketcreate()" :disabled="connectSocketLoading" style="flex-grow:3;">Opret</button>
      </div>
      <div class="buttons mt-4" v-if="state === HomeStateEnum.JOIN">
          <button @click="navigate(HomeStateEnum.DEFAULT)" :disabled="connectSocketLoading" class="backgroundRed" style="flex-grow:1">Tilbage</button>
          <button @click="socketjoin()" :disabled="connectSocketLoading" style="flex-grow:3;">Tilslut</button>
      </div>

      <div class="response">
        {{msg}}
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue} from 'vue-property-decorator';
import User from '@/models/user';
import Highscore from '@/models/highscore';
import router from '@/router';
import { Action } from 'vuex-class'
import SocketResponse from '@/models/socketResponse';
import { HomeStateEnum, Difficulty } from '@/models/enums';


@Component({
  components: {
  },
})
export default class Home extends Vue {
  @Action("CONNECT_SOCKET")
  connectSocket!: () => Promise<SocketResponse>;
  
  @Action("ROOM_CREATE")
  createRoom!: (user: User) => Promise<SocketResponse>;

  @Action("ROOM_JOIN")
  joinRoom!: (user: User) => Promise<SocketResponse>;

  currentUser: User = new User();
  connectSocketLoading = false;
  msg = '';

  HomeStateEnum = HomeStateEnum;
  state: HomeStateEnum = HomeStateEnum.DEFAULT;

  Difficulty = Difficulty;
  difficulty: Difficulty = Difficulty.EASY;

  mounted(){
    this.connectSocketLoading = true;
    this.connectSocket().then((resp: SocketResponse) => {
      console.log(resp.msg);
    }).catch((resp: SocketResponse) => {
      console.error(resp.msg);
    }).finally(() => {
      this.connectSocketLoading = false;
    });

    if(this.$route.query.roomname){
      this.currentUser.room.roomname = this.$route.query.roomname.toString();
    }
  }

  setState(state: HomeStateEnum){
    this.msg = "";
    this.state = state;
  }

  setDifficulty(difficulty: Difficulty){
    this.difficulty = difficulty;
  }

  routerNavigate(path: string){
    router.push(path);
  }

  navigate(toState: HomeStateEnum){
    if(toState === HomeStateEnum.JOIN && this.currentUser.room.roomname){
      this.socketjoin();
    }else{
      this.currentUser.room.roomname = "";
      this.setState(toState);
    }
  }

  nagivateEnter(){
    switch(this.state){
      case HomeStateEnum.DEFAULT:
        this.navigate(HomeStateEnum.JOIN);
        break;
      case HomeStateEnum.CREATE:
        this.socketcreate();
        break;
      case HomeStateEnum.JOIN:
        this.socketjoin();
        break;
    }
  }

  validate(){
    if(this.currentUser.name.length < 3){
      this.msg = "Navnet skal være 3 karakterer eller længere";
      return false;
    }
    if(this.state === HomeStateEnum.JOIN && this.currentUser.room.roomname.length !== 4){
      this.msg = "Rum nummeret skal være 4 karakterer langt";
      return false;
    }
    return true;
  }

  socketcreate(){
    //TEMP INDTIL BACKEND GENERER RUM ID'ER
    this.currentUser.room.roomname = (Math.floor(Math.random() * 8999) + 1000).toString();
    this.currentUser.room.difficulty = this.difficulty;

    if(!this.validate()) {
      return;
    }
    this.createRoom(this.currentUser).then((resp: SocketResponse) => {
      if(resp.success){
        router.push('game');
      }else{
        this.msg = resp.msg;
      }
    });
  }

  socketjoin(){
    if(!this.validate()) {
      return;
    }
    this.joinRoom(this.currentUser).then((resp: SocketResponse) => {
      if(resp.success){
        router.push('game');
      }else{
        this.msg = resp.msg;
      }
    });
  }
}
</script>

<style scoped>

.content{
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-size:1.3em;
}
.content .fieldset{
  width: 350px;
  min-height: 275px;
}

.content .fieldset .buttons{
  display:flex;
}

.content .response{
  height: 30px;
}

.content .fieldset .trophy{
  background-image: url(../../src/assets/images/trophy.svg);
  background-size: cover;
  background-position: 5px 7px;
  background-repeat: no-repeat;
  background-size: 30px;
  background-color: #fed8432e;
  float:right;
  width:40px;
  height:40px;
  cursor:pointer;
  border-radius: 20px;
  box-shadow: 2px 2px 1px 0px #dcbc402e;
}
.content .fieldset .trophy:hover{
  background-color: #fed84369;
}

</style>