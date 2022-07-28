<template>
  <div>
    <main></main>
    <section>
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

const $cookies = inject("$cookies");
const nickname = $cookies.get("nickname");

const props = defineProps({
  gameCode: {
    type: Number,
    required: true,
  },
});

let messages = reactive([]);

const gameSocket = new WebSocket(
  `ws://localhost:8000/ws/game/${props.gameCode}/`
);
gameSocket.addEventListener("message", function (event) {
  let data = JSON.parse(event.data.toString());
  console.log("Message from gameSocket: ", data);
});

const chatSocket = new WebSocket(
  `ws://localhost:8000/ws/chat/${props.gameCode}/${nickname}/`
);
chatSocket.addEventListener("message", function (event) {
  const data = JSON.parse(event.data.toString());
  console.log("Message from chatSocket: ", data);
  messages.push(data);
  console.log(messages);
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
</script>
