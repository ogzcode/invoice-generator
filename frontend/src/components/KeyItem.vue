<template>
    <div class="flex gap-2">
        <div class=" flex-1 p-2 border border-stone-300 rounded-md bg-white text-sm cursor-move hover:shadow-sm transition-shadow duration-150"
            :draggable="draggable" @dragstart="onDragStart" tabindex="0" :aria-label="`Drag: ${item?.label}`">
            <div class="flex items-center gap-2 text-stone-700">
                <Key class="w-4 h-4 text-stone-500" />
                <p class="flex-1 flex justify-between items-center">
                    <span class="font-medium">{{ item.label }}</span>
                    <span class="text-xs text-pink-500 bg-pink-50 px-2 rounded-md">#{{ item.value }}</span>
                </p>
            </div>
        </div>
        <Button variant="danger" @click.stop="removeKey(item)" aria-label="Remove Key">
            <Trash class="w-4 h-4" />
        </Button>
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import { Key, Trash } from 'lucide-vue-next'
import { useKeyStore } from '../store/useKeyStore'
import Button from './Button.vue'

const { removeKey } = useKeyStore()

type KeyItem = {
    label: string
    value: string
}

const props = defineProps({
    item: { type: Object as () => KeyItem, required: true },
    draggable: { type: Boolean, default: true },
})

const emit = defineEmits<{
    (e: 'dragstart', event: DragEvent): void
}>()

function onDragStart(e: DragEvent) {
    // set dataTransfer for copy operations
    if (e.dataTransfer) {
        e.dataTransfer.setData('text/plain', JSON.stringify(props.item))
        e.dataTransfer.effectAllowed = 'copy'
    }
    emit('dragstart', e)
}
</script>

<style scoped>
/* visual styling via Tailwind classes in template */
</style>
