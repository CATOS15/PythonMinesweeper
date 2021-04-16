<template>
  <div class="app">
    <div class="gamecontainer">
      <router-view  />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {
  },
})

export default class App extends Vue {
}
</script>

<style lang="less">
@font-face {
  font-family: Montserrat;
  src: url(../src/assets/fonts/Montserrat-Regular.ttf);
}

* {
  margin:0;
  padding:0;
  font-family: Montserrat;
  color: #BABABA;
  letter-spacing: 0.2px;
}

html, body, .app{
  margin: auto;
  width: 100%;
  height: 100%;
  background-image: url(../src/assets/background.png);
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center center;
}

input{
  border-radius: 30px;
  padding: 10px 18px;
  width: 100%;
  min-width: 100px;
  margin: 5px 0;
  color: white;
  background: #bababa;
  border: none;
}

button{
  border-radius: 20px !important;
  padding: 10px 14px;
  margin: 5px 0 !important;
  color: white;
  background: #0f80a4;
  border: none;
}
button:not(:last-child){
  margin-right:10px !important;
}
button:disabled{
  opacity: 0.65;
  color: #bababa;
}
input:focus, button:focus{
  outline: none;
}

.routerLinks > a{
  margin-left:5px;
}

.gamecontainer{
  height:100%;
}

.backgroundYellow{
  background-color: #8a8c2e;
}
.backgroundGreen{
  background-color: #2e8c55;
}
.backgroundRed{
  background-color: #eb5757;
}
.backgroundDarkBlue{
  background-color: #112c49;
}

/* width */
::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1; 
}
 
/* Handle */
::-webkit-scrollbar-thumb {
  background: #888; 
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555; 
}

</style>