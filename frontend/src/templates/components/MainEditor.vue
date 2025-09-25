<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useDraggable } from '../composables/useDraggable'
import { useResizable } from '../composables/useResizable'
import { DEFAULT_ITEM_SIZE } from '../constants/editor'
import type { DraggableItem } from '../types/editor.ts'

interface DragData {
    text: string
    key: string
}

const props = defineProps<{
    draggableItems: DraggableItem[]
}>()

const emit = defineEmits<{
    (e: 'update:draggableItems', items: DraggableItem[]): void
    (e: 'selectItem', id: string | null): void
}>()

const { isDragging, currentDragItem, dragOffset, handleDragStart, handleDragEnd } = useDraggable()
const { isResizing, currentResizeItem, handleResizeStart, handleResizeMove, handleResizeEnd } = useResizable()

// Grid boyutunu belirleyelim
const GRID_SIZE = 10 // 10px grid

// A4 sayfa boyutları (piksel cinsinden)
const A4_WIDTH = 210 * 3.78 // 210mm yaklaşık 794px
const A4_HEIGHT = 297 * 3.78 // 297mm yaklaşık 1123px

// Grid'e göre pozisyonu hesaplayan ve sayfa sınırlarını kontrol eden fonksiyon
const snapToGrid = (x: number, y: number, itemWidth = DEFAULT_ITEM_SIZE.width, itemHeight = DEFAULT_ITEM_SIZE.height) => {
    let snappedX = Math.round(x / GRID_SIZE) * GRID_SIZE
    let snappedY = Math.round(y / GRID_SIZE) * GRID_SIZE

    snappedX = Math.max(0, snappedX)
    snappedY = Math.max(0, snappedY)
    snappedX = Math.min(snappedX, A4_WIDTH - itemWidth)
    snappedY = Math.min(snappedY, A4_HEIGHT - itemHeight)

    return { x: snappedX, y: snappedY }
}

const handleDragOver = (event: DragEvent) => {
    event.preventDefault()
    event.dataTransfer!.dropEffect = 'copy'
}

const calculateContentHeight = (content: string, width: number): number => {
    const tempDiv = document.createElement('div')
    tempDiv.style.width = `${width}px`
    tempDiv.style.position = 'absolute'
    tempDiv.style.visibility = 'hidden'
    tempDiv.style.padding = content.includes('<table') ? '0' : '4px'
    tempDiv.style.boxSizing = 'border-box'
    tempDiv.innerHTML = content

    document.body.appendChild(tempDiv)
    const height = tempDiv.offsetHeight
    document.body.removeChild(tempDiv)

    return Math.max(height, 20)
}

const handleDrop = (event: DragEvent) => {
    event.preventDefault()
    const rawData = event.dataTransfer!.getData('text/plain')

    let content: string
    let key: string | undefined

    try {
        const dragData: DragData = JSON.parse(rawData)
        content = dragData.text
        key = dragData.key
    } catch {
        content = rawData
    }

    const a4Page = event.currentTarget as HTMLElement
    const rect = a4Page.getBoundingClientRect()

    const itemWidth = content.includes('<table') ? 600 : DEFAULT_ITEM_SIZE.width
    const itemHeight = calculateContentHeight(content, itemWidth)

    const snappedPosition = snapToGrid(
        event.clientX - rect.left,
        event.clientY - rect.top,
        itemWidth,
        itemHeight
    )

    const newItems = [...props.draggableItems]
    newItems.push({
        id: crypto.randomUUID(),
        content,
        key,
        type: content.includes('<table') ? 'table' : 'text',
        position: snappedPosition,
        size: { width: itemWidth, height: itemHeight },
        fontFamily: 'sans',
        fontSize: 14,
        textAlign: 'left',
        fontWeight: 'normal',
        fontStyle: 'normal',
        textDecoration: 'none',
        headers: content.includes('<table') ? ['name', 'quantity', 'unitPrice', 'vatRate'] : []
    })
    emit('update:draggableItems', newItems)
}

const handleDeleteItem = (itemId: string) => {
    emit('update:draggableItems', props.draggableItems.filter(item => item.id !== itemId))
    emit('selectItem', null)
}

const getItemStyles = (item: DraggableItem) => {
    const styles = {
        left: `${item.position.x}px`,
        top: `${item.position.y}px`,
        width: `${item.size.width}px`,
        height: `${item.size.height}px`,
        fontFamily: item.fontFamily === 'sans' ? 'ui-sans-serif, system-ui' :
            item.fontFamily === 'serif' ? 'ui-serif, Georgia' :
                'ui-monospace, monospace',
        fontSize: `${item.fontSize}px`,
        textAlign: item.textAlign as 'left' | 'center' | 'right',
        fontWeight: item.fontWeight,
        fontStyle: item.fontStyle,
        textDecoration: item.textDecoration,
        zIndex: (currentDragItem?.value?.id === item.id || currentResizeItem?.value?.id === item.id) ? 10 : 1,
        padding: '0.25rem',
        borderWidth: '1px',
        borderStyle: 'solid',
        borderColor: '#9ca3af',
        backgroundColor: '#ffffff'
    }

    if (item.content.includes('<table')) {
        styles.padding = '0'
    }

    return styles
}

const handleSelectItem = (event: MouseEvent, item: DraggableItem) => {
    event.stopPropagation()
    emit('selectItem', item.id)
}

const handlePageClick = () => {
    emit('selectItem', null)
}

const handleDragMove = (event: MouseEvent) => {
    if (!isDragging.value || !currentDragItem.value) return

    const a4Page = document.querySelector('.a4-page') as HTMLElement
    const rect = a4Page.getBoundingClientRect()

    const draggedItem = props.draggableItems.find(
        item => item.id === currentDragItem.value?.id
    )

    if (draggedItem) {
        const snappedPosition = snapToGrid(
            event.clientX - rect.left - dragOffset.value.x,
            event.clientY - rect.top - dragOffset.value.y,
            draggedItem.size.width,
            draggedItem.size.height
        )

        const updatedItems = props.draggableItems.map(item => {
            if (item.id === draggedItem.id) {
                return { ...item, position: snappedPosition }
            }
            return item
        })
        emit('update:draggableItems', updatedItems)
    }
}

onMounted(() => {
    window.addEventListener('mousemove', handleDragMove)
    window.addEventListener('mousemove', handleResizeMove)
    window.addEventListener('mouseup', handleDragEnd)
    window.addEventListener('mouseup', handleResizeEnd)
})

onUnmounted(() => {
    window.removeEventListener('mousemove', handleDragMove)
    window.removeEventListener('mousemove', handleResizeMove)
    window.removeEventListener('mouseup', handleDragEnd)
    window.removeEventListener('mouseup', handleResizeEnd)
})
</script>

<template>
    <div class="flex-1 overflow-y-auto flex justify-center pl-4 mt-4">
        <div class="w-[210mm] bg-white border border-gray-200 rounded-b-lg shadow-lg relative a4-page min-h-[297mm]"
            @dragover="handleDragOver" @drop="handleDrop" @click="handlePageClick">
            <div class="absolute inset-0 pointer-events-none">
                <div class="w-full h-full grid-bg"></div>
            </div>

            <div v-for="item in draggableItems" :key="item.id"
                class="absolute cursor-move bg-white hover:shadow-md group transition-shadow" :class="{
                    'ring-2 ring-green-500': (currentResizeItem?.id === item.id && isResizing) ||
                        (currentDragItem?.id === item.id && isDragging)
                }" :style="getItemStyles(item)" @click.stop="(e) => handleSelectItem(e, item)"
                @mousedown="(e) => handleDragStart(e, item)">
                <button
                    class="absolute -top-2 z-10 -right-2 w-6 h-6 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 flex items-center justify-center hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                    @mousedown.stop @click="handleDeleteItem(item.id)" aria-label="Öğeyi sil">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M18 6 6 18" />
                        <path d="m6 6 12 12" />
                    </svg>
                </button>

                <div class="absolute top-0 right-0 bottom-0 w-2 cursor-e-resize opacity-0 group-hover:opacity-100"
                    @mousedown.stop="(e) => handleResizeStart(e, item, 'e')" />
                <div class="absolute left-0 right-0 bottom-0 h-2 cursor-s-resize opacity-0 group-hover:opacity-100"
                    @mousedown.stop="(e) => handleResizeStart(e, item, 's')" />
                <div class="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize opacity-0 group-hover:opacity-100"
                    @mousedown.stop="(e) => handleResizeStart(e, item, 'se')" />

                <div class="w-full h-full overflow-hidden" :style="{
                    justifyContent: item.textAlign === 'left' ? 'flex-start' :
                        item.textAlign === 'right' ? 'flex-end' : 'center'
                }">
                    <template v-if="item.type === 'table'">
                        <div v-html="item.content"></div>
                    </template>
                    <template v-else>
                        {{ item.content }}
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.a4-page {
    touch-action: none;
    user-select: none;
}

/* Scroll özelleştirmeleri */
.overflow-y-auto {
    scrollbar-width: thin !important;
    scrollbar-color: #94a3b8 #f1f5f9 !important;

    &::-webkit-scrollbar {
        width: 8px !important;
    }

    &::-webkit-scrollbar-track {
        background: #f1f5f9 !important;
        border-radius: 4px !important;
    }

    &::-webkit-scrollbar-thumb {
        background-color: #94a3b8 !important;
        border-radius: 4px !important;
        border: 2px solid #f1f5f9 !important;
    }
}

.grid-bg {
    background-image:
        linear-gradient(to right, rgba(0, 0, 0, 0.05) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 0, 0, 0.05) 1px, transparent 1px);
    background-size: 10px 10px;
}

.grid-bg::after {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(to right, rgba(0, 0, 0, 0.1) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 0, 0, 0.1) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
}

[class*="cursor-"] {
    position: absolute;
    z-index: 1;
}

.cursor-e-resize {
    cursor: e-resize;
}

.cursor-s-resize {
    cursor: s-resize;
}

.cursor-se-resize {
    cursor: se-resize;
}

.draggable-table {
    border-collapse: collapse;
    width: 100%;
}

.draggable-table td {
    border: 1px solid #d1d5db;
    padding: 8px 16px;
}

.draggable-table tr:hover {
    background-color: #f9fafb;
}
</style>