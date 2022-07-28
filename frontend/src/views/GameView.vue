<template>
  <div>
    <ul>
    </ul>
  </div>
</template>

<script setup>
import { inject } from "vue";

const $cookies = inject('$cookies');
const nickname = $cookies.get("nickname")

const props = defineProps({
  gameCode: {
    type: Number,
    required: true,
  },
})

const gameSocket = new WebSocket(`ws://localhost:8000/ws/game/${props.gameCode}/`);
gameSocket.addEventListener('message', function (event) {
  let data = JSON.parse(event.data.toString())
  console.log('Message from gameSocket: ', data);
});

const chatSocket = new WebSocket(`ws://localhost:8000/ws/chat/${props.gameCode}/${nickname}/`);
chatSocket.addEventListener('message', function (event) {
  let data = JSON.parse(event.data.toString())
  console.log('Message from chatSocket: ', data);
});
</script>
