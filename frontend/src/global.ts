import { Socket } from "socket.io-client";
import Vue from "vue";
import User from "./models/user";

interface Global {
    currentSocket: Socket | null;
    currentUser: User;
}

export const GLOBAL = new Vue({
    data: {
        currentSocket: null,
        currentUser: new User()
    } as Global
});