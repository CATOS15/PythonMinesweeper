<template>
  <div class="chatcontent">
    <div class="playerscontainer gradientbackground" >
      <div v-for="(username,username_index) in usernames" :key="username_index">
        <div class="playercircle unselectable" :title="username" :class="{'active':currentUser.name.toLowerCase() == username.toLowerCase()}">{{username[0].toUpperCase()}}</div>
      </div>
    </div>
    <div class="messagescontainer gradientbackground" dir="ltr">
      <div v-for="(chatmessage,chatmessage_index) in chatmessages" :key="chatmessage_index">
        <p>
          <b>{{chatmessage.username}}: </b>
          <span>{{chatmessage.message}}</span>
        </p>
      </div>
    </div>
    <div class="inputcontainer">
      <div class="chatinput gradientbackground">
        <input type="text" v-model="message" @keyup.enter="sendMessage(message)">
        <button @click="sendMessage(message)">Go</button>
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

/* players */
.playerscontainer{
  display:flex;
  width:100%;
  height: 45px;
  overflow: hidden;
  flex-direction: row-reverse;
  align-items: center;
  justify-content: center;
  padding:5px 0;
  border-radius:20px ;
  margin:0 0 10px 0;
}

.gradientbackground{
  background-image: url(../../src/assets/background.png);
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center center;
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

/* messages */
.messagescontainer{
  width:100%;
  height:500px;
  background-color:#444;
  padding: 5px 0px 5px 10px;
  border-radius:20px ;
  margin: 0 0 10px 0; 
  overflow:auto;
  scroll-snap-type: y mandatory;
  scrollbar-gutter: always;
}

.messagescontainer > div{
  box-sizing:border-box;
}

.messagescontainer > * p{
  margin-bottom: 0px;
  word-wrap: break-word;
}

/* input */
.inputcontainer{
  width:100%;
  height:50px;
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
  /* This bit sets up the horizontal layout */
  display:flex;
  flex-direction:row;
 
  /* I've used padding so you can see the edges of the elements. */
  padding:2px;
  padding-right:5px;
  border-radius:20px;
}

input {
  /* Tell the input to use all the available space */
  flex-grow:2;
  /* And hide the input's outline, so the form looks like the outline */
  border:none;
  background: none;
}

input:focus {
  /* removing the input focus blue box. Put this on the form if you like. */
  outline: none;
}

button {
  /* Just a little styling to make it pretty */
  background:#112c49;
  color:white;
}


/* https://stackoverflow.com/questions/23200639/transparent-scrollbar-with-css/56365213 */
/* */
/* width */
::-webkit-scrollbar {
    width: 18px;
    height: 18px;
}

/* Track */
::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0);
  margin-top:14px;
  margin-bottom:14px;
}
 
/* Handle */
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
