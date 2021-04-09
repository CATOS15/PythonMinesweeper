<template>
  <div>
      <div class="game">
        <div class="h2 text-center">Welcome {{currentUser.name}} i rummet {{currentUser.room.roomname}}</div>
        <div class="gamegrid">
          <div v-for="(y,y_index) in grid" :key="y_index" class="gamerow">
            <div v-for="(x,x_index) in y" :key="x_index">
              <div class="gameblock"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="chat">
        <Chat />
      </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Getter } from 'vuex-class'
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
  @Getter('GET_CURRENT_USER')
  currentUser!: User;
  
  grid: GameBlock[][] = [];  

  //VUE Event
  created (){
    if(!(this.currentUser && this.currentUser.room && this.currentUser.name && this.currentUser.room.roomname && this.currentUser.room.difficulty && this.currentUser.room.width && this.currentUser.room.height)){
        router.replace("/");
        return;
    } 
    
    /*
    [
    [2,2,2,2,2,2]
    [2,2,2,2,2,2]
    [2,2,2,2,2,2]
    [2,2,2,2,2,2]
    [2,2,2,2,2,2]
    ]

    */

    for(let y=0;y<this.currentUser.room.height;y++){
      this.grid[y] = [];
      for(let x=0;x<this.currentUser.room.width;x++){
          this.grid[y][x] = new GameBlock();
      }
    }
  }

}
</script>

<style scoped>

.container > div{
  display: flex;
  height: 100%;
  align-items: center;
}

.game{
  height:700px;
}

.gamegrid{
  width:720px;
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
  min-width: 400px;
  width:400px;
  background: white;
}
</style>