<template>
  <div class="dark:text-gray-200">
    <p
      class="inline mr-3 uppercase font-mono font-semibold"
      :class="{ 'text-blue-600': username === nickname }"
    >
      {{ username }}
    </p>
    <p class="inline">{{ message }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  username: {
    type: String,
    required: true,
  },
  message: {
    type: String,
    required: true,
  },
  date: {
    type: String,
    required: true,
  },
  nickname: {
    type: String,
    required: true,
  },
});
</script>
