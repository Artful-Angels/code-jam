<template>
  <div>
    <div class="bg-white border-b">
      <h2>Messages</h2>
    </div>
    <div>
      <Message v-for="message in messages" v-bind="message" :nickname="nickname" />
    </div>
    <div>
      <button @click="$emit('sendMessage', 'Test message')">Send message</button>
    </div>
  </div>
</template>

<script setup>
import Message from "@/components/Messaging/Message.vue";

defineEmits(["sendMessage"])

const props = defineProps({
  messages: {
    type: Array,
    required: true,
  },
  nickname: {
    type: String,
    required: true,
  },
})
</script>
