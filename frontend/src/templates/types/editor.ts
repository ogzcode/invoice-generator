export interface Position {
  x: number
  y: number
}

export interface Size {
  width: number
  height: number
}

export interface DraggableItem {
  id: string
  label: string
  value: string
  type: 'text' | 'table'
  position: {
    x: number
    y: number
  }
  size: {
    width: number
    height: number
  }
  fontFamily: string
  fontSize: number
  color?: string
  textAlign: 'left' | 'center' | 'right'
  fontWeight: 'normal' | 'bold'
  fontStyle: 'normal' | 'italic'
  textDecoration: 'none' | 'underline'
}

export interface ExportData {
  pageItems: DraggableItem[]
  exportDate: string
  pageSize: string
}

export interface ProductTableData {
  headers: string[];
  rows: string[][];
}

export interface DraggableTableItem extends DraggableItem {
  type: 'table';
  tableData: ProductTableData;
  headers: string[];
} 

export type KeyItem = {
    label: string
    value: string
}