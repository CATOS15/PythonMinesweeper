import Vue from 'vue'
import Vuex, { StoreOptions } from 'vuex'
import { SocketState } from './statetypes'

Vue.use(Vuex)

const storeOptions: StoreOptions<SocketState> = {
  state: {
  },
  actions: {
  },
  mutations: {
  },
  getters: {
  }
}

export default new Vuex.Store<SocketState>(storeOptions);