<template>
  <div class="table-wrapper">
    <table class="draggable-table w-full table-auto">
      <thead>
        <tr>
          <th v-for="col in columns || []" :key="col.value" :style="{ width: (col.width ? col.width + 'px' : 'auto'), textAlign: col.textAlign }">
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td v-for="col in columns || []" :key="col.value + '-row'" :style="{ textAlign: col.textAlign }">
            {{ col.value }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import type { DataColumn } from '../templates/types/editor.ts'

defineProps<{
  columns?: DataColumn[]
  // optional alignment prop if outer container wants to control justification
  align?: 'left' | 'center' | 'right'
}>()
</script>

<style scoped>
.draggable-table {
    border-collapse: collapse;
    width: 100%;
}

.draggable-table td {
    border: 1px solid #d1d5db;
    padding: 8px 16px;
}

.draggable-table tr:hover {
    background-color: #f9fafb;
}

.table-wrapper {
  width: 100%;
  height: 100%;
}
</style>
