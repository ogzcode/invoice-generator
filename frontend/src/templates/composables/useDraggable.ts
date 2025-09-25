import { ref } from 'vue'
import type { DraggableItem } from '../types/editor.ts'

export const useDraggable = () => {
  const isDragging = ref(false)
  const currentDragItem = ref<DraggableItem | null>(null)
  const dragOffset = ref({ x: 0, y: 0 })

  const handleDragStart = (event: MouseEvent, item: DraggableItem) => {
    event.preventDefault()
    isDragging.value = true
    currentDragItem.value = item
    
    const element = event.currentTarget as HTMLElement
    const rect = element.getBoundingClientRect()
    
    dragOffset.value = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    }
  }

  const handleDragMove = (event: MouseEvent) => {
    if (!isDragging.value || !currentDragItem.value) return

    const a4Page = document.querySelector('.a4-page') as HTMLElement
    const rect = a4Page.getBoundingClientRect()
    
    const newX = event.clientX - rect.left - dragOffset.value.x
    const newY = event.clientY - rect.top - dragOffset.value.y
    
    currentDragItem.value.position = {
      x: Math.max(0, Math.min(newX, rect.width - 100)),
      y: Math.max(0, Math.min(newY, rect.height - 40))
    }
  }

  const handleDragEnd = () => {
    isDragging.value = false
    currentDragItem.value = null
  }

  return {
    isDragging,
    currentDragItem,
    dragOffset,
    handleDragStart,
    handleDragMove,
    handleDragEnd
  }
} 