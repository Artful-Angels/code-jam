<template>
  <div>
    <div class="bg-white border-b pb-2 pt-5 mb-3">
      <h3 class="mt-0">Messages</h3>
    </div>
    <div class="mx-3">
      <div>
        <Message
          v-for="message in messages"
          v-bind="message"
          :nickname="nickname"
        />
      </div>
      <div class="mt-4">
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
