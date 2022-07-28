<template>
  <div>
    <div class="flex items-end place-content-between mb-8">
      <LogoV1 class="max-w-xs" />
      <p>Anybody's turn</p>
    </div>
    <GameBoardGrid />
  </div>
</template>

<script setup>
import GameBoardGrid from "@/components/GameBoard/GameBoardGrid.vue";
import LogoV1 from "@/components/logos/LogoV1.vue";
</script>
