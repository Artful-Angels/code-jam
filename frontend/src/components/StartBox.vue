<template>
  <div
    class="min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8"
  >
    <main class="max-w-md w-full space-y-8">
      <div class="mb-12">
        <logo-v1 class="hidden sm:block" />
        <logo-v2 class="sm:hidden" />
      </div>
      <form
        class="mt-8 space-y-6"
        @submit.prevent="submitGame(nickname, gameCode)"
      >
        <div>
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
        </div>
        <p id="error-box" class="text-red-500 ml-1 mt-1" hidden>
          Something went wrong
        </p>
        <div>
          <button
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 dark:bg-blue-600 hover:bg-blue-700 dark:hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Join
          </button>
        </div>
      </form>
      <div class="w-full text-center font-mono uppercase  dark:text-gray-200 dark:hover:text-gray-300" style="margin-top: 15px">
        <a href="/commands">Read the list of commands</a>
      </div>
    </main>
  </div>
</template>

<script setup>
import LogoV1 from "@/components/logos/LogoV1.vue";
import LogoV2 from "@/components/logos/LogoV2.vue";
import axios from "axios";
import router from "@/router";
import { inject } from "vue";

const $cookies = inject("$cookies");

let nickname = undefined;
let gameCode = undefined;

function updateGameCode(element) {
  const event = new Event("input");
  element.value = generateGameCode();
  element.dispatchEvent(event);
}

function generateGameCode() {
  return Math.floor(Math.random() * 90000) + 10000;
  // TODO: Ensure that the game code never collides with already existing games
}

function submitGame(nickname, gameCode) {
  axios
    .post("http://localhost:8000/game/createorjoin/", {
      nickname: cleanupNickname(nickname),
      game_code: gameCode,
    })
    .then((response) => {
      switch (response.status) {
        case 200:
          startGame(gameCode, cleanupNickname(nickname));
          break;
        default:
          showError("Unrecognized response!");
      }
    })
    .catch((response) => {
      if (response.response.status === 409) {
        showError(
          "A player has already joined with that name. Please choose a different one."
        );
      } else if (response.response.status === 400) {
        showError("Can't join. The game has already started!");
      } else {
        showError("Something went wrong!");
      }
    });
}

function startGame(gameCode, nickname) {
  $cookies.set("nickname", cleanupNickname(nickname));
  router.push({
    name: "game",
    params: { gameCode: gameCode },
  });
}

function showError(text) {
  const error_box = document.getElementById("error-box");
  error_box.innerText = text;
  error_box.removeAttribute("hidden");
}

function cleanupNickname(nickname) {
  return nickname.trim().replace(" ", "_");
}
</script>
