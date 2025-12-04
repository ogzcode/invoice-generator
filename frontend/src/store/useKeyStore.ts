import { defineStore } from "pinia"
import { ref } from "vue"

type KeyItem = {
    label: string
    value: string
}


type KeyState = {
    keyList: KeyItem[]
}

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
            this.keyList = this.keyList.filter(key => key !== keyToRemove)
        }
    }
})