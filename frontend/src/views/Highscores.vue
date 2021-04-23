<template>
    <div class="content">
        <div class="highscore_container">
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>Brugere</th>
                        <th>Antal spillere</th>
                        <th>Sværhedsgrad</th>
                        <th>Tid</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(highscore, highscores_index) in highscores" :key="highscores_index">
                        <td>{{highscore.usernames}}</td>
                        <td>{{highscore.numberOfPlayers}}</td>
                        <td>{{highscore.difficulty}}</td>
                        <td>{{highscore.timer}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
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
    border-radius:10px;
}

.styled-table {
    border-collapse: collapse;
    margin: 25px 0;
    font-size: 0.9em;
    font-family: sans-serif;
    min-width: 300px;
    max-width:800px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    border-radius: 10px;
    -moz-border-radius:10px;
}

.styled-table thead tr {
    background-color: #0f80a4;
    color: #ffffff;
    text-align: left;
}

.styled-table th,
.styled-table td {
    padding: 12px 15px;
}

.styled-table th{
    color:white;
}

.styled-table td{
    color:black;
}

.styled-table tbody tr {
    border-bottom: 1px solid #dddddd;
}

.styled-table tbody tr:nth-of-type(odd) {
    background-color: #FFFFFF;
}

.styled-table tbody tr:nth-of-type(even) {
    background-color: #f3f3f3;
}

.styled-table tbody tr:last-of-type {
    border-bottom: none;
}

/* rounded borders */
th:first-of-type {
  border-top-left-radius: 10px;
}
th:last-of-type {
  border-top-right-radius: 10px;
}
tr:last-of-type td:first-of-type {
  border-bottom-left-radius: 10px;
}
tr:last-of-type td:last-of-type {
  border-bottom-right-radius: 10px;
}

/*
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

*/


</style>