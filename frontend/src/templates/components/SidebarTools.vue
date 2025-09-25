<script setup lang="ts">
import { ref, watch, computed } from 'vue'
// @ts-ignore
import toolData from '../data/tool.json'
import Dropdown from './Dropdown.vue'
import ProductDropdown from './ProductDropdown.vue'
import { useRouter } from 'vue-router';

const router = useRouter()
interface ToolSection {
  [key: string]: {
    [key: string]: string
  }
}

interface SelectedProduct {
  key: string
  label: string
  selected: boolean
}

const props = defineProps<{
  existingItems?: { content: string, type?: string }[]
  selectedProducts: SelectedProduct[]
}>()

const emit = defineEmits<{
  (e: 'changeTableData', tableData: string): void
  (e: 'update:selectedProducts', products: SelectedProduct[]): void
}>()

const toolSections = toolData as ToolSection
const openDropdowns = ref<string[]>([])

// selectedProducts ref'ini kaldırıyoruz çünkü artık prop olarak alıyoruz
// Bunun yerine computed kullanacağız
const localSelectedProducts = computed({
  get: () => props.selectedProducts,
  set: (value) => {
    emit('update:selectedProducts', value)
  }
})

// Kullanılan değerleri kontrol eden yardımcı fonksiyon
const isValueUsed = (value: string) => {
  if (!props.existingItems) return false
  return props.existingItems.some(item =>
    item.content === `${value}: ` || item.content === value
  )
}

const handleToggleDropdown = (title: string) => {
  if (openDropdowns.value.includes(title)) {
    openDropdowns.value = openDropdowns.value.filter(item => item !== title)
  } else {
    openDropdowns.value.push(title)
  }
}

const handleSelectedProductsChange = (products: SelectedProduct[]) => {
  localSelectedProducts.value = products
}

const handleDragStart = (event: DragEvent, text: string, key: string) => {
  if (event.dataTransfer) {
    const dragData = {
      text,
      key
    }
    event.dataTransfer.setData('text/plain', JSON.stringify(dragData))
    event.dataTransfer.effectAllowed = 'copy'
  }
}

const generateTableHTML = () => {
  // Sadece seçili olan özellikleri filtrele
  const selectedColumns = localSelectedProducts.value.filter(product => product.selected)

  const rows = Array.from({ length: 5 })
  // Tablo HTML'ini oluştur
  const tableHTML = `
    <table style="min-width: 100%; border-collapse: collapse; border: 1px solid #d1d5db;">
    <thead>
      <tr>
        ${selectedColumns.map(col => {
    return `<th style="border: 1px solid #d1d5db; padding: 4px 8px; color: #374151; font-size: 12px">${col.label}</th>`
  }).join('')}
      </tr>
    </thead>
      <tbody>
        ${rows.map(() => `
          <tr style="font-size: 12px;">
            ${selectedColumns.map(col => {
    if (col.key === 'name') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; color: #374151;">Ürün Adı</td>`
    }
    else if (col.key === 'description') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; color: #374151;">Ürünün açıklaması</td>`
    }
    else if (col.key === 'code') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; color: #374151;">Ürün Kodu</td>`
    }
    else if (col.key === 'unit') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; color: #374151;">Ürün Birimi</td>`
    }
    else if (col.key === 'quantity') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; text-align: center;">1</td>`
    }
    else if (col.key === 'communicationTax') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; text-align: center;">%20</td>`
    }
    else if (col.key === 'exciseDuty') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; text-align: center;">%20</td>`
    }
    else if (col.key === 'accommodationTax') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; text-align: center;">%20</td>`
    }
    else if (col.key === 'withholdingTax') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; text-align: center;">%20</td>`
    }
    else if (col.key === 'discount') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; text-align: center;">%20</td>`
    }
    else if (col.key === 'price') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; text-align: right;">1.000,00</td>`
    } else if (col.key === 'vat') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; text-align: center;">%20</td>`
    }
    else if (col.key === 'total') {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px; text-align: right;">1.000,00</td>`
    }
    else {
      return `<td style="border: 1px solid #d1d5db; padding: 4px 8px;">1.000,00</td>`
    }
  }).join('')}
          </tr>
        `).join('')}
      </tbody>
    </table>
  `

  return tableHTML.trim()
}

const handleProductTableDragStart = (event: DragEvent) => {
  if (event.dataTransfer) {
    // Seçili kolonlardan tablo HTML'i oluştur
    const tableHTML = generateTableHTML()
    event.dataTransfer.setData('text/plain', tableHTML)
    event.dataTransfer.effectAllowed = 'copy'
  }
}

const translateTitle = (title: string): string => {
  const titleMap: { [key: string]: string } = {
    customer: 'Müşteri Bilgileri',
    invoice: 'Fatura Bilgileri',
    totalAmount: 'Toplam Tutar Bilgileri',
    specialNotes: 'Özel Notlar'
  }
  return titleMap[title] || title
}

watch(localSelectedProducts, () => {
  const tableHTML = generateTableHTML()
  emit('changeTableData', tableHTML)
})

const isTableUsed = computed(() => {
  if (!props.existingItems) return false
  return props.existingItems.some(item => item?.type === 'table')
})

const handleGoHome = () => {
  router.push('/templates')
}
</script>

<template>
  <div class="h-screen overflow-y-auto p-4 flex flex-col gap-4 bg-white">
    <div class="flex flex-col gap-2">
      <button class="text-base text-gray-700 flex items-center justify-center gap-2 border border-gray-300 rounded-md py-3"
      @click="handleGoHome">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
        <polyline points="9 22 9 12 15 12 15 22"/>
      </svg>
      Şablonlar Sayfası
    </button>
    <Divider />
    <h1 class="text-xl font-bold text-gray-800">Araçlar</h1>
    </div>

    <div class="flex flex-col gap-2">
      <template v-for="(section, title) in toolSections" :key="title">
        <Dropdown v-if="title !== 'product'" :title="String(title)" :translated-title="translateTitle(String(title))"
          :is-open="openDropdowns.includes(String(title))"
          :is-last-item="title === Object.keys(toolSections).length - 1" @toggle="handleToggleDropdown">
          <div v-for="(value, key) in section" :key="key"
            class="py-2 px-6 bg-white text-sm cursor-move hover:bg-gray-50 group" :class="{
              'border-b border-gray-200': key !== Object.keys(section).length - 1,
              'text-gray-600': !isValueUsed(value),
              'text-gray-400 cursor-not-allowed': isValueUsed(value)
            }" draggable="true" @dragstart="(e) => !isValueUsed(value) && handleDragStart(e, `${value}: `, String(key))"
            tabindex="0" :aria-label="`Drag: ${value}`" :aria-disabled="isValueUsed(value)">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"
                  fill="currentColor">
                  <path
                    d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" />
                </svg>
                {{ value }}
              </div>
              <div class="flex items-center gap-2">
                <span v-if="isValueUsed(value)" class="text-xs text-gray-400">(Kullanıldı)</span>
                <svg class="w-5 h-5 text-gray-400 opacity-0 group-hover:opacity-100" xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M3 7a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 11a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                    clip-rule="evenodd" />
                </svg>
              </div>
            </div>
          </div>
        </Dropdown>
      </template>
    </div>
    <!-- Ürün Dropdown'ı -->
    <ProductDropdown v-model:selectedProducts="localSelectedProducts" :initial-selected-products="localSelectedProducts"
      @update:selectedProducts="handleSelectedProductsChange" />

    <button
      class="w-full px-4 py-3 text-left bg-white border border-gray-300 rounded-md hover:bg-gray-50 flex items-center justify-between group cursor-move disabled:opacity-50 disabled:cursor-not-allowed"
      draggable="true" @dragstart="handleProductTableDragStart" tabindex="0" aria-label="Ürünler Tablosu"
      :disabled="isTableUsed">
      <span class="font-medium" :class="isTableUsed ? 'text-gray-400' : 'text-gray-600'">Ürünler Tablosu</span>
      <svg class="w-5 h-5 opacity-0 group-hover:opacity-100" :class="isTableUsed ? 'text-gray-300' : 'text-gray-400'"
        xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd"
          d="M3 7a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 11a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
          clip-rule="evenodd" />
      </svg>
    </button>

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