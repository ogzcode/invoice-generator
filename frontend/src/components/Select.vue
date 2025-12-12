
<template>
  <div>
    <select
      :value="modelValue === null ? '' : String(modelValue)"
      @change="onChange"
      :disabled="disabled"
      class="w-full border border-gray-200 rounded-md p-1 text-sm bg-white text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-500"
    >
      <option v-if="placeholder" value="" disabled hidden>{{ placeholder }}</option>
      <option v-for="opt in options" :key="String(opt.value)" :value="String(opt.value)">{{ opt.label }}</option>
    </select>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from 'vue'

type Option = { label: string; value: string | number }

const props = defineProps({
  modelValue: { type: [String, Number] as PropType<string | number | null>, default: null },
  options: { type: Array as PropType<Option[]>, default: () => [] },
  placeholder: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number | null): void
}>()

// Keep props as a single reactive object so template and watchers stay reactive

function onChange(e: Event) {
  const raw = (e.target as HTMLSelectElement).value
  const match = props.options.find((o) => String(o.value) === raw)
  const value = match ? match.value : (raw === '' ? null : raw)
  emit('update:modelValue', value)
}
</script>

<style scoped>
/* Native select styling done with Tailwind classes in template */
</style>
