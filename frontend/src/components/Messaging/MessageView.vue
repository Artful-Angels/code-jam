<template>
  <div>
    <div class="bg-white border-b">
      <h2>Messages</h2>
    </div>
    <div>
      <Message
        v-for="message in messages"
        v-bind="message"
        :nickname="nickname"
      />
    </div>
    <div>
      <input
        type="text"
        ref="messageField"
        v-model="userMessage"
        @keydown.enter="
          $emit('sendMessage', userMessage);
          userMessage = '';
        "
        placeholder="Message"
      />
    </div>
  </div>
</template>

<script setup>
import Message from "@/components/Messaging/Message.vue";
import { ref } from "vue";

defineEmits(["sendMessage"]);

const props = defineProps({
  messages: {
    type: Array,
    required: true,
  },
  nickname: {
    type: String,
    required: true,
  },
});

let userMessage = ref("");
</script>
