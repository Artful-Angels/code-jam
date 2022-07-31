<template>
  <div class="h-full">
    <div class="flex items-end place-content-between mb-8">
      <LogoV1 class="max-w-xs" />
      <div class="text-right dark:text-gray-200">
        <p class="text-lg font-semibold">
          <span v-if="alivePlayers.length > 0 || deadPlayers.length === 0">
            <img
              src="https://raw.githubusercontent.com/twitter/twemoji/master/assets/svg/1f9d1.svg"
              alt="Players emoji"
              class="w-8 inline"
            />
            {{ alivePlayers.length }}
          </span>
          <span v-if="deadPlayers.length > 0" class="ml-5">
            <img
              src="https://raw.githubusercontent.com/twitter/twemoji/master/assets/svg/1f480.svg"
              alt="Skull emoji"
              class="w-7 inline"
            />
            {{ deadPlayers.length }}
          </span>
        </p>
        <!-- <p>Anybody's turn</p> -->
      </div>
    </div>
    <GameBoardGrid
      v-if="gameStarted"
      :squares="gameState.value?.squares || {}"
      :isAlive="alivePlayers.includes(nickname)"
      @openSquare="(coordinates) => $emit('openSquare', coordinates)"
    />
    <div v-else>
      <GameBoardWaiting
        class="w-full flex flex-col justify-center"
        :game-code="gameCode"
      />
    </div>
    <div v-if="gameStarted" class="mt-5 text-center uppercase text-xl font-mono font-semibold">
      <p v-if="isAlive" class="text-blue-600">Alive</p>
      <p v-else class="text-red-600">Dead</p>
    </div>
  </div>
</template>

<script setup>
import GameBoardGrid from "@/components/GameBoard/GameBoardGrid.vue";
import LogoV1 from "@/components/logos/LogoV1.vue";
import GameBoardWaiting from "@/components/GameBoard/GameBoardWaiting.vue";
import { computed, watch } from "vue";

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
  nickname: {
    type: String,
    required: true,
  },
});

const alivePlayers = computed(() => {
  if (props.gameState.value?.players === undefined) return [];
  return Object.keys(props.gameState.value.players).filter(
    (playerName) => props.gameState.value.players[playerName].is_alive
  );
});

const deadPlayers = computed(() => {
  if (props.gameState.value?.players === undefined) return [];
  return Object.keys(props.gameState.value.players).filter(
    (playerName) => !props.gameState.value.players[playerName].is_alive
  );
});

const isAlive = computed(() => {
  if (props.gameState.value?.players === undefined) return true;
  return props.gameState.value.players[props.nickname].is_alive;
});

watch(deadPlayers, (newValue, oldValue) => {
  if (oldValue.length !== newValue.length) {
    const deadPlayer = newValue.filter((x) => !oldValue.includes(x))[0];
    emits("playerDied", deadPlayer);
  }
});

const emits = defineEmits(["openSquare", "playerDied"]);
</script>
