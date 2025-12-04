import { defineStore } from "pinia"
import { ref } from "vue"
import type { KeyItem } from "../templates/types/editor"

export const useKeyStore = defineStore("keys", {
    state: () => ({
        keyList: ref<KeyItem[]>([]),
    }),
    actions: {  
        addKey(newKey: KeyItem) {
            if (!this.keyList.includes(newKey)) {
                this.keyList.push(newKey)
            }
        },
        removeKey(keyToRemove: KeyItem) {
            this.keyList = this.keyList.filter(key => key.value !== keyToRemove.value)
        }
    }
})