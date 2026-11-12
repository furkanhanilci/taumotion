# Uygulama sırası ve teslim kapıları

**Güncel yayın: v1.3.1.** [Entegrasyon sözleşmesi](integration-contract-v1.3.1.md) bu belgedeki nominal ufuk, veri kapsamı ve sürüm uyumluluğunu kesinleştirir; tüm yöntemler korunur.

Bu sıra işin tamamını uygulanabilir paketlere böler; hiçbir araştırma ailesi kapsam dışına çıkarılmaz. Kaynakların çoğu hazır olsa da çoklu model entegrasyonu ana emek kalemidir. Süre tahmini model/benchmark smoke testlerinden önce kesinleştirilmez.

## G0 — Kaynak ve ortam
source_pins.json içindeki commitleri ayrı bağımlılıklar olarak al; LICENSE/model card ve veri kullanım koşullarını o commit/checkpoint için kaydet. Checkpoint URL/revision/SHA256, input örneği ve resmi inference komutu oluştur. Algı, iki planlayıcı, policy ve benchmark ortamlarını ayır. Çıktı: çalıştırılabilir env manifestleri ve native tek örnek logları.

Kapı: kaynak sürümleri gerçekten import/forward yapıyor; ağırlık strict-load uyumlu; eksik token/weights gibi durumlar listeli. Kaynak inceleme yapılmış olması bu kapının geçildiği anlamına gelmez.

## G1 — Hazır parçaların eşdeğer adaptörleri
B01–B04: native ve adapter çıktısını aynı örnekte karşılaştır. ReCog online-cache yolunu düzelt; Zoo'nun 0.0.4 dalını kullan; Tiny/Base config ile checkpoint tensor şekillerini denetle. K=1 eşdeğerliği bitmeden K batch veya performans optimizasyonu yapılmaz. Çıktı: scene/native/candidate/evidence sözleşmeleri ve golden örnekler.

Kapı: koordinat/zaman/sensör eşlemesi; NaN/missing durumları; future leakage engeli. Başarısızlık modül silme değil adaptör düzeltmesi doğurur.

## G1.5 — Erken birlikte çalışma ve zaman pilotu
Model worker'ları RL eğitimi başlamadan birlikte profillenir. M03/M07 paylaşılan VLM servisi, GPU yerleşimi, CARLA renderer ve CPU hazırlığı aynı ölçümde yer alır. Bir bekleyen istek kuyruğu, geç sonuç reddi ve M22/M23 sözleşmeleri hazırlanır. Bu kapı G5'e ertelenmez. Çıktı: aday frekans/yaş zarfı, episode/saat ve henüz karşılanamayan bütçeler.

## G2 — Ortak kontrol hattı
Önce hazır klasik rota üreticisiyle NMPC'yi kapalı döngü çalıştır. Araç parametrelerini ve aktüatör dönüşümünü tanıla. Düşük hız, durma, viraj ve engel senaryolarını doğrula. Sonra A/B adayını bağla. Çıktı: C3/C4/C5 ortak controller koşulları.

Kapı: solver status, izleme ve deadline izleri; şerit/engel limitlerinin hangi koşulda slack kullandığı; fallback reason kayıtları. Bu erken aşama, aylarca politika eğitip kontrol adaptör hatasını sonradan keşfetmeyi önler.

## G3 — Semantik, kanıt ve offline seçim
AutoE2E taxonomy/head/coupling parçalarını al; claim/evidence eşlemesini ekle. Train teacher etiketleri üret, validation kalibrasyonu yap. E2 complementarity ve E3 heuristic/supervised/bandit başlat. Çıktı: aynı candidate cache üzerinde tekrarlanabilir selector deneyi, teacher/student veri seti.

Kapı: claim doğruluk ve coverage ölçümleri; model confidence kalibre edilmeden güven diye kullanılmıyor; oracle yalnız training/eval yolunda. Semantik kazanç negatifse bu bulgu korunur.

## G4 — Küçük politika ve residual
G4a: offline supervised başlangıç ve küçük closed-loop veri turu. G4b: sınırlı CARLA PPO pilotu; aday koşullu residual, GRU, mask/logp ve aynı shield/guardian doğrulaması. G4c: CVaR η/λ ve tail pilotu. G4d: kilitli protokolle tam seed/episode deneyleri. Her aşamada episode duvar süresi, etkin paralellik ve toplam bütçe çıkarılır. Olumsuz yöntem sonucu kapsamdan çıkarma değildir.

Kapı: örneklenen eylem ile öğrenilen logp tutarlı; warmstart/hidden state episode sınırında reset; eğitim testten ayrı. Sadece reward eğrisi yeterli değildir.

## G5 — Tüm benchmark ve kaynak profilleri
NAVSIM v1.1/v2.1.2, KITScenes, Bench2Drive tam test; Robust ve OOD; P0–P3; Qwen3.8 ve student kıyası. Çıktı: T01–T12 temel tablolar, koşul/sürüm ve CI.

Kapı: published/reproduced ayrımı; partial runs görünür; eşit K ve hesap bütçesi; gecikme enjeksiyonu. Büyük modeller aynı anda GPU'ya sığmazsa worker sıralama/quantization profili denenir; model kapsamdan çıkarılmaz.

## G6 — XAI, veri döngüsü ve aktarım
E10/E10-H, E13/E14, E15. Kontrollü semantik ve çevresel müdahaleler ayrılır. İnsan çalışması teknik doğrulama tamamlandıktan sonra yürür. Çıktı: açıklama etkisi, kullanıcı anlama/güven, veri çeşitliliği ve keşifsel aktarım raporu.

Kapı: no-op müdahalede state restore; yanlı örnek seçimi kontrolü; test seti veri döngüsüne girmiyor.

## G7 — Tez ve yeniden üretim
Kod kaynağı ve adaptör katkısı açık; tüm RQ/E ailesi sonuç veya belgelenmiş teknik bulgu ile kapanır. Negatif bulgular tartışma bölümüne girer. Model/data/env manifests, komutlar, kaynak tabloları, failure atlas ve şekiller teslim edilir.

## Entegrasyon riskleri ve hazırlanan yanıt
| Risk | Somut yanıt | Korunan işlev |
|---|---|---|
| Native rig farklı | Resmi preprocessing + ayrı sensor privilege; uygun backend kalibrasyonu | İki üretici ve adil kıyas |
| Eski algı ortamı / modern TorchRL | Ayrı worker, sürümlü paket | Hazır algı ve küçük RL |
| Ara kanıt çıktıları siliniyor | return_evidence yaması ve native eşdeğerliği | Bağımsız grounding |
| Trafik ışığı state yok | Hazır ROI classifier + şerit ilişkisi | Kural kanıtı |
| Canlı sahnede cache yok | Gerçek online worker; exact-request cache | Kapalı döngü |
| Çift model maliyeti fazla | P0 referans + P1/P2/P3 ölçümü | Tam mimari ve verimlilik araştırması |
| Residual uygulanamıyor | Bounded knotlar + yeniden kontrol + geri besleme | Residual ve NMPC araştırması |
| CVaR örneği az | Tail sayısı açık, yeterli on-policy episode, α duyarlılık | Risk araştırması |
| XAI etkisi shield'da kayboluyor | Beş aşamalı karar izi | Açıklama ve kontrol katkısı |
| Alan kayması | Native/adapted koşullar ayrı, kalibrasyon ve E9/E14 | Genelleme |

## v1.2 addendum — current specification supersedes applicable v1.1 text

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.
