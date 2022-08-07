<template>
  <div class="mt-20">
    <div class="text-center flex flex-col items-center">
      <h2 class="mb-2">Waiting for players...</h2>
      <p class="dark:text-gray-300 mb-6">
        Share this link with your friends to let them join the game:
      </p>
      <GameBoardWaitingCopy :copyText="joinUrl" />
    </div>
    <div class="flex justify-center mt-10">
      <LogoIcon class="max-w-[96px] animate-bounce" />
    </div>
  </div>
</template>

<script setup>
import LogoIcon from "@/components/logos/LogoIcon.vue";
import GameBoardWaitingCopy from "@/components/GameBoard/GameBoardWaitingCopy.vue";

const props = defineProps({
  gameCode: {
    type: Number,
    required: true,
  },
});

const joinUrl = `${window.location.host}/?game=${props.gameCode}`;
</script>
