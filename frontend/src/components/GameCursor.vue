<template>
  <div>
    <!-- <div v-for="(userCursor, index) in userCursors" :key="index">
        supermand
    </div> -->
    <div v-for="(userCursor, index) in userCursors" :key="index" class="cursor" :style="{'left' : userCursor.left + 'px', 'top' : userCursor.top + 'px'}">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cursor-fill" viewBox="0 0 16 16">
        <path d="M14.082 2.182a.5.5 0 0 1 .103.557L8.528 15.467a.5.5 0 0 1-.917-.007L5.57 10.694.803 8.652a.5.5 0 0 1-.006-.916l12.728-5.657a.5.5 0 0 1 .556.103z" 
            transform="scale(-1,1) translate(-16,0)" 
            :style="{'fill': '#ff0000'}" />
      </svg>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
import { Getter, Action } from 'vuex-class';
import User, { UserCursor } from '@/models/user';

@Component
export default class GameCursor extends Vue {
  @Getter('GET_CURRENT_USER')
  currentUser!: User;
  
  @Action("CURSOR_SEND_USERCURSOR")
  cursor_sendUsercursor!: (userCursor: UserCursor) => Promise<string>;

  @Action("CURSOR_LISTEN_USERCURSOR")
  cursor_listenUsercursor!: (callback: (userCursor: UserCursor) => void) => Promise<null>;

  @Prop({required: true})
  usernames!: string[];

  @Prop({required: true})
  gamegridHTML!: HTMLElement;

  gamegridHTMLOffsetLeft: number = 0;
  gamegridHTMLOffsetTop: number = 0;

  userCursorsMap: Map<string, UserCursor> = new Map<string, UserCursor>();
  userCursors: UserCursor[] = [];

  userCursor: UserCursor = new UserCursor();

  @Watch("usernames")
  usernamesChange(){
    const newUserCursorsMap = new Map<string, UserCursor>();
    for(const username in this.usernames){
      const userCursor = this.userCursorsMap.get(username);
      if(userCursor){
        newUserCursorsMap.set(username, userCursor);
      }
    }
    this.userCursorsMap = newUserCursorsMap;
    this.userCursors = Array.from(this.userCursorsMap.values());
  }

  mounted(){
    this.gamegridHTMLOffsetLeft = this.gamegridHTML.offsetLeft;
    this.gamegridHTMLOffsetTop = this.gamegridHTML.offsetTop;
    this.userCursor.name = this.currentUser.name;
    this.userCursor.roomname = this.currentUser.room.roomname;

    window.addEventListener('resize', () => {
      this.gamegridHTMLOffsetLeft = this.gamegridHTML.offsetLeft;
      this.gamegridHTMLOffsetTop = this.gamegridHTML.offsetTop;
    });

    this.gamegridHTML.addEventListener("mousemove", (event: MouseEvent) => {
      this.userCursor.left = event.pageX - this.gamegridHTMLOffsetLeft;
      this.userCursor.top = event.pageY - this.gamegridHTMLOffsetTop;
      this.cursor_sendUsercursor(this.userCursor);
    });

    this.cursor_listenUsercursor((userCursor: UserCursor) => {
      if(userCursor.name == this.currentUser.name){
        return;
      }
      this.userCursorsMap.set(userCursor.name, userCursor);
      this.userCursors = Array.from(this.userCursorsMap.values());
    });
  }
}
</script>

<style scoped lang="less">
  .cursor{
    position: absolute;
  }
  .cursor > div{
    color:black;
  }
</style>