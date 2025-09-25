import { ref } from 'vue'
import type { DraggableItem } from '../types/editor.ts'

export const useResizable = () => {
  const isResizing = ref(false)
  const currentResizeItem = ref<DraggableItem | null>(null)
  const resizeDirection = ref<'e' | 's' | 'se' | null>(null)
  const startSize = ref({ width: 0, height: 0 })
  const startPosition = ref({ x: 0, y: 0 })

  const handleResizeStart = (
    event: MouseEvent,
    item: DraggableItem,
    direction: 'e' | 's' | 'se'
  ) => {
    isResizing.value = true
    currentResizeItem.value = item
    resizeDirection.value = direction
    startPosition.value = { x: event.clientX, y: event.clientY }
    startSize.value = { ...item.size }
  }

  const handleResizeMove = (event: MouseEvent) => {
    if (!isResizing.value || !currentResizeItem.value) return

    const deltaX = event.clientX - startPosition.value.x
    const deltaY = event.clientY - startPosition.value.y

    // Sadece mevcut öğenin boyutunu güncelle
    const newSize = { ...startSize.value }

    if (resizeDirection.value === 'e' || resizeDirection.value === 'se') {
      newSize.width = Math.max(50, startSize.value.width + deltaX)
    }
    if (resizeDirection.value === 's' || resizeDirection.value === 'se') {
      newSize.height = Math.max(50, startSize.value.height + deltaY)
    }

    currentResizeItem.value.size = newSize
  }

  const handleResizeEnd = () => {
    isResizing.value = false
    currentResizeItem.value = null
    resizeDirection.value = null
  }

  return {
    isResizing,
    currentResizeItem,
    handleResizeStart,
    handleResizeMove,
    handleResizeEnd
  }
} 