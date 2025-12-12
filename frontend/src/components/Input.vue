<template>
	<input
		:type="type"
		:value="modelValue"
		@input="onInput"
		:placeholder="placeholder"
		:disabled="disabled"
		:class="computedClass"
		:aria-label="ariaLabel"
	/>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
	modelValue: { type: [String, Number], default: '' },
	type: { type: String, default: 'text' },
	placeholder: { type: String, default: '' },
	disabled: { type: Boolean, default: false },
	inputClass: { type: String, default: '' },
	ariaLabel: { type: String, default: 'input' },
})

const emit = defineEmits(['update:modelValue', 'input'])

function onInput(event: Event) {
	const target = event.target as HTMLInputElement | null
	const value = target ? target.value : ''
	emit('update:modelValue', value)
	emit('input', value)
}

const computedClass = computed(() => {
	const base = 'w-full p-1 text-sm border border-gray-300 rounded-sm focus:outline-none focus:ring-1 focus:ring-blue-500'
	const disabled = props.disabled ? ' opacity-60 cursor-not-allowed' : ''
	return `${base}${disabled} ${props.inputClass}`.trim()
})
</script>

<style scoped>
/* Intentionally empty: styling uses Tailwind classes */
</style>
