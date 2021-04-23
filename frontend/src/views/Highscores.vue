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
    width:auto;
}

.styled-table {
    min-width: 800px;
    width: 800px;
    max-width: 800px;
    font-size: 0.9em;
    display:block;
    table-layout: fixed;
    border-collapse: collapse;
    margin:auto;
}

/* fiks at der kan være en scrollbar, pølse*/
.styled-table thead{
    position: relative;
    display: block;
}

.styled-table tbody{
    display:block;
    overflow-y:scroll;
    overflow-x:hidden;
    height:200px;
    border-radius:0px 0px 0px 10px;
}

.styled-table td{
    overflow:auto;
}

/* gud = https://www.tjvantoll.com/2012/11/10/creating-cross-browser-scrollable-tbody/ */
.styled-table td:nth-child(1), .styled-table th:nth-child(1) { min-width: 410px; max-width:410px; }
.styled-table td:nth-child(2), .styled-table th:nth-child(2) { min-width: 130px; }
.styled-table td:nth-child(3), .styled-table th:nth-child(3) { min-width: 150px; }
.styled-table td:nth-child(4), .styled-table th:nth-child(4) { width: 300px; }

/* scrollbar styling (om den skal være rund eller firkantet) */
::-webkit-scrollbar {
    border-radius: 0 0 100px 0;
    height: 18px;
    width:10px;
    background-color: white;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0);
    border-radius: 0 0 10px 0;
    margin-top:2px;
    margin-bottom:5px;
    padding-right:10px;
}

::-webkit-scrollbar-thumb {
    border-right: 3px solid rgba(0, 0, 0, 0);
    border-left: 3px solid rgba(0, 0, 0, 0);
    background-clip: padding-box;
    background-color: rgba(0, 0, 0, 0.45);
    border-radius:100px;
}

::-webkit-scrollbar-corner {
    background-color: transparent;
}

/* horizontal scrollbar if names to long */

::-webkit-scrollbar:horizontal {
    height: 1px;
    background-color: white;
}

::-webkit-scrollbar-track:horizontal {
    background: rgba(0, 0, 0, 0);
    
}

::-webkit-scrollbar-thumb:horizontal {
    background-clip: padding-box;
    border-radius:100px;
    border-right: 0px solid rgba(0, 0, 0, 0);
    border-left: 0px solid rgba(0, 0, 0, 0);
}

::-webkit-scrollbar-corner:horizontal {
    background-color: transparent;
}

/* colors and distinction between rows*/
.styled-table th,
.styled-table td {
    padding: 12px 15px;
}

.styled-table thead tr {
    background-color: #0f80a4;
    color: #ffffff;
    text-align: left;
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
  /*border-bottom-right-radius: 10px;*/
}

</style>