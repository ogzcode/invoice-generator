import type { DraggableItem, ExportData } from '../types/editor.ts'

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
            ${draggableItems.map(item => `
              <div class="item" data-key="${item.value}" style="
                position: absolute;
                left: ${item.position.x}px;
                top: ${item.position.y}px;
                width: ${item.size.width}px;
                min-height: ${item.size.height}px;
                font-family: ${item.fontFamily || 'sans-serif'};
                font-size: ${item.fontSize}px;
                color: ${item.color || '#000'};
                text-align: ${item.textAlign || 'left'};
                font-weight: ${item.fontWeight || 'normal'};
                font-style: ${item.fontStyle || 'normal'};
                text-decoration: ${item.textDecoration || 'none'};
                line-height: 1.5;
              ">
                ${item.label}
              </div>
            `).join('')}
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
                ${draggableItems.map(item => `
                    <div class="item" data-key="${item.value}" style="
                        position: absolute;
                        left: ${item.position.x}px;
                        top: ${item.position.y}px;
                        width: ${item.size.width}px;
                        min-height: ${item.size.height}px;
                        font-family: ${item.fontFamily || 'Arial, sans-serif'};
                        font-size: ${item.fontSize}px;
                        color: ${item.color || '#000'};
                        text-align: ${item.textAlign || 'left'};
                        font-weight: ${item.fontWeight || 'normal'};
                        font-style: ${item.fontStyle || 'normal'};
                        text-decoration: ${item.textDecoration || 'none'};
                        line-height: 1.5;
                    ">
                        ${item.label}
                    </div>
                `).join('')}
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