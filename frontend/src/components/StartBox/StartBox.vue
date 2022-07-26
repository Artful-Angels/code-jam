<template>
  <div
    class="min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8"
  >
    <main class="max-w-md w-full space-y-8">
      <div class="mb-12">
        <logo-v1 class="hidden sm:block" />
        <logo-v2 class="sm:hidden" />
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="submitGame">
        <div class="rounded-md shadow-sm -space-y-px">
          <label for="nickname" class="sr-only">Nickname</label>
          <input
            id="nickname"
            name="nickname"
            type="text"
            autocomplete="nickname"
            placeholder="Nickname"
            v-model="nickname"
            required
          />
          <label for="game-code" class="sr-only">Game code</label>
          <input
            id="game-code"
            ref="game-code"
            name="game_code"
            type="number"
            autocomplete="off"
            placeholder="Game code"
            class="pr-28 inline"
            v-model="gameCode"
            required
          />
          <a
            href="#"
            @click="updateGameCode(this.$refs['game-code'])"
            style="margin-left: -94px"
            class="font-mono relative z-50 text-blue-600 hover:text-blue-700 dark:hover:text-blue-500"
            >NEW GAME</a
          >
        </div>
        <div>
          <button
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 dark:bg-blue-600 hover:bg-blue-700 dark:hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Join
          </button>
        </div>
      </form>
    </main>
  </div>
</template>

<script setup>
import LogoV1 from "@/components/logos/LogoV1.vue";
import LogoV2 from "@/components/logos/LogoV2.vue";

let nickname = undefined
let gameCode = undefined

function updateGameCode(element) {
  const event = new Event('input')
  element.value = generateGameCode()
  element.dispatchEvent(event)
}

function generateGameCode() {
  return Math.floor(Math.random() * 90000) + 10000;
  // TODO: Ensure that the game code never collides with already existing games
}

function submitGame() {
}
</script>
