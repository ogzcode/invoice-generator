<template>
  <div class="inline-block">
    <button
      ref="reference"
      type="button"
      @click="toggle"
    >
      <slot name="button">{{ buttonLabel }}</slot>
    </button>

    <teleport to="body">
      <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40" @click="close" />

        <!-- Centered mode -->
        <div
          v-if="props.centered"
          ref="floating"
          role="dialog"
          aria-modal="true"
          tabindex="-1"
          :class="dialogClassComputed"
        >
          <div>
            <slot name="content" />
          </div>
          <div class="mt-3">
            <slot name="actions" />
          </div>
        </div>

        <!-- Anchored mode (uses Floating UI styles) -->
        <div
          v-else
          ref="floating"
          :style="floatingStyles"
          role="dialog"
          aria-modal="true"
          tabindex="-1"
          :class="[props.dialogClass || 'bg-white shadow-lg rounded-md p-4', 'min-w-[200px] z-50 pointer-events-auto']"
        >
          <div>
            <slot name="content" />
          </div>
          <div class="mt-3">
            <slot name="actions" />
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useFloating, offset, flip, shift, autoUpdate } from '@floating-ui/vue'

const props = defineProps({
  placement: { type: String, default: 'bottom-start' },
  buttonLabel: { type: String, default: 'Open' },
  buttonClass: { type: String, default: '' },
  dialogClass: { type: String, default: '' },
  closeOnOutside: { type: Boolean, default: true },
  centered: { type: Boolean, default: true },
  size: { type: String, default: 'medium' }, // small | medium | large
})

const reference = ref<HTMLElement | null>(null)
const floating = ref<HTMLElement | null>(null)
const open = ref(false)

const { floatingStyles, update } = useFloating(reference, floating, {
  placement: props.placement as any,
  middleware: [offset(8), flip(), shift()],
  whileElementsMounted: autoUpdate,
})

function close() {
  open.value = false
}

function sizeClassFor(size: string) {
  switch (size) {
    case 'small':
      return 'w-xl'
    case 'large':
      return 'max-w-3xl w-full'
    case 'medium':
      return 'w-2xl'
    default:
      return 'w-96'
  }
}

const sizeClass = sizeClassFor(props.size)
const dialogClassComputed = `${props.dialogClass || 'bg-white shadow-lg rounded-md p-4'} ${sizeClass} z-50 pointer-events-auto`

function toggle() {
  open.value = !open.value
}

function setOpen(value: boolean) {
  open.value = value
}

// Expose control functions/refs to parent components (use with `ref` on this component)
defineExpose({ open, setOpen, toggle, close })

function onDocumentClick(e: MouseEvent) {
  if (!props.closeOnOutside) return
  const target = e.target as Node | null
  const refEl = reference.value
  const floatEl = floating.value
  if (!refEl || !floatEl) return
  if (refEl.contains(target)) return
  if (floatEl.contains(target)) return
  open.value = false
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') open.value = false
}

watch(open, (v) => {
  if (v) {
    // position once opened
    update?.()
    // focus the floating element for accessibility
    setTimeout(() => floating.value?.focus(), 0)
  }
})

onMounted(() => {
  document.addEventListener('click', onDocumentClick)
  document.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onDocumentClick)
  document.removeEventListener('keydown', onKeydown)
})
</script>

<style scoped>
/* Visuals use Tailwind classes in template; keep the style block for future local tweaks */
</style>
