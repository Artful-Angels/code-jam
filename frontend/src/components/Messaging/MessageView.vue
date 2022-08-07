<template>
  <div>
    <div
      class="bg-white dark:bg-slate-800 border-b dark:border-slate-700 pb-2 pt-5 mb-3"
    >
      <h3 class="mt-0">Messages</h3>
    </div>
    <div class="px-3 overflow-y-auto pb-4" style="height: calc(100vh - 145px)">
      <div id="messageList" class="w-full">
        <div
          v-if="!gameStarted"
          class="w-full p-3 mb-2 dark:bg-slate-800 rounded-md border border-slate-300 dark:border-gray-700 text-gray-900 dark:text-slate-100 sm:text-sm"
        >
          <p class="mb-2">
            The game hasn't started yet, so new players can still join. Send
            them this link:
          </p>
          <button
            class="w-full py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 dark:hover:bg-blue-500"
            href="#"
            @click="copyToClipboard(joinUrl)"
          >
            COPY LINK
          </button>
        </div>
        <Message
          v-for="message in messages"
          v-bind="message"
          :nickname="nickname"
        />
      </div>
      <div class="mt-4 fixed bottom-6" style="width: calc(28.57142857% - 26px)">
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
import { onMounted, ref } from "vue";

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
  gameCode: {
    type: Number,
    required: true,
  },
  gameStarted: {
    type: Boolean,
    required: true,
  },
});

let userMessage = ref("");
let messageListElement = ref(undefined);

const joinUrl = `${window.location.host}/?game=${props.gameCode}`;

function scrollToLastMessage() {
  if (messageListElement.value !== undefined) {
    messageListElement.value.lastElementChild.scrollIntoView({
      behavior: "smooth",
    });
  }
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text.toString());
}

onMounted(() => {
  messageListElement.value = document.getElementById("messageList");
  messageListElement.value.addEventListener("DOMNodeInserted", () => {
    scrollToLastMessage();
  });
});
</script>
