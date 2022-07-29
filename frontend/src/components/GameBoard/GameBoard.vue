<template>
  <div>
    <div class="flex items-end place-content-between mb-8">
      <LogoV1 class="max-w-xs" />
      <div class="text-right dark:text-gray-200">
        <p>{{ Object.keys(gameState.value?.players || {}).length }} players</p>
        <p>Anybody's turn</p>
      </div>
    </div>
    <GameBoardGrid :squares="gameState.value?.squares || {}" @openSquare="(coordinates) => $emit('openSquare', coordinates)" />
  </div>
</template>

<script setup>
import GameBoardGrid from "@/components/GameBoard/GameBoardGrid.vue";
import LogoV1 from "@/components/logos/LogoV1.vue";

const props = defineProps({
  gameState: {
    type: Object,
    required: true,
  },
})

defineEmits(["openSquare"])
</script>
