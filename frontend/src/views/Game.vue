<template>
  <div>
      <div class="game">
        {{game}}
      </div>
      <div class="chat" @mousemove="mousemove($event)">
        <Chat name="game" />
      </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Chat from '@/components/Chat.vue'

@Component({
  components: {
    Chat
  },
})
export default class Game extends Vue {
    name = "Olli";
    game = "Her er spilområdet";

    mousemove(event: MouseEvent){
      console.log("X: " + event.offsetX + " Y: " + event.offsetY);
    }
}
</script>

<style scoped>

.game{
  width:calc(100% - 200px);
  height:100%;
  float:left;
}

.chat{
  width:200px;
  height:100%;
  float:left;
}
</style>