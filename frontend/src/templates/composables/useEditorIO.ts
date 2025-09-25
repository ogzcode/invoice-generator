import { ref, Ref } from 'vue'
import type { DraggableItem, ExportData } from '../types/editor.ts'

function addDataKeysToTable(htmlContent: string, headers: string[]) {
    // Verilen HTML içeriğinden bir DOM nesnesi oluşturur
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlContent, 'text/html');

    // Tablo başlıklarını (<th>) ve tablo satırlarını (<tr>) seçer
    const thElements = doc.querySelectorAll('thead th');

    // Her bir başlık elemanına (th) data-key özniteliğini ekler
    thElements.forEach((th, index) => {
        if (headers[index]) {
            th.setAttribute('data-key', headers[index]);
        }
    });
    // Değiştirilmiş HTML içeriğini string olarak geri döndürür
    return doc.body.innerHTML;
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
            ${draggableItems.map(item => `
              <div class="item" data-key="${item.key}" style="
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
                ${item.type === 'table' ? addDataKeysToTable(item.content, item.headers) : item.content}
              </div>
            `).join('')}
          </div>
        </div>
      </body>
      </html>
    `
    return htmlContent

    /* const blob = new Blob([htmlContent], { type: 'text/html' })
    const url = URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.download = `${fileName}.html`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url) */
}

export const validateImportedData = (data: any): data is ExportData => {
    if (!data || typeof data !== 'object') return false
    if (!Array.isArray(data.pageItems)) return false
    if (typeof data.exportDate !== 'string') return false
    if (typeof data.pageSize !== 'string') return false

    return data.pageItems.every((item: any) => {
        return (
            item &&
            typeof item.id === 'string' &&
            typeof item.content === 'string' &&
            typeof item.type === 'string' &&
            item.position &&
            typeof item.position.x === 'number' &&
            typeof item.position.y === 'number' &&
            item.size &&
            typeof item.size.width === 'number' &&
            typeof item.size.height === 'number' &&
            typeof item.fontFamily === 'string' &&
            typeof item.fontSize === 'number' &&
            ['left', 'center', 'right'].includes(item.textAlign) &&
            ['normal', 'bold'].includes(item.fontWeight) &&
            ['normal', 'italic'].includes(item.fontStyle) &&
            ['none', 'underline'].includes(item.textDecoration)
        )
    })
}

export const importFromJson = async (file: File, draggableItems: DraggableItem[]) => {
    try {
        const content = await file.text()
        const importedData = JSON.parse(content)

        if (!validateImportedData(importedData)) {
            throw new Error('Geçersiz JSON formatı')
        }

        draggableItems = importedData.pageItems
    } catch (error) {
        console.error('JSON dosyası içe aktarılırken hata oluştu:', error)
        throw error
    }
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
                    <div class="item" data-key="${item.key}" style="
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
                        ${item.type === 'table' ? item.content : item.content}
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

export const exportToPdf = async (fileName: string, draggableItems: DraggableItem[]) => {
    try {
        // jsPDF'i dinamik olarak yükle
        const jsPDF = (await import('jspdf')).default

        // PDF oluştur (A4 boyutunda)
        const pdf = new jsPDF('p', 'mm', 'a4')
        const pageWidth = 210
        const pageHeight = 297

        // Sayfa arka planını beyaz yap
        pdf.setFillColor(255, 255, 255)
        pdf.rect(0, 0, pageWidth, pageHeight, 'F')

        // Her bir item'ı PDF'e ekle
        for (const item of draggableItems) {
            // Pozisyonu mm'ye çevir (piksel -> mm: / 3.78)
            const x = item.position.x / 3.78 + 7 // 7mm padding
            const y = item.position.y / 3.78 + 7 // 7mm padding

            // Font ayarları
            pdf.setFontSize(item.fontSize || 12)
            pdf.setTextColor(item.color || '#000000')

            // Font weight ve style
            let fontStyle = 'normal'
            if (item.fontWeight === 'bold' && item.fontStyle === 'italic') {
                fontStyle = 'bolditalic'
            } else if (item.fontWeight === 'bold') {
                fontStyle = 'bold'
            } else if (item.fontStyle === 'italic') {
                fontStyle = 'italic'
            }

            pdf.setFont('helvetica', fontStyle)

            if (item.type === 'table') {
                // Tablo için HTML içeriğini parse et
                const tempDiv = document.createElement('div')
                tempDiv.innerHTML = item.content

                const table = tempDiv.querySelector('table')
                if (table) {
                    const rows = Array.from(table.querySelectorAll('tr'))
                    let currentY = y

                    rows.forEach((row, rowIndex) => {
                        const cells = Array.from(row.querySelectorAll('td, th'))
                        let currentX = x
                        const cellWidth = (item.size.width / 3.78) / cells.length

                        cells.forEach((cell) => {
                            // Hücre çerçevesi
                            pdf.rect(currentX, currentY, cellWidth, 8)

                            // Hücre metni
                            const text = cell.textContent?.trim() || ''
                            pdf.text(text, currentX + 2, currentY + 5)

                            currentX += cellWidth
                        })

                        currentY += 8
                    })
                }
            } else {
                // Normal metin
                const lines = item.content.split('\n')
                const lineHeight = (item.fontSize || 12) * 0.35 // mm cinsinden satır yüksekliği

                lines.forEach((line, index) => {
                    const textY = y + (index * lineHeight)

                    // Text align
                    if (item.textAlign === 'center') {
                        const textWidth = pdf.getTextWidth(line)
                        const centerX = x + (item.size.width / 3.78 / 2) - (textWidth / 2)
                        pdf.text(line, centerX, textY)
                    } else if (item.textAlign === 'right') {
                        const textWidth = pdf.getTextWidth(line)
                        const rightX = x + (item.size.width / 3.78) - textWidth
                        pdf.text(line, rightX, textY)
                    } else {
                        pdf.text(line, x, textY)
                    }
                })
            }
        }

        // PDF'i indir
        pdf.save(`${fileName}.pdf`)

    } catch (error) {
        console.error('PDF oluşturulurken hata oluştu:', error)
        throw error
    }
}
