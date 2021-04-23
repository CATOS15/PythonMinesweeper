<template>
    <div class="content">
        <table>
            <tr>
                <th>Brugere</th>
                <th>Antal spillere</th>
                <th>Sværhedsgrad</th>
                <th>Tid</th>
            </tr>
            <tr v-for="(highscore, highscores_index) in highscores" :key="highscores_index">
                <th>{{highscore.usernames}}</th>
                <th>{{highscore.numberOfPlayers}}</th>
                <th>{{highscore.difficulty}}</th>
                <th>{{highscore.timer}}</th>
            </tr>
        </table>
    </div>
</template>

<script lang="ts">
import { Component, Vue} from 'vue-property-decorator';
import { Getter, Action } from 'vuex-class'
import Highscore from '@/models/highscore';
import SocketResponse from '@/models/socketResponse';

@Component({
  components: {
  },
})
export default class Highscores extends Vue{
    @Getter('IS_SOCKET_CONNECTED')
    isSocketConnected!: boolean;

    @Action("CONNECT_SOCKET")
    connectSocket!: () => Promise<SocketResponse>;

    @Action("GET_HIGHSCORES")
    getHighscores!: () => Promise<Highscore[]>;

    connectSocketLoading = false;
    highscores: Highscore[] = [];

    mounted(){
        if(this.isSocketConnected){
            this.loadHighscores();
            return;
        }
        this.connectSocketLoading = true;
        this.connectSocket().then((resp: SocketResponse) => {
            this.loadHighscores();
        }).catch((resp: SocketResponse) => {
            console.error(resp.msg);
        }).finally(() => {
            this.connectSocketLoading = false;
        });
    }

    loadHighscores(){
        this.getHighscores().then((highscores: Highscore[]) => {
            this.highscores = highscores;
            this.highscores = this.highscores.sort((a, b) => {
                return a.timer > b.timer ? 1 : -1;
            });
        });
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

.highscore_container{
    background:yellow;
    width:100px;
    height:100px;
}

table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
}

</style>