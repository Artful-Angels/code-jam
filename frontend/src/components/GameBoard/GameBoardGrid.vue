<template>
  <div class="grid gap-1 grid-cols-[repeat(30,_minmax(0,_1fr))]">
    <GameBoardGridSquare
      v-for="square in squares"
      :key="square.coordinates"
      v-bind="square"
      :isFlagged="flaggedSquares[square.coordinates]"
      @toggleFlag="(coordinates) => toggleFlag(coordinates)"
    />
  </div>
</template>

<script setup>
import GameBoardGridSquare from "@/components/GameBoard/GameBoardGridSquare.vue";
import { reactive } from "vue";

const props = defineProps({
  squares: {
    type: Object,
    required: true,
  },
})

let flaggedSquares = reactive({});

function toggleFlag(coordinates) {
  if (flaggedSquares.hasOwnProperty(coordinates)) {
    flaggedSquares[coordinates] = flaggedSquares[coordinates] === false;
  } else {
    flaggedSquares[coordinates] = true
  }
}
</script>
