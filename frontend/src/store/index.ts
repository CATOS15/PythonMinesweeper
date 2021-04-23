import ChatMessage from '@/models/chatMessage'
import Coordinate from '@/models/coordinate'
import { GameState } from '@/models/enums'
import Highscore from '@/models/highscore'
import SocketResponse from '@/models/socketResponse'
import User, { Room, UserCursor } from '@/models/user'
import { io, Socket, SocketOptions } from 'socket.io-client'
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
        socket = io('ws://' + location.hostname + ':5005', {transports: ["websocket"]});
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
    GET_HIGHSCORES(state){
      return new Promise((resolve) => {
        socket.emit("getHighscores", (resp: string) => {
          const socketResponse = JSON.parse(resp) as SocketResponse;
          if(socketResponse.success){
            const highscore = JSON.parse(socketResponse.msg) as Highscore[];
            resolve(highscore);
          }
        });
      });
    },
    ROOM_CREATE(state, user: User){
      return new Promise((resolve) => {
        socket.emit("createroom", JSON.stringify(user), (resp: string) => {
          const socketResponse = JSON.parse(resp) as SocketResponse;
          if(socketResponse.success){
            const room = JSON.parse(socketResponse.msg);
            user.room.height = room.height;
            user.room.width = room.width;
            user.room.timer = room.timer;
            user.room.flags = room.flags;
            user.room.gamestate = room.gamestate;
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
            const room = JSON.parse(socketResponse.msg);
            user.room.height = room.height;
            user.room.width = room.width;
            user.room.timer = room.timer;
            user.room.flags = room.flags;
            user.room.gamestate = room.gamestate;
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
        socket.emit("refreshUsersConnected", JSON.stringify(user), () => {
          resolve(null);
        });
      });
    },
    ROOM_GET_SHOWN_FIELDS(state, user: User){
      return new Promise((resolve) => {
        socket.emit("getshownfields", JSON.stringify(user), (resp: string) => {
          const socketResponse = JSON.parse(resp) as SocketResponse;
          if(socketResponse.success){
            const grid = JSON.parse(socketResponse.msg) as Coordinate[];
            resolve(grid);
          }
        });
      });
    },
    ROOM_LISTEN_USERSCONNECTED(state, callback: (usernames: string[]) => void){
      socket.on("emitUsersConnected", (resp: string) => {
        const usernames = JSON.parse(resp) as string[];
        callback(usernames);
      });
    },
    ROOM_LISTEN_GAMESTATE(state, callback: (gamestate: GameState) => void){
      socket.on("emitGamestate", (gamestate: GameState) => {
        callback(gamestate);
      });
    },
    ROOM_GET_TIME(state, user: User){
      return new Promise((resolve) => {
        socket.emit("gettime", JSON.stringify(user), (resp: string) => {
          const socketResponse = JSON.parse(resp) as SocketResponse;
          if(socketResponse.success){
            const timer = JSON.parse(socketResponse.msg) as number;
            resolve(timer);
          }
        });
      });
    },
    FIELD_RIGHTLEFTCLICK(state, coordinate: Coordinate){
      return new Promise((resolve) => {
        socket.emit("rightleftClick", JSON.stringify(coordinate), () => {
          resolve(null);
        });
      });
    },
    FIELD_RIGHTCLICK(state, coordinate: Coordinate){
      return new Promise((resolve) => {
        socket.emit("rightClick", JSON.stringify(coordinate), () => {
          resolve(null);
        });
      });
    },
    FIELD_LEFTCLICK(state, coordinate: Coordinate){
      return new Promise((resolve) => {
        socket.emit("leftClick", JSON.stringify(coordinate), () => {
          resolve(null);
        });
      });
    },
    FIELD_LISTEN_CLICK(state, callback: (grid: Coordinate[]) => void){
      socket.on("emitClick", (resp: string) => {
        const grid = JSON.parse(resp) as Coordinate[];
        callback(grid);
      });
    },
    CHAT_SENDMESSAGE(state, message: ChatMessage){
      return new Promise((resolve) => {
        socket.emit("sendmessage", JSON.stringify(message), (resp: string) => {
          resolve(resp);
        });
      });
    },
    CHAT_LISTEN_MESSAGE(state, callback: (chatMessage: ChatMessage) => void){
      socket.on("emitMessage", (resp: string) => {
        const chatMessage = JSON.parse(resp) as ChatMessage;
        callback(chatMessage);
      });
    },
    CURSOR_SEND_USERCURSOR(state, userCursor: UserCursor){
      return new Promise((resolve) => {
        socket.emit("sendusercursor", JSON.stringify(userCursor), () => {
          resolve(null);
        });
      });
    },
    CURSOR_LISTEN_USERCURSOR(state, callback: (userCursors: UserCursor) => void){
      socket.on("emitUserCursor", (resp: string) => {
        const userCursor = JSON.parse(resp) as UserCursor;
        callback(userCursor);
      });
    },
  },
  mutations: {
    SET_CURRENT_USER(state, user: User){
      state.currentUser = user;
    }
  },
  getters: {
    GET_CURRENT_USER(state){
      return state.currentUser;
    },
    IS_SOCKET_CONNECTED(state){
      return socket && socket.connected;
    }
  }
}

export default new Vuex.Store<SocketState>(storeOptions);