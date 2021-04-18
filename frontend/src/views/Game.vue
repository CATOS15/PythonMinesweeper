<template>
  <div class="content" @contextmenu.prevent>
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
              Flag: 14
            </div>
            <div>
              Tid: 157
            </div>
          </div>
          <div class="gamegrid" ref="gamegridHTML">
            <div v-for="(x,x_index) in grid" :key="x_index" class="gamerow">
              <div v-for="(y,y_index) in x" :key="y_index">
                <div class="field" 
                  @mousedown="fieldMousedown($event, x_index, y_index)"
                  @mouseup="fieldMouseup($event, x_index, y_index)"
                  :class="getClass(grid[x_index][y_index].field)">
                </div>
              </div>
            </div>  
            <GameCursor :usernames="usernames" :gamegridHTML="gamegridHTML" v-if="contentReady" />
          </div>
        </div>
        <div class="chat" v-if="contentReady">
          <Chat :usernames="usernames" :gamestate="gamestate" />
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
import Coordinate from '@/models/coordinate';
import { Field, GameState } from '@/models/enums';
import GameCursor from '@/components/GameCursor.vue';


@Component({
  components: {
    Chat,
    GameCursor
  },
})
export default class Game extends Vue {
  @Getter('GET_CURRENT_USER')
  currentUser!: User;

  @Action("ROOM_LEAVE")
  leaveRoom!: () => Promise<null>;

  @Action("ROOM_GET_SHOWN_FIELDS")
  room_getShownFields!: (user: User) => Promise<Coordinate[]>;

  @Action("ROOM_LISTEN_GAMESTATE")
  room_listengamestate!: (callback: (gamestate: GameState) => void) => Promise<null>;

  @Action("ROOM_LISTEN_USERSCONNECTED")
  room_listenUserConnected!: (callback: (usernames: string[]) => void) => Promise<null>;

  @Action("FIELD_LEFTCLICK")
  field_leftclick!: (coordinate: Coordinate) => Promise<null>;

  @Action("FIELD_RIGHTCLICK")
  field_rightclick!: (coordinate: Coordinate) => Promise<null>;

  @Action("FIELD_RIGHTLEFTCLICK")
  field_rightleftclick!: (coordinate: Coordinate) => Promise<null>;

  @Action("FIELD_LISTEN_CLICK")
  field_listenclick!: (callback: (grid: Coordinate[]) => void) => Promise<null>;

  Field = Field;
  GameState = GameState;
  contentReady: boolean = false;
  grid: GameBlock[][] = [];  
  gamestate: GameState = GameState.ACTIVE;
  usernames: String[] = [];
  
  mouseRightDown = false;
  mouseLeftDown = false;

  gamegridHTML!: HTMLElement;

  mounted(){
    if(!(this.currentUser && this.currentUser.room && this.currentUser.name && this.currentUser.room.roomname && this.currentUser.room.difficulty && this.currentUser.room.width && this.currentUser.room.height)){
        router.replace("/");
        return;
    } 
    for(let x=0;x<this.currentUser.room.width;x++){
      this.grid[x] = [];
      for(let y=0;y<this.currentUser.room.height;y++){
          this.grid[x][y] = new GameBlock();
      }
    }
    
    this.room_getShownFields(this.currentUser).then((coordinates: Coordinate[]) => {
      for(let i = 0;i<coordinates.length;i++){
        const gameblock = coordinates[i];
        const row = this.grid[gameblock.x];
        row[gameblock.y].field = gameblock.field;
        Vue.set(this.grid, gameblock.x, row);
      }
    });

    this.room_listengamestate((gamestate: GameState) => {
      this.gamestate = gamestate;
    });

    this.field_listenclick((coordinates: Coordinate[]) => {
      for(let i = 0;i<coordinates.length;i++){
        const gameblock = coordinates[i];
        const row = this.grid[gameblock.x];
        row[gameblock.y].field = gameblock.field;
        Vue.set(this.grid, gameblock.x, row);
      }
    });

    this.room_listenUserConnected((usernames: string[]) => {
      this.usernames = usernames;
    });

    this.gamegridHTML = this.$refs.gamegridHTML as HTMLElement;

    this.contentReady = true;
  }

  socketleave(){
    this.leaveRoom().then(()=>{
      router.replace("/");
    });
  }

  fieldMousedown(event: MouseEvent, x: number, y: number){
    const coordinate = new Coordinate();
    coordinate.x = x;
    coordinate.y = y;
    coordinate.roomname = this.currentUser.room.roomname;

    if(event.button === 0){
      this.mouseLeftDown = true;
    }
    if(event.button === 2){
      this.mouseRightDown = true;
    }
    if(this.mouseRightDown && !this.mouseLeftDown){
      this.field_rightclick(coordinate);
    }
  }
  fieldMouseup(event: MouseEvent, x: number, y: number){
    const coordinate = new Coordinate();
    coordinate.x = x;
    coordinate.y = y;
    coordinate.roomname = this.currentUser.room.roomname;

    if(this.mouseLeftDown && this.mouseRightDown){
      this.mouseLeftDown = false;
      this.mouseRightDown = false;
      this.field_rightleftclick(coordinate);
    }
    else{
      if(event.button === 0){
        this.mouseLeftDown = false;
        this.field_leftclick(coordinate);
      }
      if(event.button === 2){
        this.mouseRightDown = false;
      }
    }
  }

  getClass(field: Field){
    let fieldClass = "";
    if(field !== Field.BLOCK){
      if(field !== Field.FLAG){
        fieldClass += " clicked";
      }
      fieldClass += " n" + field.valueOf();
    }
    return fieldClass;
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
  height:730px;
}

.gamegrid{
  position: relative;
  width:820px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  overflow:hidden;
}
.gamerow{
  display: flex;
  flex-wrap: wrap;
  width:100%;
  justify-content: center;
}

.field{
  height: 32px;
  width: 32px;
  background-color: #87cefa;
  border-radius: 4px;
  margin : 1px;
  float: left;
  background-repeat: no-repeat;
  background-position: center;
  background-size: 24px 24px;
}
.field:hover:not(.clicked){
  background-color: #a4dcff;
}
.field.clicked{
  background-color: white;
  color: #87cefa;
}

.chat{
  height:730px;
  width:340px;
}

/* field image styles */
.field.n1{
  background-image: url(../../src/assets/images/1.svg);
}
.field.n2{
  background-image: url(../../src/assets/images/2.svg);
}
.field.n3{
  background-image: url(../../src/assets/images/3.svg);
}
.field.n4{
  background-image: url(../../src/assets/images/4.svg);
}
.field.n5{
  background-image: url(../../src/assets/images/5.svg);
}
.field.n6{
  background-image: url(../../src/assets/images/6.svg);
}
.field.n7{
  background-image: url(../../src/assets/images/7.svg);
}
.field.n8{
  background-image: url(../../src/assets/images/8.svg);
}
.field.n11{
  background-image: url(../../src/assets/images/11.svg);
}
.field.n12{
  background-image: url(../../src/assets/images/12.svg);
}

/*

bobler i top af chat for personer
rum ID I højre side  

*/

</style>