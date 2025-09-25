<script setup lang="ts">
import { ref, defineEmits, onMounted, onUnmounted, watch, computed } from 'vue'
import { useSortable } from '@vueuse/integrations/useSortable'
import productData from '../data/tool.json'

interface ProductItem {
  key: string
  label: string
  selected: boolean
}

interface SelectedProduct {
  key: string
  label: string
  selected: boolean
}

const props = defineProps<{
  selectedProducts: SelectedProduct[]
  initialSelectedProducts: SelectedProduct[]
}>()

const emit = defineEmits<{
  (e: 'update:selectedProducts', products: SelectedProduct[]): void
}>()

const localSelectedProducts = computed({
  get: () => props.selectedProducts,
  set: (value) => {
    emit('update:selectedProducts', value)
  }
})

const handleToggleProduct = (product: SelectedProduct) => {
  const updatedProducts = localSelectedProducts.value.map(p => {
    if (p.key === product.key) {
      return { ...p, selected: !p.selected }
    }
    return p
  })
  localSelectedProducts.value = updatedProducts
}

// Product verilerini uygun formata dönüştürme
const products = ref<ProductItem[]>(
  Object.entries(productData.product).map(([key, label]) => ({
    key,
    label: label as string,
    selected: props.initialSelectedProducts.find(product => product.key === key) ? true : false
  }))
)

// Sadece selectedProducts değişikliklerini izle ve products'ı güncelle
watch(() => props.selectedProducts, (newProducts) => {
  // Eğer products değeri henüz oluşturulmamışsa işlem yapma
  if (!products.value.length) return

  products.value = products.value.map(product => ({
    ...product,
    selected: newProducts.some(p => p.key === product.key && p.selected)
  }))
}, { deep: true })

const isOpen = ref(false)
const containerRef = ref<HTMLElement | null>(null)

// Sortable entegrasyonu
const sortable = useSortable(containerRef, products, {
  animation: 150,
  ghostClass: 'bg-gray-100',
  onEnd: () => {
    handleCheckboxChange()
  }
})

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const handleCheckboxChange = () => {
  const selectedProducts = products.value
    .filter(item => item.selected)
    .map(item => ({ key: item.key, label: item.label, selected: item.selected }))
  
  // Eğer seçili ürünler mevcut seçili ürünlerden farklıysa güncelle
  if (JSON.stringify(selectedProducts) !== JSON.stringify(props.selectedProducts)) {
    emit('update:selectedProducts', selectedProducts)
  }
}

// Dışarı tıklandığında dropdown'ı kapatma
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.product-dropdown')) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <div class="product-dropdown relative">
    <button
      @click="toggleDropdown"
      class="w-full px-4 py-3 text-left bg-white border border-gray-300 rounded-md hover:bg-gray-50"
      :class="{ 'rounded-b-none': isOpen }"
    >
      <div class="flex items-center justify-between">
        <span class="font-medium text-gray-600">Ürün Alanları</span>
        <svg
          class="w-5 h-5 transition-transform text-gray-400"
          :class="{ 'rotate-180': isOpen }"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
    </button>

    <div
      v-show="isOpen"
      ref="containerRef"
      class="absolute z-10 w-full bg-white border border-gray-300 border-t-0 rounded-b-md shadow-lg"
    >
      <div
        v-for="item in products"
        :key="item.key"
        class="flex items-center px-4 py-2 hover:bg-gray-50 cursor-move group"
        :class="{ 'bg-blue-50': item.selected }"
      >
        <div class="flex items-center flex-1 gap-2">
          <input
            type="checkbox"
            :id="item.key"
            v-model="item.selected"
            @change="handleCheckboxChange"
            class="w-4 h-4 text-blue-500 border-gray-300 rounded focus:ring-blue-500"
          >
          <label :for="item.key" class="text-sm text-gray-600">{{ item.label }}</label>
        </div>
        <svg
          class="w-5 h-5 text-gray-400 opacity-0 group-hover:opacity-100"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M3 7a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 11a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
    </div>
  </div>
</template>

<style>
/* Ürün dropdown özel stilleri */
.product-dropdown {
  user-select: none;
  --dropdown-bg: white;
  --dropdown-border: #e5e7eb;
  --dropdown-text: #4b5563;
  --dropdown-hover: #f9fafb;
  --dropdown-selected: #ebf5ff;
  
  /* Dark mode geçersiz kılma */
  &, :deep(*) {
    color-scheme: light !important;
  }

  /* Dropdown button */
  button {
    background-color: var(--dropdown-bg) !important;
    border-color: var(--dropdown-border) !important;
    color: var(--dropdown-text) !important;

    &:hover {
      background-color: var(--dropdown-hover) !important;
    }

    svg {
      color: #9ca3af !important;
    }
  }

  /* Dropdown içerik */
  .dropdown-content {
    background-color: var(--dropdown-bg) !important;
    border-color: var(--dropdown-border) !important;
  }

  /* Checkbox container */
  .checkbox-container {
    &:hover {
      background-color: var(--dropdown-hover) !important;
    }

    &.selected {
      background-color: var(--dropdown-selected) !important;
    }
  }

  /* Checkbox input */
  input[type="checkbox"] {
    appearance: none !important;
    -webkit-appearance: none !important;
    width: 1rem !important;
    height: 1rem !important;
    border: 1px solid var(--dropdown-border) !important;
    border-radius: 0.25rem !important;
    background-color: var(--dropdown-bg) !important;
    cursor: pointer !important;
    
    &:checked {
      background-color: #2563eb !important;
      border-color: #2563eb !important;
      background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='M12.207 4.793a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0l-2-2a1 1 0 011.414-1.414L6.5 9.086l4.293-4.293a1 1 0 011.414 0z'/%3e%3c/svg%3e") !important;
    }

    &:focus {
      outline: none !important;
      box-shadow: 0 0 0 2px #93c5fd !important;
    }
  }

  /* Label */
  label {
    color: var(--dropdown-text) !important;
    cursor: pointer !important;
  }

  /* Sıralama ikonu */
  .sort-icon {
    color: #9ca3af !important;
  }
}

/* Dark mode override */
:deep(.app-dark) .product-dropdown {
  --dropdown-bg: white;
  --dropdown-border: #e5e7eb;
  --dropdown-text: #4b5563;
  --dropdown-hover: #f9fafb;
  --dropdown-selected: #ebf5ff;
}
</style> 