<template>
  <div class="chatcontent">
    <div class="playerscontainer" >
      <div v-for="(username,username_index) in usernames" :key="username_index">
        <div class="playercircle unselectable" :title="username" :class="{'active':currentUser.name.toLowerCase() == username.toLowerCase()}">{{username[0].toUpperCase()}}</div>
      </div>
    </div>
    <div class="messagescontainer" dir="ltr">
      <div v-for="(chatmessage,chatmessage_index) in chatmessages" :key="chatmessage_index">
        <b>{{chatmessage.username}}: </b>
        <span>{{chatmessage.message}}</span>
      </div>
    </div>
    <div class="inputcontainer">
      <div class="chatinput">
        <input type="text" v-model="message" @keyup.enter="sendMessage(message)" placeholder="Indtast besked..." />
        <button @click="sendMessage(message)">
          <svg width="24" height="24" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Getter, Action } from 'vuex-class';
import User from '@/models/user';
import ChatMessage from '@/models/chatMessage';
import SocketResponse from '@/models/socketResponse';

@Component
export default class Chat extends Vue {
  @Getter('GET_CURRENT_USER')
  currentUser!: User;

  @Action("ROOM_REFRESH_USERSCONNECTED")
  room_refreshUsersConnected!: (user: User) => Promise<SocketResponse>;

  @Action("ROOM_LISTEN_USERSCONNECTED")
  room_listenUserConnected!: (callback: (usernames: string[]) => void) => Promise<null>;

  @Action("CHAT_SENDMESSAGE")
  chat_sendMessage!: (chatMessage: ChatMessage) => Promise<string>;

  @Action("CHAT_LISTEN_MESSAGE")
  chat_listenMessage!: (callback: (chatMessage: ChatMessage) => void) => Promise<null>;
  
  message: string = '';

  usernames: String[] = [];

  chatmessages: ChatMessage[] = [];

  mounted(){
    this.chat_listenMessage((chatMessage: ChatMessage) => {
      this.chatmessages.push(chatMessage);
      this.message = '';
    });
    this.room_listenUserConnected((usernames: string[]) => {
      this.usernames = usernames;
    });
    this.room_refreshUsersConnected(this.currentUser);
  }

  sendMessage(message: string){
    if(message.length === 0){
      return;
    }

    const chatMessage = new ChatMessage();
    chatMessage.username = this.currentUser.name;
    chatMessage.message = message;
    chatMessage.time = new Date();
    chatMessage.roomname = this.currentUser.room.roomname;
    this.chat_sendMessage(chatMessage);
  }
}

</script>

<style scoped lang="less">

.chatcontent{
  display:flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
}

.playerscontainer{
  display:flex;
  flex-direction: row-reverse;
  overflow: hidden;
  width:100%;
  margin-bottom: 10px;
}

.playercircle{
  height: 35px;
  width: 35px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
  margin: 0 3px;
  color: white;
  display:flex;
  justify-content: center;
  align-items: center;
  font-weight: 900;
  padding: 1px 0 0 1px;
}

.playercircle.active{
  background-color:red;
}

.playercircle:nth-of-type(even) {
  background-color: #666;
}

.messagescontainer{
  width:100%;
  height:500px;
  background-color:#0000004a;
  padding: 5px 10px;
  border-radius: 10px;
  margin: 0 0 10px 0; 
  overflow:auto;
  scroll-snap-type: y mandatory;
  scrollbar-gutter: always;
}

.messagescontainer > div{
  margin-bottom: 6px;
  line-height: 21px;
  word-wrap: break-word;
}

.inputcontainer{
  width:100%;
  background-color: #0000004a;
  border-radius:10px ;
}

.unselectable {
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

.chatinput {
  display:flex;
  flex-direction:row;
  align-items: center;
  padding-right:5px;
  border-radius:20px;
}

.chatinput input {
  flex-grow:2;
  border:none;
  background: none;
  padding-top: 13px;
}

.chatinput input:focus {
  outline: none;
}

.chatinput button {
  height: 30px;
  padding: 0;
  width: 60px;
  background:#112c49;
}

.chatinput button path {
  color:white;
}


::-webkit-scrollbar {
    width: 18px;
    height: 18px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0);
  margin-top:14px;
  margin-bottom:14px;
}
 
::-webkit-scrollbar-thumb {
  height: 6px;
    border-right: 9px solid rgba(0, 0, 0, 0);
    border-left: 4px solid rgba(0, 0, 0, 0);
    background-clip: padding-box;
    background-color: rgba(0, 0, 0, 0.45);
}

::-webkit-scrollbar-corner {
    background-color: transparent;
}
</style>