<script setup lang="ts">
import { ref } from 'vue';
import type { DraggableItem } from '../types/editor.ts'
import { useRouter } from 'vue-router'
import { exportToJson, exportToHtml, exportToPdf, printTemplate } from '../composables/useEditorIO'

const router = useRouter()
const props = defineProps<{
    selectedItem: DraggableItem | undefined
    draggableItems: DraggableItem[]
}>()

const templateName = ref('test')
const electronicType = ref("5");

const handleSaveTemplate = async () => {
    try {
        const exportData = {
            pageItems: props.draggableItems,
            exportDate: new Date().toISOString(),
            pageSize: 'A4'
        }

        const jsonString = JSON.stringify(exportData, null, 2)
        const htmlString = exportToHtml(templateName.value, exportData.pageItems)

        console.log('Şablon JSON:', jsonString)
        console.log('Şablon HTML:', htmlString)

    } catch (error) {
        console.error('Şablon kaydedilirken hata oluştu:', error)
    }
}
</script>

<template>
    <div class="p-4 bg-white">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">Düzenleme</h2>

        <!-- Dosya İşlemleri -->
        <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200 mb-4">
            <h3 class="text-base font-medium text-gray-700 mb-3">Şablon İşlemleri</h3>
            <div class="space-y-3">
                <div>
                    <label class="block text-sm text-gray-500 mb-1">Şablon Adı</label>
                    <input type="text" :value="templateName"
                        @input="templateName = ($event.target as HTMLInputElement).value"
                        placeholder="fatura_sablonu"
                        class="w-full px-3 py-2 border border-gray-200 rounded-md focus:outline-none focus:ring-0 focus:border-blue-500" />
                </div>
                <div>
                    <label class="block text-sm text-gray-500 mb-1">Şablon Tipi</label>
                    <select v-model="electronicType"
                        class="w-full px-3 py-3 text-sm border border-gray-200 rounded-md focus:ring-1 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                        <option value="5">Fatura</option>
                        <option value="6">İrsaliye</option>
                        <option value="7">Teklif</option>
                    </select>
                </div>
                <div class="flex flex-col gap-2">
                    <button :disabled="!templateName || !draggableItems.length" @click="handleSaveTemplate"
                        class="w-full px-3 py-2 text-sm bg-blue-100 disabled:opacity-50 disabled:cursor-not-allowed text-blue-600 rounded-md hover:bg-blue-100 transition-colors flex items-center justify-center gap-2">
                        <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd"
                                d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                                clip-rule="evenodd" />
                        </svg>
                        Şablonu Kaydet
                    </button>
                    <button @click="exportToJson('test', draggableItems)"
                        class="w-full px-3 py-2 text-sm bg-blue-100 disabled:opacity-50 disabled:cursor-not-allowed text-blue-600 rounded-md hover:bg-blue-100 transition-colors flex items-center justify-center gap-2">
                        <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd"
                                d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                                clip-rule="evenodd" />
                        </svg>
                        Şablonu JSON'a Dönüştür
                    </button>
                    <button @click="exportToHtml('test', draggableItems)"
                        class="w-full px-3 py-2 text-sm bg-blue-100 disabled:opacity-50 disabled:cursor-not-allowed text-blue-600 rounded-md hover:bg-blue-100 transition-colors flex items-center justify-center gap-2">
                        <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd"
                                d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                                clip-rule="evenodd" />
                        </svg>
                        Şablonu HTML'e Dönüştür
                    </button>
                    <button @click="printTemplate(draggableItems)"
                        class="w-full px-3 py-2 text-sm bg-green-100 disabled:opacity-50 disabled:cursor-not-allowed text-green-600 rounded-md hover:bg-green-100 transition-colors flex items-center justify-center gap-2">
                        <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd"
                                d="M5 4v3H4a2 2 0 00-2 2v3a2 2 0 002 2h1v2a2 2 0 002 2h6a2 2 0 002-2v-2h1a2 2 0 002-2V9a2 2 0 00-2-2h-1V4a2 2 0 00-2-2H7a2 2 0 00-2 2zm8 0H7v3h6V4zm0 8H7v4h6v-4z"
                                clip-rule="evenodd" />
                        </svg>
                        Şablonu Yazdır
                    </button> 
               
                    <button @click="exportToPdf('test', draggableItems)"
                        class="w-full px-3 py-2 text-sm bg-red-100 disabled:opacity-50 disabled:cursor-not-allowed text-red-600 rounded-md hover:bg-red-100 transition-colors flex items-center justify-center gap-2">
                        <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd"
                                d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                                clip-rule="evenodd" />
                        </svg>
                        Şablonu PDF'e Dönüştür
                    </button>
                        
                </div>
            </div>
        </div>

        <div v-if="!selectedItem" class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div class="flex items-center justify-center h-32 text-gray-400">
                <p class="text-sm">Özelliklerini düzenlemek için bir element seçin</p>
            </div>
        </div>

        <div v-if="selectedItem" class="space-y-4">
            <!-- Boyut Ayarları -->
            <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
                <h3 class="text-sm font-medium text-gray-700 mb-3">Boyut</h3>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs text-gray-500 mb-1">Genişlik</label>
                        <div class="relative">
                            <input type="number" v-model="selectedItem.size.width"
                                class="w-full px-3 py-1.5 text-sm border border-gray-200 rounded-md focus:ring-1 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                                min="50" />
                            <span class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-400">px</span>
                        </div>
                    </div>
                    <div>
                        <label class="block text-xs text-gray-500 mb-1">Yükseklik</label>
                        <div class="relative">
                            <input type="number" v-model="selectedItem.size.height"
                                class="w-full px-3 py-1.5 text-sm border border-gray-200 rounded-md focus:ring-1 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                                min="50" />
                            <span class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-400">px</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Yazı Ayarları -->
            <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
                <h3 class="text-sm font-medium text-gray-700 mb-3">Yazı</h3>
                <div class="space-y-3">
                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="block text-xs text-gray-500 mb-1">Font</label>
                            <select v-model="selectedItem.fontFamily"
                                class="w-full px-3 py-1.5 text-sm border border-gray-200 rounded-md focus:ring-1 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                                <option value="sans">Sans-serif</option>
                                <option value="serif">Serif</option>
                                <option value="mono">Monospace</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs text-gray-500 mb-1">Boyut</label>
                            <div class="relative">
                                <input type="number" v-model="selectedItem.fontSize"
                                    class="w-full px-3 py-1.5 text-sm border border-gray-200 rounded-md focus:ring-1 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                                    min="8" max="72" />
                                <span class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-400">px</span>
                            </div>
                        </div>
                    </div>
                    <div class="flex gap-2">
                        <button
                            @click="selectedItem.fontWeight = selectedItem.fontWeight === 'bold' ? 'normal' : 'bold'"
                            class="flex-1 p-2 rounded-md border transition-colors" :class="{
                                'bg-blue-50 border-blue-500 text-blue-600': selectedItem.fontWeight === 'bold',
                                'border-gray-200 text-gray-600 hover:bg-gray-50': selectedItem.fontWeight !== 'bold'
                            }">
                            <div class="flex justify-center">
                                <span class="font-bold">B</span>
                            </div>
                        </button>
                        <button
                            @click="selectedItem.fontStyle = selectedItem.fontStyle === 'italic' ? 'normal' : 'italic'"
                            class="flex-1 p-2 rounded-md border transition-colors" :class="{
                                'bg-blue-50 border-blue-500 text-blue-600': selectedItem.fontStyle === 'italic',
                                'border-gray-200 text-gray-600 hover:bg-gray-50': selectedItem.fontStyle !== 'italic'
                            }">
                            <div class="flex justify-center">
                                <span class="italic">I</span>
                            </div>
                        </button>
                        <button
                            @click="selectedItem.textDecoration = selectedItem.textDecoration === 'underline' ? 'none' : 'underline'"
                            class="flex-1 p-2 rounded-md border transition-colors" :class="{
                                'bg-blue-50 border-blue-500 text-blue-600': selectedItem.textDecoration === 'underline',
                                'border-gray-200 text-gray-600 hover:bg-gray-50': selectedItem.textDecoration !== 'underline'
                            }">
                            <div class="flex justify-center">
                                <span class="underline">U</span>
                            </div>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Hizalama Ayarları -->
            <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
                <h3 class="text-sm font-medium text-gray-700 mb-3">Hizalama</h3>
                <div class="flex gap-2">
                    <button v-for="align in ['left', 'center', 'right']" :key="align"
                        @click="selectedItem.textAlign = align as 'left' | 'center' | 'right'"
                        class="flex-1 p-2 rounded-md border transition-colors" :class="{
                            'bg-blue-50 border-blue-500 text-blue-600': selectedItem.textAlign === align,
                            'border-gray-200 text-gray-600 hover:bg-gray-50': selectedItem.textAlign !== align
                        }">
                        <div class="flex justify-center">
                            <svg v-if="align === 'left'" xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                stroke-linecap="round" stroke-linejoin="round">
                                <line x1="3" x2="21" y1="6" y2="6" />
                                <line x1="3" x2="13" y1="12" y2="12" />
                                <line x1="3" x2="21" y1="18" y2="18" />
                            </svg>
                            <svg v-if="align === 'center'" xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                stroke-linecap="round" stroke-linejoin="round">
                                <line x1="3" x2="21" y1="6" y2="6" />
                                <line x1="6" x2="18" y1="12" y2="12" />
                                <line x1="3" x2="21" y1="18" y2="18" />
                            </svg>
                            <svg v-if="align === 'right'" xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                stroke-linecap="round" stroke-linejoin="round">
                                <line x1="3" x2="21" y1="6" y2="6" />
                                <line x1="11" x2="21" y1="12" y2="12" />
                                <line x1="3" x2="21" y1="18" y2="18" />
                            </svg>
                        </div>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>