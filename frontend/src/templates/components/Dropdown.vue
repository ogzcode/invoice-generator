<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

interface Props {
  title: string
  isOpen: boolean
  translatedTitle: string
  isLastItem?: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'toggle': [title: string]
}>()

const handleToggle = () => {
  emit('toggle', props.title)
}
</script>

<template>
  <div class="border border-gray-300 rounded-md overflow-hidden mb-2">
    <button 
      class="w-full px-4 py-3 text-left bg-white hover:bg-gray-50 flex items-center justify-between transition-colors"
      @click="handleToggle"
      :aria-expanded="isOpen"
      :aria-controls="`dropdown-${title}`"
    >
      <span class="font-medium text-gray-600">{{ translatedTitle }}</span>
      <svg
        class="w-5 h-5 text-gray-400 transform transition-transform"
        :class="{ 'rotate-180': isOpen }"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fill-rule="evenodd"
          d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
          clip-rule="evenodd"
        />
      </svg>
    </button>

    <div 
      v-show="isOpen" 
      :id="`dropdown-${title}`" 
      class="bg-white border-t border-gray-200"
    >
      <slot></slot>
    </div>
  </div>
</template> 