<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
// @ts-ignore
import SidebarTools from './components/SidebarTools.vue'
import EditingPanel from './components/EditingPanel.vue'
import MainEditor from './components/MainEditor.vue'
import type { DraggableItem } from './types/editor'
import { useKeyStore } from '../store/useKeyStore'

const isLoading = ref(true)
const draggableItems = ref<DraggableItem[]>([])
const selectedItemId = ref<string | null>(null)

const keyStore = useKeyStore()
const keyList = computed(() => keyStore.keyList)
//const { exportToJson } = useEditorIO(draggableItems)

// Ruler değerlerini statik olarak hesaplama
const GRID_SIZE = 10
const RULER_VALUES = Array.from(
  { length: Math.floor(794 / GRID_SIZE) + 1 },
  (_, i) => i * GRID_SIZE
)
const rulerValues = ref(RULER_VALUES)

const selectedItem = computed(() => {
  return draggableItems.value.find(item => item.id === selectedItemId.value)
})

onMounted(() => {
  // Simulate loading delay
  setTimeout(() => {
    isLoading.value = false
  }, 50)
})

watch(
  keyList,
  (v) => {
    const list = Array.isArray(v) ? v : Array.isArray((v as any)?.value) ? (v as any).value : []
    const values = new Set(list.map((k: any) => k.value))

    draggableItems.value = draggableItems.value.filter((item) => {
      if (!item.value) return true
      return values.has(item.value)
    })

    if (selectedItemId.value) {
      const selected = draggableItems.value.find(i => i.id === selectedItemId.value)
      if (!selected) {
        selectedItemId.value = null
      } else {
        if (!selected.value || !values.has(selected.value)) {
          selectedItemId.value = null
        }
      }
    }
  },
  { deep: true }
)
</script>

<template>
  <!-- Loading Overlay -->
  <Transition name="fade">
    <div v-if="isLoading"
      class="fixed inset-0 z-50 flex items-center justify-center bg-white bg-opacity-80 backdrop-blur-sm">
      <div class="text-center">
        <div
          class="inline-block w-16 h-16 border-4 border-t-primary border-primary border-opacity-20 rounded-full animate-spin">
        </div>
        <p class="mt-4 text-lg font-medium text-gray-700">Yükleniyor...</p>
      </div>
    </div>
  </Transition>

  <div class="template-editor min-h-screen bg-gray-100 grid grid-cols-12">
    <div class="sidebar-tools col-span-2">
      <SidebarTools />
    </div>

    <div class="col-span-8 flex flex-col max-h-screen pb-12">
      <div class="sticky top-0 z-10 flex justify-center">
        <div class="w-[210mm] h-8 bg-white border border-gray-200 rounded-t-lg relative overflow-hidden">
          <div v-for="value in rulerValues" :key="value" class="absolute bottom-0 border-l border-gray-300" :style="{
            left: `${value}px`,
            height: value % 50 === 0 ? '24px' : value % 25 === 0 ? '16px' : '8px'
          }">
            <span v-if="value % 50 === 0" class="absolute -left-2 top-0 text-[10px] text-gray-500">
              {{ value }}
            </span>
          </div>
        </div>
      </div>

      <MainEditor v-model:draggableItems="draggableItems" @selectItem="selectedItemId = $event" />
    </div>

    <div class="editing-panel col-span-2">
      <EditingPanel :selectedItem="selectedItem" :draggableItems="draggableItems" />
    </div>
  </div>
</template>

<style>
/* Kritik CSS'i inline olarak tanımlama */
:root {
  --editor-primary: #2563eb;
  --editor-secondary: #1e40af;
  --editor-bg: #f3f4f6;
  --editor-border: #e5e7eb;
  --editor-text: #1f2937;
}

/* Template Editor stilleri */
.template-editor {
  color-scheme: light;
  background-color: var(--editor-bg);
  color: var(--editor-text);
}

/* A4 sayfa stilleri */
.a4-page {
  touch-action: none;
  user-select: none;
  background-color: white !important;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

/* Grid arka planı */
.grid-bg {
  background-image:
    linear-gradient(to right, rgba(0, 0, 0, 0.05) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(0, 0, 0, 0.05) 1px, transparent 1px);
  background-size: 10px 10px;
  position: relative;
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

/* Kenar tutamaçları */
.resize-handle {
  position: absolute;
  z-index: 1;
  background-color: var(--editor-primary);
  border-radius: 2px;
}

/* Yön tutamaçları */
.cursor-e-resize {
  cursor: e-resize;
}

.cursor-s-resize {
  cursor: s-resize;
}

.cursor-se-resize {
  cursor: se-resize;
}

/* Cetvel */
.sticky {
  background-color: var(--editor-bg);
  border-bottom: 1px solid var(--editor-border);
}

/* Tablo stilleri */
.draggable-table {
  border-collapse: collapse;
  width: 100%;
}

.draggable-table td,
.draggable-table th {
  border: 1px solid var(--editor-border);
  padding: 8px 16px;
  background-color: white;
  color: var(--editor-text);
}

.draggable-table tr:hover {
  background-color: var(--editor-bg);
}

/* Renk seçici */
input[type="color"] {
  padding: 0;
}

input[type="color"]::-webkit-color-swatch-wrapper {
  padding: 0;
}

input[type="color"]::-webkit-color-swatch {
  border: none;
  border-radius: 4px;
}

/* Sidebar */
.sidebar-tools {
  background-color: white;
  border-right: 1px solid var(--editor-border);
}

.sidebar-tools .tool-item:hover {
  background-color: var(--editor-bg);
}

/* Editing panel */
.editing-panel {
  background-color: white;
  border-left: 1px solid var(--editor-border);
}

.editing-panel input,
.editing-panel select {
  border: 1px solid var(--editor-border);
  background-color: white;
  color: var(--editor-text);
}

.editing-panel input:focus,
.editing-panel select:focus {
  border-color: var(--editor-primary);
  outline-color: var(--editor-primary);
}

/* Loading animasyonu için transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Loading spinner özelleştirmeleri */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.border-t-primary {
  border-top-color: var(--editor-primary);
}

.border-primary {
  border-color: var(--editor-primary);
}
</style>