<template>
  <div class="h-full">
    <div class="flex items-end place-content-between mb-8">
      <LogoV1 class="max-w-xs" />
      <div class="text-right dark:text-gray-200">
        <p>{{ Object.keys(gameState.value?.players || {}).length }} players</p>
        <p>Anybody's turn</p>
      </div>
    </div>
    <GameBoardGrid
      v-if="gameStarted"
      :squares="gameState.value?.squares || {}"
      @openSquare="(coordinates) => $emit('openSquare', coordinates)"
    />
    <div v-else>
      <GameBoardWaiting class="w-full flex flex-col justify-center" :game-code="gameCode" />
    </div>
  </div>
</template>

<script setup>
import GameBoardGrid from "@/components/GameBoard/GameBoardGrid.vue";
import LogoV1 from "@/components/logos/LogoV1.vue";
import GameBoardWaiting from "@/components/GameBoard/GameBoardWaiting.vue";

const props = defineProps({
  gameCode: {
    type: Number,
    required: true,
  },
  gameState: {
    type: Object,
    required: true,
  },
  gameStarted: {
    type: Boolean,
    required: false,
    default: false,
  },
});

defineEmits(["openSquare"]);
</script>
