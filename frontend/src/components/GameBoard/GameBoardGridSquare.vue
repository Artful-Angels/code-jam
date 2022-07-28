<template>
  <button
    class="flex items-center place-content-center p-1 rounded-md aspect-square"
    :class="{ 'bg-gray-100': !(isOpen || isOpenLocal) }"
    @click="openSquare"
    @contextmenu.prevent="$emit('toggleFlag', coordinates)"
  >
    <Flag v-if="isFlagged && !(isOpen || isOpenLocal)" />
    <Mine v-else-if="(isOpen || isOpenLocal) && isMine" />
    <span v-else-if="(isOpen || isOpenLocal)">{{adjacentMines ? adjacentMines : '' }}</span>
  </button>
</template>

<script setup>
import Flag from "@/components/icons/Flag.vue";
import Mine from "@/components/icons/Mine.vue";
import { ref } from "vue";

const emit = defineEmits(["openSquare", "toggleFlag"])

const props = defineProps({
  coordinates: {
    type: String,
    required: true,
  },
  isOpen: {
    type: Boolean,
    required: false,
    default: false,
  },
  isMine: {
    type: Boolean,
    required: false,
    default: false,
  },
  isFlagged: {
    type: Boolean,
    required: false,
    default: false,
  },
  adjacentMines: {
    type: Number,
    required: false,
    default: 0,
  },
});

let isOpenLocal = ref(false)

function openSquare() {
  if (!props.isFlagged) {
    console.log("Opening square")

    emit('openSquare', props.coordinates)
    isOpenLocal.value = true
  }
}
</script>
