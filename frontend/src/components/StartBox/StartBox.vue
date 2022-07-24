<template>
  <div
    class="min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2>BugSweeper</h2>
        <p class="mt-1 text-center font-mono dark:text-slate-500">PLAY NOW</p>
      </div>
      <form class="mt-8 space-y-6" action="#" method="POST">
        <div class="rounded-md shadow-sm -space-y-px">
          <label for="nickname" class="sr-only">Nickname</label>
          <input
            id="nickname"
            name="nickname"
            type="text"
            autocomplete="nickname"
            placeholder="Nickname"
            required
          />
          <label for="game-code" class="sr-only">Game code</label>
          <input
            id="game-code"
            ref="game-code"
            name="game-code"
            type="number"
            autocomplete="off"
            placeholder="Game code"
            class="pr-28 inline"
            required
          />
          <a
            href="#"
            @click="$refs['game-code'].value = generateGameCode()"
            style="margin-left: -94px"
            class="font-mono relative z-50 text-blue-600 hover:text-blue-700 dark:hover:text-blue-500"
            >NEW GAME</a
          >
        </div>
        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 dark:bg-blue-600 hover:bg-blue-700 dark:hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Join
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
function generateGameCode() {
  return Math.floor(Math.random() * 90000) + 10000;
  // TODO: Ensure that the game code never collides with already existing games
}
</script>
