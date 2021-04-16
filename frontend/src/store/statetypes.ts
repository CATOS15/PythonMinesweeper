import User from "@/models/user";
import { Socket } from "socket.io-client";

export interface SocketState{
    currentUser: User;
}