<script setup lang="ts">
import { computed } from 'vue'
// @ts-ignore
import toolData from '../data/tool.json'
import AddKeyInput from './AddKeyInput.vue'
import { useKeyStore } from '../../store/useKeyStore'
import type { KeyItem as KeyItemType } from '../types/editor'
import KeyItem from '../../components/KeyItem.vue'

const keyStore = useKeyStore()
const keyList = computed(() => keyStore.keyList)

const handleDragStart = (event: DragEvent | any, key: KeyItemType) => {
	if (event?.dataTransfer) {
		event.dataTransfer.setData('text/plain', JSON.stringify(key))
		event.dataTransfer.effectAllowed = 'copy'
	}
}
</script>

<template>
	<div class="h-screen overflow-y-auto px-4 flex flex-col gap-4 bg-white">
		<h1 class="text-lg font-bold text-stone-700 border-b border-stone-300 pb-1">Araçlar</h1>
		<AddKeyInput />

		<KeyItem
			v-for="(value, key) in keyList"
			:key="key"
			:item="value"
			@dragstart="handleDragStart($event, value)"
		/>
	</div>
</template>

<style scoped>
[draggable="true"] {
	user-select: none;
	-webkit-user-drag: element;
}

[draggable="true"]:focus {
	outline: 1px solid #22c55e;
}

/* Özel scrollbar stilleri */
::-webkit-scrollbar {
	width: 8px;
}

::-webkit-scrollbar-track {
	background: #f1f1f1;
	border-radius: 4px;
}

::-webkit-scrollbar-thumb {
	background: #888;
	border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
	background: #666;
}

.cursor-not-allowed {
	cursor: not-allowed !important;
}

[draggable="true"][aria-disabled="true"] {
	pointer-events: none;
	opacity: 0.7;
}
</style>