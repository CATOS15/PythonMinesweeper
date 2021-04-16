<template>
  <div class="content">
      <div class="gameinfo" style="width:1060px;">
        <div>
          <img class="logo" style="cursor:pointer;" src="../../src/assets/bomb_title.png" @click="socketleave" />
        </div>
        <div class="h2">
          Rum: {{currentUser.room.roomname}}
        </div>
      </div>
      <div class="gamechatcontainer">
        <div class="game">
          <div class="gameinfo h2">
            <div>
              Flags: 14
            </div>
            <div>
              Time: 157
            </div>
          </div>
          <div class="gamegrid">
            <div v-for="(y,y_index) in grid" :key="y_index" class="gamerow">
              <div v-for="(x,x_index) in y" :key="x_index">
                <div class="gameblock"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="chat" v-if="initChat">
          <Chat />
        </div>
      </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Getter, Action } from 'vuex-class'
import Chat from '@/components/Chat.vue'
import GameBlock from '@/models/gameblock';
import router from '@/router';
import User from '@/models/user';


@Component({
  components: {
    Chat
  },
})
export default class Game extends Vue {
  @Action("ROOM_LEAVE")
  leaveRoom!: () => Promise<null>;

  @Getter('GET_CURRENT_USER')
  currentUser!: User;

  initChat: boolean = false;
  
  grid: GameBlock[][] = [];  

  //VUE Event
  created (){
    if(!(this.currentUser && this.currentUser.room && this.currentUser.name && this.currentUser.room.roomname && this.currentUser.room.difficulty && this.currentUser.room.width && this.currentUser.room.height)){
        router.replace("/");
        return;
    } 
    for(let y=0;y<this.currentUser.room.height;y++){
      this.grid[y] = [];
      for(let x=0;x<this.currentUser.room.width;x++){
          this.grid[y][x] = new GameBlock();
      }
    }
    this.initChat = true;
  }
  socketleave(){
    this.leaveRoom().then(()=>{
      router.replace("/");
    });
  }
}
</script>

<style scoped>

.content{
  display: flex;
  height: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.logoroomcontainer{
  display:flex;
  height:auto;
  width:1060px; 
  height:auto;
  text-align: left;
}

.logo{
  width:auto;
  height:90px
}

.gameinfo{
  display: flex;
  height:auto;
  width:100%; 
  justify-content: space-between;
  align-items: center;
}

.gameinfo > div{
  padding:0 8px
}

.gamechatcontainer{
  display: flex;
  height: auto;
  align-items: center;
  flex-direction: row;
}

.game{
  height:700px;
}

.gamegrid{
  width:700px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.gamerow{
  display: flex;
  flex-wrap: wrap;
  width:100%;
  justify-content: center;
}

.gameblock{
  height: 32px;
  width: 32px;
  background: #87cefa;
  border-radius: 4px;
  margin : 1px;
  float: left;
}

.chat{
  height:700px;
  width:340px;
}

/*

bobler i top af chat for personer
rum ID I højre side  

*/

</style>