import ChatMessage from '@/models/chatMessage'
import SocketResponse from '@/models/socketResponse'
import User from '@/models/user'
import { io, Socket } from 'socket.io-client'
import Vue from 'vue'
import Vuex, { StoreOptions } from 'vuex'
import { SocketState } from './statetypes'

Vue.use(Vuex)

let socket: Socket;

const storeOptions: StoreOptions<SocketState> = {
  state: {
    currentUser: new User()
  },
  actions: {
    CONNECT_SOCKET(state){
      return new Promise((resolve, reject) => {
        socket = io('ws://' + location.hostname + ':5005');
        socket.on('connect', () => {
          const socketResponse = new SocketResponse();
          socketResponse.msg = "Forbindelse til socket oprettet";
          socketResponse.success = true;
          resolve(socketResponse);
        });
        socket.on('connect_failed', () => {
          const socketResponse = new SocketResponse();
          socketResponse.msg = "Forbindelsen til socket kunne ikke oprettes";
          socketResponse.success = false;
          reject(socketResponse);
        });
      });
    },
    ROOM_CREATE(state, user: User){
      return new Promise((resolve) => {
        socket.emit("createroom", JSON.stringify(user), (resp: string) => {
          const socketResponse = JSON.parse(resp) as SocketResponse;
          if(socketResponse.success){
            this.commit("SET_CURRENT_USER", user);
          }
          resolve(socketResponse);
        });
      });
    },
    ROOM_JOIN(state, user: User){
      return new Promise((resolve) => {
        socket.emit("joinroom", JSON.stringify(user), (resp: string) => {
          const socketResponse = JSON.parse(resp) as SocketResponse;
          if(socketResponse.success){
            this.commit("SET_CURRENT_USER", user);
          }
          resolve(socketResponse);
        });
      });
    },
    ROOM_LEAVE(state){
      return new Promise((resolve) => {
        socket.emit("leaveroom", () => {
          this.commit("SET_CURRENT_USER", new User());
          resolve(null);
        });
      });
    },
    ROOM_REFRESH_USERSCONNECTED(state, user: User){
      return new Promise((resolve) => {
        socket.emit("refreshUsersconnected", JSON.stringify(user), () => {
          resolve(null);
        });
      });
    },
    ROOM_LISTEN_USERSCONNECTED(state, callback: (usernames: string[]) => void){
      socket.on("emitUsersconnected", (resp: string) => {
        const usernames = JSON.parse(resp) as string[];
        callback(usernames);
      });
    },
    CHAT_SENDMESSAGE(state, message: String){
      return new Promise((resolve) => {
        socket.emit("sendmessage", JSON.stringify(message), (resp: string) => {
          console.log(resp);
          resolve(resp);
        });
      });
    },
    CHAT_LISTEN_MESSAGE(state, callback: (chatMessage: ChatMessage) => void){
      socket.on("emitMessage", (resp: string) => {
        const chatMessage = JSON.parse(resp) as ChatMessage;
        callback(chatMessage);
      });
    }
  },
  mutations: {
    SET_CURRENT_USER(state, user: User){
      //TODO: Slet når backend returnerer højde og bredde
      user.room.width = 20;
      user.room.height = 15;
      state.currentUser = user;
    }
  },
  getters: {
    GET_CURRENT_USER(state){
      return state.currentUser;
    }
  }
}

export default new Vuex.Store<SocketState>(storeOptions);