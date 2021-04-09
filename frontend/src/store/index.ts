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
    CONNECT_SOCKET(){
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
    CREATE_ROOM(state, user: User){
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
    JOIN_ROOM(state, user: User){
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
    LEAVE_ROOM(state){
      return new Promise((resolve) => {
        socket.emit("leaveroom", () => {
          this.commit("SET_CURRENT_USER", new User());
          resolve(null);
        });
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