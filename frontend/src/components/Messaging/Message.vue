<template>
  <div>
    <p>{{ username }}</p>
    <p>{{ message }}</p>
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
})
</script>
