<template>
  <div class="grid gap-1 grid-cols-[repeat(30,_minmax(0,_1fr))]">
    <GameBoardGridSquare
      v-for="(square, key) in squares"
      :key="key"
      v-bind="square"
      :isFlagged="flaggedSquares[key]"
      @toggleFlag="(coordinates) => toggleFlag(key)"
      @openSquare="(coordinates) => $emit('openSquare', coordinates)"
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
});

defineEmits(["openSquare"]);

let flaggedSquares = reactive({});

function toggleFlag(coordinates) {
  console.log(coordinates)
  if (flaggedSquares.hasOwnProperty(coordinates)) {
    flaggedSquares[coordinates] = flaggedSquares[coordinates] === false;
  } else {
    flaggedSquares[coordinates] = true;
  }
}
</script>
