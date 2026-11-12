> Tarihsel sürüm kaydı. Güncel yayın v1.3.1; [güncel belge denetimi](../reports/documentation_checks.json). Arşiv/konuşma kopyaları yerel teslimde korunur, Git yayınına dahil değildir.

# τMOTION v1.3 — Nihai mimari kapsam ve belge bütünlük denetimi

**Kapsam:** v1.2 mimari topolojisi üzerine 12 Kasım 2026 tarihli dokümantasyon/marka güncellemesi. **Bu denetim, araç sürüşü veya modellerin gerçek çalışma başarısı hakkında hiçbir kanıt sağlamaz.** Kullanıcının güncel amacı eksiksiz tasarım tanımıdır.

**Kontrol edilen:** 24 M00–M23 modülü, 54 kenar, 24 modül için gerekçe/girdi/çıktı/eğitim/hata alanları, İngilizce eşlikçi, girdi-çıktı sözleşmeleri, offline future-data ayrımı, kritik critic/GRU/CoT/RL/NMPC yöntemleri, klasik Autoware/AutoE2E ayrımı, sayısal tahminlerin epistemik statüsü, güncel orijinal LiDAR'sız logo, eski üç arşiv sürümü, U01–U25 geçmişi ve PDF.

## Yapısal doğrulama sonucu

**50/50 PASS**. Ayrıntılı makine okunur kontrol kaydı: `reports/documentation_checks_v1_3.json`.

| Bütünlük katmanı | Durum | Kanıt |
|---|---|---|
| Mimari modül envanteri | 24/24 | `specs/components.json` + master TR/EN |
| Bağlantı grafiği | 54/54 | `specs/architecture_edges.json` |
| Modül sözleşmeleri | reason/input/output/bridge/training/failure | `components.json` ve `FINAL_ARCHITECTURE_MASTER_TR.md` |
| Öğrenilmiş critic ve offline teacher | M10/M21 ve bağlantıları korunur | `docs/safety-critic-and-supervision.md` + `docs/training-and-data-v1.2.md` |
| AutoE2E ve klasik Autoware kapsamı | Önceden mevcut yöntemler yeniden sayılmadı | `docs/autoware-and-hybrid-e2e-v1.3.md` |
| Benchmark senaryoları | Tahmin/ölçüm ayrımı korundu | `specs/benchmark_expectations_v1_3.json` |
| Yeni logo | Byte-identical PNG + SHA256 | `docs/brand-approved-v1.3.md` |
| Konuşma eki | U01–U25 görünür kullanıcı mesajları, asistan özetleri ayrı | `history/` |
| PDF | Ana Türkçe ve İngilizce teknik mimariyi kapsar | `reports/TAUMOTION_Final_Architecture_Specification_v1_3.pdf` |

## Kapsamın gerekçeli tanımı

**Tam olarak tanımlı:** Tüm modül kimlikleri, gereklilikleri, input/output sözleşmeleri, source privilege, semantik/algı/planlama/critic/RL/kontrol veri geçişleri, hiyerarşik eğitim akışı ve ödül/risk ayrımı, kontrollü karar izinleri, Autoware/AutoE2E benchmark rolleri, akademik Hybrid End-to-End tanımı ve marka onayı. Ayrıntılar master TR, eski yöntem/arayüz belgeleri ve source pin'lerde korunur.

**Bu sürümün bilinçli biçimde kapsam dışı tuttuğu şeyler:** Gerçek CARLA/vehicle çalıştırması, ağırlıkların eğitilmesi, 20 Hz'nin ölçülmesi, parametrik araç kalibrasyonu, fonksiyonel güvenlik sertifikası veya yeni yayımlanmış τMOTION benchmark sonucu. Bu konuların tamamlanmamış olması, şu andaki **mimari tanım tamlığında eksik belge** olarak sayılmaz; ileride implementation/evaluation kapısıdır.

**Teknik varsayımlar:** İki donmuş temel modelin CARLA/NAVSIM'e adapte edilmesi, safety critic kalibrasyonu, çoklu hedef etiket doğruluğu, dağıtılmış GPU bütçesi ve gerçek zamanlı gecikme hedefleri, nihai tasarımda varsayım olarak tanımlıdır; gerçek sonuçlar bunları doğrulamak içindir. İlave üçüncü zorunlu planner yoktur.

## Ayrıntılı dosya denetimleri

- [x] 24 canonical modules
- [x] 54 canonical directed edges
- [x] 24 modules described individually in master TR
- [x] 24 modules in companion EN
- [x] required canonical field present: necessity — module metadata
- [x] required canonical field present: input — module metadata
- [x] required canonical field present: output — module metadata
- [x] required canonical field present: training — module metadata
- [x] required canonical field present: failure — module metadata
- [x] required canonical field present: bridge — module metadata
- [x] required canonical field present: source — module metadata
- [x] master technical coverage: hybrid E2E scope
- [x] master technical coverage: not monolithic
- [x] master technical coverage: offline teacher policy separation
- [x] master technical coverage: critic differentiation
- [x] master technical coverage: bounded residual
- [x] master technical coverage: dual planner K6
- [x] master technical coverage: NMPC state
- [x] master technical coverage: independent guardian
- [x] master technical coverage: separate stale evidence
- [x] master technical coverage: XAI world intervention
- [x] master technical coverage: AutoE2E already included
- [x] master technical coverage: classic Autoware baseline
- [x] master technical coverage: all benchmark targets
- [x] master technical coverage: no roof LiDAR
- [x] logo PNG correct and hash locked
- [x] new logo approval and old logo both preserved
- [x] brand docs clarify raster and no lidar
- [x] forecast status explicitly unmeasured
- [x] benchmark matrix six metrics
- [x] Autoware positions documented
- [x] no third mandatory planner
- [x] history old U01-U15 intact
- [x] new history U16-U25 complete
- [x] assistant summaries non-verbatim marked
- [x] historical v1_0 zip archive preserved
- [x] historical v1_1 zip archive preserved
- [x] historical v1_2 zip archive preserved
- [x] v1.2 historical archive byte for byte
- [x] existing vector diagram online_tr
- [x] existing vector diagram online_en
- [x] existing vector diagram offline_tr
- [x] existing vector diagram offline_en
- [x] existing vector diagram control_tr
- [x] existing vector diagram control_en
- [x] existing vector diagram full_modules_tr
- [x] existing vector diagram full_modules_en
- [x] authoritative Markdown local links all resolve — []
- [x] final PDF opens and has >=35 pages — pages=61
- [x] final PDF current branding/version
