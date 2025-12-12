<template>
	<button
		:class="computedClass"
		:disabled="disabled"
		@click="onClick"
		v-bind="attrs"
	>
		<slot />
	</button>
</template>

<script setup lang="ts">
import { computed, useAttrs } from 'vue'

const props = defineProps({
	variant: { type: String, default: 'primary' }, // primary | secondary | ghost | outline | danger
	size: { type: String, default: 'md' }, // sm | md | lg
	disabled: { type: Boolean, default: false },
	rounded: { type: Boolean, default: true },
	btnClass: { type: String, default: '' },
})

const emit = defineEmits(['click'])
const attrs = useAttrs()

const base = 'inline-flex items-center justify-center font-medium transition-colors duration-150'

const variants: Record<string, string> = {
	primary: 'bg-blue-100 text-blue-800 hover:bg-blue-200',
	secondary: 'bg-gray-100 text-gray-800 hover:bg-gray-200',
	ghost: 'bg-transparent text-gray-800 hover:bg-gray-100',
	outline: 'bg-white text-gray-800 border border-gray-300 hover:bg-gray-50',
    danger: 'bg-red-100 text-red-800 hover:bg-red-200',
}

const sizes: Record<string, string> = {
	sm: 'px-2 py-1 text-sm',
	md: 'px-3 py-2 text-sm',
	lg: 'px-4 py-2 text-base',
}

const computedClass = computed(() => {
	const v = variants[props.variant] || variants.primary
	const s = sizes[props.size] || sizes.md
	const r = props.rounded ? 'rounded-md' : ''
	const disabled = props.disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'
	return [base, v, s, r, disabled, props.btnClass].filter(Boolean).join(' ')
})

function onClick(e: MouseEvent) {
	if (props.disabled) return
	emit('click', e)
}
</script>

<style scoped>
/* Styling via Tailwind classes */
</style>
