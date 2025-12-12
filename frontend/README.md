# Frontend — Proje Teknik Dokümantasyonu

Bu belge `frontend/` klasöründeki yapı, önemli dosyalar, çalışma talimatları ve geliştirme önerilerini özetler. Proje Vite + Vue 3 + TypeScript temelli bir ön yüz uygulamasıdır (tek sayfa uygulama).

## Özet

- Teknoloji: Vite, Vue 3, TypeScript
- Ana giriş: `src/main.ts`
- Ana uygulama: `src/App.vue`
- Durum yönetimi: `src/store/useKeyStore.ts` (Pinia benzeri store kompozisyonu)
- UI bileşenleri: `src/components/` altında Vue bileşenleri (`Button.vue`, `Dialog.vue`, `Input.vue`, `TableItem.vue`, vb.)
- Şablon editörü: `src/templates/` altında editör ve şablon bileşenleri (ör. `TemplateAction.vue`, `MainEditor.vue`, `TableEditor.vue`)
- Styles: `src/style.css`
- Vite config: `vite.config.ts`
- Paket yönetimi: `package.json`

## Önemli Dosyalar ve Roller

- `index.html` — Vite giriş HTML.
- `package.json` — scriptler ve bağımlılıklar. (Çalıştırma, build, lint vb.)
- `vite.config.ts` — Vite yapılandırması.
- `src/main.ts` — uygulamayı başlatır, global eklentiler ve store burada bootstrap edilir.
- `src/App.vue` — uygulama kabı.
- `src/components/` — tekrar kullanılabilir UI bileşenleri.
- `src/templates/` — şablon düzenleme ve aktarım işlevselliği:
  - `components/` — editör alt bileşenleri (Dragging, Resizing, Sidebar, vb.).
  - `composables/` — `useDraggable.ts`, `useEditorIO.ts`, `useResizable.ts` gibi yeniden kullanılabilir mantık.
  - `constants/`, `types/`, `data/` — sabitler, TypeScript tipleri ve örnek veri.

## Çalıştırma (Geliştirme ve Derleme)

1. Bağımlılıkları yükleyin:

```bash
npm install
```

2. Geliştirme sunucusunu çalıştırın:

```bash
npm run dev
```

3. Üretim için derleme:

```bash
npm run build
```

4. Üretim çıktısını yerel sunucuda test etmek için:

```bash
npm run preview
```

(Script isimleri `package.json` içinde farklıysa ona göre uyarlayın.)

## Mimari Notlar

- Kompozisyon API (composables) kullanımı bileşen mantığını test edilebilir ve yeniden kullanılabilir parçalara ayırır.
- `useEditorIO.ts` muhtemelen JSON şablonları ile I/O (import/export) işlerini yapar — backend `json_process.py` ile aynı JSON şeması üzerinden uyumluluk sağlanmalı.
- `useDraggable.ts` ve `useResizable.ts` bileşenlerin sol/üst/width/height konum verisi ile çalışır; bu veriler backend tarafındaki `pageItems` ile eşleşmelidir.

## Geliştirme Önerileri ve Dikkat Edilecekler

- Tip Güvenliği: `src/templates/types` içindeki tipleri genişletin ve `tsconfig` kurallarını sıkılaştırın (noImplicitAny vb.)
- Testler: Bileşen testleri (Vitest/Jest) ekleyin; özellikle `composables` ve `store` için birim testleri faydalı.
- E2E: Şablon oluşturma → backend dönüşümü (HTML üretim) akışını doğrulayan bir E2E testi oluşturun.
- Performans: Büyük şablonlarda drag/resize olaylarını throttling/debounce ile optimize edin.
- Accessibility: Form bileşenleri (`Input`, `Select`, `Button`) için ARIA ve klavye erişilebilirliği doğrulayın.
- Stil Yönetimi: `style.css` global stiller içeriyorsa, bileşen bazlı CSS (scoped veya CSS modules) kullanılmasını düşünün.
- State Persistence: Kullanıcı şablonları yerel depolama veya backend (API) ile senkronize edilebilecek şekilde persistente edin.

## Entegrasyon Notları (Backend ile)

- JSON şablon formatı frontend editöründen export edilirken `backend/json_process.py`'de beklenen `pageItems`, `pageSize`, `dataColumns` gibi alanlarla uyumlu olmalıdır.
- Görsel alanlar için frontend `image` öğelerine URL veya base64 verisi sağlayabiliyorsa backend `create_image_element` fonksiyonunun desteklediği formatlarla eşleştiğinden emin olun.
- Tablo kolon tanımları (`dataColumns`) içindeki `textAlign`, `width`, `label` gibi alanların hem frontend düzenleyicide hem backend renderer'da aynı anlamı taşıması gerekir.

## Hızlı Kontrol Listesi (Kod Gözden Geçirme İçin)

- `src/templates/composables` fonksiyonları saf (pure) ve test edilebilir mi?
- `useKeyStore.ts` store yapısı uygun şekilde tiplenmiş mi?
- Bileşenlerin props/emitleri doğru tiplenmiş ve validasyon yapılmış mı?
- `package.json` scriptleri projenin CI/CD akışına uygun mu?

## Hızlı Komutlar

- Geliştirme: `npm run dev`
- Üretim build: `npm run build`
- Preview: `npm run preview`
- Bağımlılık yükle: `npm install`

---

Bu README frontend yapısının kısa ama kapsamlı bir özetini sağlar. İsterseniz benzer şekilde örnek bir JSON export/girdi şeması, birim test şablonları veya `useEditorIO` için bir test harness ekleyebilirim.
