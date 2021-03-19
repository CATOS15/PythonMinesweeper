<template>
  <div>
      <div class="game">
        
        <div class="h2">Welcome {{GLOBAL.currentUser.name}}</div>
        <div class="gamegrid">
          <div v-for="(x,x_index) in grid" :key="x_index">
            <div v-for="(y,y_index) in x" :key="y_index">
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
import Chat from '@/components/Chat.vue'
import GameBlock from '@/models/gameblock';
import { GLOBAL } from '@/global';
import router from '@/router';


@Component({
  components: {
    Chat
    
  },
})
export default class Game extends Vue {
  GLOBAL = GLOBAL;
  
  grid: GameBlock[][] = [];  

  created (){
    if(!(GLOBAL.currentUser && GLOBAL.currentUser.roomname && GLOBAL.currentUser.name)){
      router.replace("/");
      return;
    }

    const sizeX = 20;
    const sizeY = 15;
    for(let x=0;x<sizeX;x++){
      this.grid[x] = [];
      for(let y=0;y<sizeY;y++){
          this.grid[x][y] = new GameBlock();
      }
    }
  }

}
</script>

<style scoped>

.game{
  width:calc(100% - 200px);
  height:100%;
  float:left;
}

.gamegrid{
  height: 510px;
  width: 680px;
  margin: auto;
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
  width:200px;
  height:100%;
  float:left;
}
</style>