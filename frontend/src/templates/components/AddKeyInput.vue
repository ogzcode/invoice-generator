<template>
    <Dialog>
        <template #button>
            <Button variant="secondary" size="sm">
                <Plus class="w-5 h-5 mr-2" />
                Anahtar Ekle
            </Button>
        </template>
        <template #content>
            <label class="block mb-2 font-medium text-gray-700">Yeni Anahtar Ekle</label>
            <div class="my-2">
                <label class="block text-sm font-medium text-stone-700">Anahtar Etiketi</label>
                <Input v-model="keyText" placeholder="Anahtar etiketi girin" />
            </div>
            <div class="my-2">
                <label class="block text-sm font-medium text-stone-700">Anahtar Değeri</label>
                <Input v-model="keyValue" placeholder="Anahtar değeri girin" />
            </div>

        </template>
        <template #actions>
            <div class="flex justify-end">
                <Button variant="primary" @click="onAdd" :disabled="btnDisabled">
                    <Plus class="w-5 h-5 mr-2 " />
                    Ekle
                </Button>
            </div>
        </template>
    </Dialog>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useKeyStore } from '../../store/useKeyStore'
import Dialog from '../../components/Dialog.vue'
import Input from '../../components/Input.vue'
import Button from '../../components/Button.vue'
import { Plus } from 'lucide-vue-next'

const keyStore = useKeyStore()
const keyText = ref('')
const keyValue = ref('')

function onAdd() {

    // Use same string for both label and value since only one input was requested
    keyStore.addKey({ label: keyText.value, value: keyValue.value })
    keyText.value = ''
    keyValue.value = ''
}

const btnDisabled = computed(() => {
    return !keyText.value.trim() || !keyValue.value.trim()
})
</script>

<style scoped>
/* Styling handled via Tailwind classes in the template */
</style>