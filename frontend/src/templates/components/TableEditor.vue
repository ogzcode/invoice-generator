<template>
    <div>
        <Dialog ref="dialogRef">
            <template #button>
                <Button size="sm" variant="primary">
                    <Columns2 class="w-5 h-5 mr-2"/>
                    Tablo Sütunları
                </Button>
            </template>

            <template #content>
                <div class="space-y-3 max-h-[60vh] overflow-auto">
                    <div v-if="localColumns.length === 0" class="text-sm text-gray-500">Henüz sütun yok. Aşağıdan
                        ekleyin.</div>

                    <div v-for="(col, idx) in localColumns" :key="idx"
                        class="grid grid-cols-12 gap-2 items-end p-2 border-b border-gray-200 rounded">
                        <div class="col-span-3">
                            <label class="block text-xs text-gray-500 mb-1">Başlık</label>
                            <Input v-model="col.label" class="w-full px-2 py-1 text-sm border rounded" />
                        </div>

                        <div class="col-span-3">
                            <label class="block text-xs text-gray-500 mb-1">Değer (anahtar)</label>
                            <Input v-model="col.value" class="w-full px-2 py-1 text-sm border rounded" />
                        </div>

                        <div class="col-span-2">
                            <label class="block text-xs text-gray-500 mb-1">Genişlik (px)</label>
                            <Input type="number" v-model.number="col.width" min="20"
                                class="w-full px-2 py-1 text-sm border rounded" />
                        </div>

                        <div class="col-span-2">
                            <label class="block text-xs text-gray-500 mb-1">Hizalama</label>
                            <Select v-model="col.textAlign" :options="[
                                { label: 'Sol', value: 'left' },
                                { label: 'Orta', value: 'center' },
                                { label: 'Sağ', value: 'right' },
                            ]" />
                        </div>

                        <div class="col-span-2 flex items-center justify-end gap-2">
                            <Button variant="danger" @click="removeColumn(idx)"
                                class="text-sm text-red-600 hover:underline">
                                <Trash class="w-4 h-4 mr-1 inline" />
                            </Button>
                        </div>
                    </div>

                    <div class="pt-2">
                        <Button variant="primary" @click="addColumn"
                            class="px-3 py-1 text-sm bg-gray-100 rounded border">+ Sütun Ekle</Button>
                    </div>
                </div>
            </template>

            <template #actions>
                <div class="flex justify-end gap-2">
                    <Button variant="secondary" @click="cancel">
                        <X class="w-5 h-5 mr-2" />
                        İptal
                    </Button>
                    <Button variant="primary" @click="save">
                        <Check class="w-5 h-5 mr-2" />
                        Kaydet
                    </Button>
                </div>
            </template>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Dialog from '../../components/Dialog.vue'
import Button from '../../components/Button.vue'
import type { DataColumn } from '../types/editor.ts'
import Input from '../../components/Input.vue';
import Select from '../../components/Select.vue';
import { Check, Columns2, Trash, X } from 'lucide-vue-next';

const props = defineProps<{
    modelValue?: DataColumn[]
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: DataColumn[]): void
}>()

const dialogRef = ref<any | null>(null)

// local editable copy so we can cancel edits
const localColumns = ref<DataColumn[]>(JSON.parse(JSON.stringify(props.modelValue || [])))

watch(() => props.modelValue, (v) => {
    localColumns.value = JSON.parse(JSON.stringify(v || []))
})

function addColumn() {
    localColumns.value.push({
        label: 'Yeni Sütun',
        value: `col_${Date.now()}`,
        width: 120,
        textAlign: 'left'
    } as DataColumn)
}

function removeColumn(index: number) {
    localColumns.value.splice(index, 1)
}

function save() {
    // ensure width is a number and sane defaults
    localColumns.value = localColumns.value.map(c => ({
        label: c.label || '',
        value: c.value || '',
        width: Number(c.width) || 120,
        textAlign: c.textAlign || 'left'
    }))
    emit('update:modelValue', JSON.parse(JSON.stringify(localColumns.value)))
    dialogRef.value?.setOpen(false)
}

function cancel() {
    // revert local changes
    localColumns.value = JSON.parse(JSON.stringify(props.modelValue || []))
    dialogRef.value?.setOpen(false)
}
</script>