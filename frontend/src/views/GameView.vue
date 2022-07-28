<template>
  <div>
    <ul>
    </ul>
  </div>
</template>

<script setup>
const props = defineProps({
  gameCode: {
    type: Number,
    required: true,
  },
})

const gameSocket = new WebSocket(`ws://localhost:8000/ws/game/${props.gameCode}/`);
gameSocket.addEventListener('message', function (event) {
  let data = JSON.parse(event.data.toString())
  console.log('Message from server: ', data);
});
</script>
