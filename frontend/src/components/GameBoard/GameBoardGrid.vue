<template>
  <div class="grid gap-1 grid-cols-[repeat(30,_minmax(0,_1fr))]">
    <GameBoardGridSquare
      v-for="(square, key) in squares"
      :key="key"
      v-bind="square"
      :flagStatus="flaggedSquares[key]"
      :disabled="!isAlive || isFinished"
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
  isAlive: {
    type: Boolean,
    required: false,
    default: true,
  },
  isFinished: {
    type: Boolean,
    required: false,
    default: false,
  },
  gameCode: {
    type: Number,
    required: true,
  },
});

defineEmits(["openSquare"]);

let flaggedSquares = reactive(
  JSON.parse(sessionStorage.getItem(`flaggedSquares:${props.gameCode}`)) || {}
);

function toggleFlag(coordinates) {
  /*
  Flags come in 3 types:
  0: unflagged
  1: flagged
  2: marked safe

  Every time toggleFlag is called, the flag type is incremented by 1, until it hits 3 and goes back to 0.
   */
  if (flaggedSquares.hasOwnProperty(coordinates)) {
    if (flaggedSquares[coordinates] === 2) {
      flaggedSquares[coordinates] = 0;
    } else {
      flaggedSquares[coordinates]++;
    }
  } else {
    flaggedSquares[coordinates] = 1;
  }
  sessionStorage.setItem(
    `flaggedSquares:${props.gameCode}`,
    JSON.stringify(flaggedSquares)
  );
}
</script>
