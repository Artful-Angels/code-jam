<template>
  <div class="grid grid-cols-7 h-full">
    <main class="col-span-5 bg-white p-10">
      <GameBoard :gameState="gameState" @openSquare="(coordinates) => { openSquare(coordinates) }" />
    </main>
    <section class="col-span-2 border-l-2 h-full">
      <MessageView
        :messages="messages"
        :nickname="nickname"
        @send-message="(message) => sendMessage(message)"
      />
    </section>
  </div>
</template>

<script setup>
import { inject, reactive } from "vue";
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
let gameState = reactive({value: {}});

const gameSocket = new WebSocket(
  `ws://localhost:8000/ws/game/${props.gameCode}/`
);
gameSocket.addEventListener("message", function (event) {
  let data = JSON.parse(event.data.toString());
  console.log("Message from gameSocket: ", data);
  switch (data.method) {
    case "update_members":
      gameState.value.players = data.data
      break
    case "start_game":
      gameState.value = data.data
  }
});

const chatSocket = new WebSocket(
  `ws://localhost:8000/ws/chat/${props.gameCode}/${nickname}/`
);
chatSocket.addEventListener("message", function (event) {
  const data = JSON.parse(event.data.toString());
  console.log("Message from chatSocket: ", data);
  messages.push(data);
});

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
  console.log("Opening square", coordinates)
}
</script>
