<script setup lang="ts">
import { ref } from 'vue';
import type { DraggableItem } from '../types/editor.ts'
import Input from '../../components/Input.vue';
import Dialog from '../../components/Dialog.vue';
import Button from '../../components/Button.vue';
import { File, AlignLeft, AlignCenter, AlignRight } from 'lucide-vue-next';

defineProps<{
    selectedItem: DraggableItem | undefined
    draggableItems: DraggableItem[]
}>()

const templateName = ref('test')
</script>

<template>
    <div class="px-4 bg-white min-h-screen overflow-y-auto">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">Düzenleme</h2>
        <!-- Dosya İşlemleri -->

        <Dialog>
            <template #button>
                <Button size="sm" variant="primary" class="w-full mb-4">
                    <File class="w-4 h-4 mr-2" />
                    Dosya İşlemleri
                </Button>
            </template>
            <template #content>
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Şablon Adı</label>
                        <Input v-model="templateName" placeholder="Şablon adını girin" />
                    </div>
                    <div class="flex gap-2">
                        <Button variant="secondary" class="flex-1">
                            Şablonu Dışa Aktar
                        </Button>
                    </div>
                </div>
            </template>
        </Dialog>

        <div v-if="!selectedItem" class="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
            <div class="flex items-center justify-center h-32 text-gray-400">
                <p class="text-sm">Özelliklerini düzenlemek için bir element seçin</p>
            </div>
        </div>
        <div v-else class="bg-pink-50 text-pink-500 border-b p-2 mb-4 font-medium">
            {{ selectedItem.label }} öğesini düzenliyorsunuz
        </div>

        <div v-if="selectedItem" class="space-y-4">
            <!-- Boyut Ayarları -->
            <div class="bg-white rounded-lg p-2 shadow-sm border border-gray-200">
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
            <div class="bg-white rounded-lg p-2 shadow-sm border border-gray-200">
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
                            class="flex-1 py-1 rounded-md border transition-colors" :class="{
                                'bg-blue-50 border-blue-500 text-blue-600': selectedItem.fontWeight === 'bold',
                                'border-gray-200 text-gray-600 hover:bg-gray-50': selectedItem.fontWeight !== 'bold'
                            }">
                            <div class="flex justify-center">
                                <span class="font-bold">B</span>
                            </div>
                        </button>
                        <button
                            @click="selectedItem.fontStyle = selectedItem.fontStyle === 'italic' ? 'normal' : 'italic'"
                            class="flex-1 py-1 rounded-md border transition-colors" :class="{
                                'bg-blue-50 border-blue-500 text-blue-600': selectedItem.fontStyle === 'italic',
                                'border-gray-200 text-gray-600 hover:bg-gray-50': selectedItem.fontStyle !== 'italic'
                            }">
                            <div class="flex justify-center">
                                <span class="italic">I</span>
                            </div>
                        </button>
                        <button
                            @click="selectedItem.textDecoration = selectedItem.textDecoration === 'underline' ? 'none' : 'underline'"
                            class="flex-1 py-1 rounded-md border transition-colors" :class="{
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
            <div class="bg-white rounded-lg p-2 shadow-sm border border-gray-200">
                <h3 class="text-sm font-medium text-gray-700 mb-3">Hizalama</h3>
                <div class="flex gap-2">
                    <button v-for="align in ['left', 'center', 'right']" :key="align"
                        @click="selectedItem.textAlign = align as 'left' | 'center' | 'right'"
                        class="flex-1 p-2 rounded-md border transition-colors" :class="{
                            'bg-blue-50 border-blue-500 text-blue-600': selectedItem.textAlign === align,
                            'border-gray-200 text-gray-600 hover:bg-gray-50': selectedItem.textAlign !== align
                        }">
                        <div class="flex justify-center">
                            <AlignLeft v-if="align === 'left'" class="w-4 h-4" />
                            <AlignCenter v-if="align === 'center'" class="w-4 h-4" />
                            <AlignRight v-if="align === 'right'" class="w-4 h-4" />
                        </div>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>