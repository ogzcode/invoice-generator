import type { DraggableItem, ExportData } from '../types/editor.ts'

function escapeHtml(str: any) {
    if (str === null || str === undefined) return ''
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;')
}

function renderTableHtmlForItem(item: DraggableItem) {
    const cols = (item.dataColumns || [])
    const thead = `<tr>${cols.map(c => `<th data-key="${escapeHtml(c.value)}" style="border:1px solid #d1d5db;padding:8px;text-align:${escapeHtml(c.textAlign)};width:${c.width ? escapeHtml(c.width + 'px') : 'auto'}">${escapeHtml(c.label)}</th>`).join('')}</tr>`
    const tbody = `<tr>${cols.map(c => `<td style="border:1px solid #d1d5db;padding:8px;text-align:${escapeHtml(c.textAlign)}"></td>`).join('')}</tr>`
    return `<table style="border-collapse:collapse;width:100%;min-width:100%">${thead}<tbody>${tbody}</tbody></table>`
}

function renderItemDiv(item: DraggableItem) {
    // Render different inner content depending on item type
    const inner = (item.type === 'image') ? `
      <div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;">
        <div style="width:100%;height:100%;background:#f1f5f9;border:1px dashed #d1d5db;border-radius:6px;display:flex;align-items:center;justify-content:center;">
          <svg width="20" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
            <rect x="3" y="3" width="18" height="14" rx="1.5" stroke="#6b7280" stroke-width="1.2" fill="none" />
            <circle cx="8" cy="8" r="1.5" fill="#6b7280" />
            <path d="M3 17l5-6 4 5 3-4 6 6" stroke="#6b7280" stroke-width="1.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </div>
    ` : (item.type === 'table' ? '' : escapeHtml(item.value))

    return `
      <div class="item" data-key="${escapeHtml(item.value)}" style="
        position: absolute;
        left: ${escapeHtml(item.position.x)}px;
        top: ${escapeHtml(item.position.y)}px;
        width: ${escapeHtml(item.size.width)}px;
        height: ${escapeHtml(item.size.height)}px;
        font-family: ${escapeHtml(item.fontFamily || 'sans-serif')};
        font-size: ${escapeHtml(item.fontSize)}px;
        color: ${escapeHtml(item.color || '#000')};
        text-align: ${escapeHtml(item.textAlign || 'left')};
        font-weight: ${escapeHtml(item.fontWeight || 'normal')};
        font-style: ${escapeHtml(item.fontStyle || 'normal')};
        text-decoration: ${escapeHtml(item.textDecoration || 'none')};
        line-height: 1.5;
      ">
        ${inner}
      </div>
    `
}

export const exportToJson = (fileName: string, draggableItems: DraggableItem[]) => {
    const exportData: ExportData = {
        pageItems: draggableItems,
        exportDate: new Date().toISOString(),
        pageSize: 'A4'
    }

    const jsonString = JSON.stringify(exportData, null, 2)
    const blob = new Blob([jsonString], { type: 'application/json' })
    const url = URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.download = `${fileName}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
}

export const exportToHtml = (fileName: string = 'template', draggableItems: DraggableItem[]) => {
    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>${fileName}</title>
        <style>
          .preview-container {
            overflow: auto;
            padding: 20px;
            display: flex;
            justify-content: center;
          }
          
          .page {
            width: 210mm;
            min-height: 297mm;
            background: white;
            position: relative;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin: 0 auto;
          }
          
          .item {
            position: absolute;
            line-height: 1.5;
          }
          
          /* Tablo stilleri */
          .min-w-full {
            width: 100%;
          }
          
          .border-collapse {
            border-collapse: collapse;
          }
          
          .border {
            border-width: 1px;
          }
          
          .border-gray-300 {
            border-color: #d1d5db;
          }
          
          .px-4 {
            padding-left: 1rem;
            padding-right: 1rem;
          }
          
          .py-2 {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
          }
          
          .text-gray-700 {
            color: #374151;
          }
          
          .text-center {
            text-align: center;
          }
          
          @media print {
            .preview-container {
              padding: 0;
            }
            .page {
              margin: 0;
              padding: 20px;
              -webkit-print-color-adjust: exact;
              print-color-adjust: exact;
              box-shadow: none;
            }
          }
        </style>
      </head>
      <body>
        <div class="preview-container">
          <div class="page">
            ${draggableItems.map(item => item.type === 'table' ? renderItemDiv(item).replace('</div>', `${renderTableHtmlForItem(item)}</div>`) : renderItemDiv(item)).join('')}
          </div>
        </div>
      </body>
      </html>
    `
    //return htmlContent

    const blob = new Blob([htmlContent], { type: 'text/html' })
    const url = URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.download = `${fileName}.html`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
}

export const printTemplate = (draggableItems: DraggableItem[]) => {
    // Yazdırma için HTML içeriği oluştur
    const printContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Şablon Yazdırma</title>
            <style>
                @page {
                    size: A4;
                    margin: 0;
                }
                
                body {
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                }
                
                .print-container {
                    width: 210mm;
                    min-height: 297mm;
                    background: white;
                    position: relative;
                    padding: 20px;
                    margin: 0 auto;
                }
                
                .item {
                    position: absolute;
                    line-height: 1.5;
                }
                
                /* Tablo stilleri */
                .min-w-full {
                    width: 100%;
                }
                
                .border-collapse {
                    border-collapse: collapse;
                }
                
                .border {
                    border-width: 1px;
                }
                
                .border-gray-300 {
                    border-color: #d1d5db;
                }
                
                .px-4 {
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
                
                .py-2 {
                    padding-top: 0.5rem;
                    padding-bottom: 0.5rem;
                }
                
                .text-gray-700 {
                    color: #374151;
                }
                
                .text-center {
                    text-align: center;
                }
                
                @media print {
                    body {
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                    }
                    
                    .print-container {
                        margin: 0;
                        padding: 20px;
                        box-shadow: none;
                    }
                }
            </style>
        </head>
        <body>
            <div class="print-container">
                ${draggableItems.map(item => item.type === 'table' ? renderItemDiv(item).replace('</div>', `${renderTableHtmlForItem(item)}</div>`) : renderItemDiv(item)).join('')}
            </div>
        </body>
        </html>
    `

    // Yeni pencere aç ve yazdırma diyaloğunu göster
    const printWindow = window.open('', '_blank')
    if (printWindow) {
        printWindow.document.write(printContent)
        printWindow.document.close()

        // Sayfa yüklendikten sonra yazdırma diyaloğunu aç
        printWindow.onload = () => {
            printWindow.print()
            // Yazdırma tamamlandıktan sonra pencereyi kapat
            printWindow.onafterprint = () => {
                printWindow.close()
            }
        }
    }
}