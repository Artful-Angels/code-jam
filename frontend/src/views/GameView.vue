<template>
  <div class="grid grid-cols-7 h-full">
    <main class="col-span-5 bg-white dark:bg-slate-900 p-10">
      <GameBoard
        :gameCode="gameCode"
        :gameState="gameState"
        :gameStarted="gameStarted"
        :nickname="nickname"
        @openSquare="
          (coordinates) => {
            openSquare(coordinates);
          }
        "
        @playerDied="
          (player) => {
            // if not all players are dead, call systemMessage
            if (alivePlayers.length > 0 && player !== undefined) {
              systemMessage(`${player} has died`);
            }
          }
        "
      />
    </main>
    <section class="col-span-2 border-l-2 dark:border-slate-700 h-full">
      <MessageView
        :messages="messages"
        :nickname="nickname"
        @send-message="(message) => sendMessage(message)"
      />
    </section>
  </div>
</template>

<script setup>
import {computed, inject, reactive, ref} from "vue";
import MessageView from "@/components/Messaging/MessageView.vue";
import GameBoard from "@/components/GameBoard/GameBoard.vue";

const $cookies = inject("$cookies");
const nickname = $cookies.get("nickname");

const props = defineProps({
  gameCode: {
    type: Number,
    required: true,
  },
});

let messages = reactive([]);
let gameState = reactive({ value: {} });
let gameStarted = ref(false);

const gameSocket = new WebSocket(
  `ws://localhost:8000/ws/game/${props.gameCode}/`
);
gameSocket.addEventListener("message", function (event) {
  let data = JSON.parse(event.data.toString());
  console.log("Message from gameSocket: ", data);
  switch (data.method) {
    case "update_members":
      gameState.value.players = data.data;
      break;
    case "start_game":
      gameState.value = data.data;
      gameStarted.value = true;
      if (!tryFinish()) {
        // if (data.data.is_started === false) {
          // systemMessage("Game has started!");
        // }
      }
      break;
    case "update_game":
      gameState.value = data.data;
      tryFinish();
      break;
  }
});

const alivePlayers = computed(() => {
  if (gameState.value?.players === undefined) return []
  return Object.keys(gameState.value.players).filter(
    (playerName) => gameState.value.players[playerName].is_alive
  )
})

function tryFinish() {
  if (gameState.value?.is_finished === undefined) return
  if (gameState.value.is_finished) {
    systemMessage("Game has finished 🎉")
    console.log(alivePlayers.value);
    if (alivePlayers.value.length > 0) {
      systemMessage(`The following player${alivePlayers.value.length > 1 ? 's' : ''} survived:`)
      alivePlayers.value.forEach((playerName) => {
        systemMessage(`• ${playerName}`)
      })
    } else {
      systemMessage("No one survived. Better luck next time!")
    }
    return true
  }
}

const chatSocket = new WebSocket(
  `ws://localhost:8000/ws/chat/${props.gameCode}/${nickname}/`
);
chatSocket.addEventListener("message", function (event) {
  const data = JSON.parse(event.data.toString());
  console.log("Message from chatSocket: ", data);
  messages.push(data);
});

function systemMessage(message) {
  messages.push({
    message: message,
    username: "server",
    systemMessage: true,
  });
}

function sendMessage(message) {
  chatSocket.send(
    JSON.stringify({
      message: message,
      username: nickname,
      game_code: props.gameCode,
    })
  );
}

function openSquare(coordinates) {
  console.log("Opening square", coordinates);
  gameSocket.send(
    JSON.stringify({
      method: "update_game",
      data: {
        game_code: props.gameCode,
        player_name: nickname,
        click_at: coordinates,
      },
    })
  );
}
</script>
