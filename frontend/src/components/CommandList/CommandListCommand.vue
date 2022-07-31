<template>
  <div class="text-left mt-6">
    <h3 class="text-left uppercase text-xl font-mono font-semibold text-blue-600">{{ isHidden ? '---' : name }}</h3>
    <p class="dark:text-gray-200">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  name: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  isHidden: {
    type: Boolean,
    required: false,
    default: false,
  }
})
</script>
