# Architecture Specification v1.2 — değişiklik kaydı ve karar gerekçesi

**Tarih:** 11 Kasım 2026. **Durum:** TASARIM / DEĞERLENDİRME PLANI; model inference, kaynak adaptörleri ve gerçek sürüş doğrulaması henüz gerçekleştirilmedi. Bu sürüm, kullanıcının v1.1 sonrası görüşmelerde verdiği açık kararları kapsamı daraltmadan belgeye işler.

## Değişmeyen mimari ilkeler

1. Marka adı **τMOTION**. Ana görsellerde **daha önce onaylanan mor τ / zarif MOTION logosu korunur**; yeni, ilgisiz simge kullanılmaz. Onaylanan görsel `assets/brand/APPROVED_PURPLE_TAU_REFERENCE_UNMODIFIED.png` içinde *aynen* saklanır. Eski v1.1 turkuaz SVG dosyaları kaybolmasın diye korunur, ancak bu onaylanan kimlik değildir.
2. M00–M23 biçiminde **24 ana modül** korunur. Yeni öğrenilmiş safety critic, **M10'un alt bileşeni**; uzman verisi ve çok hedefli etiketler **M00/M06/M17/M20/M21 çevrim dışı süreçleri**; üçüncü büyük planlayıcı **zorunlu değildir**.
3. Önceki VLM/CoT, horizon-aware reasoning, independent perception/grounding, iki dondurulmuş hareket üreticisi, küçük hibrit RL, sınırlı residual, Dynamic NMPC, independent deadline guardian ve XAI bileşenleri devam eder.
4. Ana planlayıcı ağırlıkları değiştirilmez; küçük safety critic, selector, residual ve opsiyonel horizon-student eğitilebilir. Gerçek checkpoint revizyonları/hashes hâlâ `null`.
5. Çizimlerde **yalnız genel teknik modül adları** bulunur. Kodda ve akademik kaynaklarda LEAD, FPD-Drive, AutoE2E gibi özgün kaynaklar **saklanmaz**, fakat her kodun katkısı ve lisansı açıkça belirtilir.

## v1.1 → v1.2: Yeni kararların tam listesi

| Karar kimliği | Yenilik | Neden ekledik? | Kod/bağlantı | Sahiplik ve onay |
|---|---|---|---|---|
| D12-01 | **M10 Learned Safety & Performance Critic** | El yapımı TTC/çarpışma/ilerleme özellikleri tek başına yanlış sıralama üretebilir. | SafetyScores → PolicyObservation; M10→M11 | Küçük trainable model; ilk aşamada fiziksel özelliklerle, sonraki ablation'da grounded CoT/görünürlük/MPC eklenir. |
| D12-02 | **Çok başlıklı risk/performans tahminleri** | NC, DAC, TTC, DDC, EP, comfort, MPC feasibility ayrı öğrenme hedefleri gerektirir. | `candidate_scores` alanları; her biri farklı çıktı türünde | M10; ölçülmemiş başlıklara kalibre olasılık denemez. |
| D12-03 | **Risk yanlış-sıralama düzeltmesi + kalibrasyon** | Güvensiz adayı yüksek puanlama ve güvenli adayı düşük puanlama vakalarına odaklanmak. | Pairwise/group ranking, Brier/ECE, false-safe@risk | M10; gerçek risk etiketi yalnız eğitimde, inference'da sızıntı yasak. |
| D12-04 | **Çoklu geçerli hedef (multi-target)** | Tek insan/uzman hareketi, diğer geçerli manevraları gereksiz cezalandırabilir. | `TeacherTargetSet`, valid/mode masks | M21 offline; tek log geleceği diğer eylemlerin gerçek sonucu sayılmaz. |
| D12-05 | **Gelecek bilgili öğretmen** | Eğitimde karşı-olgusal adayları daha iyi denetlemek. | teacher labels → offline cache; politika girdi allowlist dışında | M00+M21; gerçek geleceğin çevrim içi kullanımı yasak. |
| D12-06 | **Görünürlük/örtülme farkındalıklı etiketleme** | Mevcut olmayan nesne ile sensörün görmediği nesneyi ayırmak. | `VisibilityEvidence`/`UNKNOWN`; bağımsız geometry + camera availability | M02, M06, M21; CARLA privileged IDs sadece offline etiket üretiminde. |
| D12-07 | **Güçlü expert ve kural tabanlı baseline** | Klasik ajanların yüksek başarı ve ayrıcalıklı bilgi avantajını dürüstçe ölçmek. | Native expert, same-evidence rule+NMPC iki ayrı kol | M20; privileged vs sensor-compatible kesin ayrılır. |
| D12-08 | **Sürüm kontrollü veri/özellik cache'i** | Farklı rig/preprocess/teacher checkpoint'iyle eski cache'in yanlış kullanımı önlenir. | sensor/preprocess/model/split/config fingerprints | M17/M21; hash uyuşmazlığında fail-closed. |
| D12-09 | **Strong planner baseline ve challenger** | Üst seviye aday üretim/scoring metoduna karşı değerlendirme, ancak gereksiz 3. online büyük model yok. | Native inference baseline; optional oracle study | M20; advanced planner weights ayrı, VRAM ve lisans denetimi gerekli. |
| D12-10 | **Diffusion-bridge karşılaştırma opsiyonu** | Gerçek yeni aday çeşitliliği var mı? | Offline challenger/ablation | M08/M20; temel çift planlayıcının yerini otomatik almaz. |
| D12-11 | **E19–E24 yeni deney serisi** | Yeni kritik, çoklu hedef, visibility, expert, oracle ve model/compute kıyaslarını ayrıştırmak. | `coverage.json`, `experiments.md` | RQ1–RQ9 korunur, ek alt sorular v1.2. |
| D12-12 | **Türkçe+İngilizce temiz şemalar** | Karışık iki dilli figürler ve gereksiz marka adları tez için uygun değil. | `assets/diagrams/v1_2/` DOT/SVG/PNG/PDF | İki dil ayrı ve editlenebilir. |
| D12-13 | **v1.1 sonrası konuşma kararlarını arşivleme** | Araştırma kararlarının tarihsel bağı kopmasın. | `history/` | Birebir görünen kullanıcı metinleri + işaretlenmiş asistan özetleri; tam platform transkripti iddiası yok. |
| D12-14 | **Benchmark kaynak/tahmin ayrımı** | KITScenes ADE/FDE, NAVSIM PDMS ve CARLA SR/DS aynı ölçü değil; hedefler ölçüm gibi gösterilmemeli. | `docs/benchmark-matrix-v1.2.md` | Aynı protokol/revision/sensor/split ile yeniden çalıştırılmalı. |
| D12-15 | **Logo/marka kilidi** | Önceki görsel tasarımlarda logo yanlış değişti. | brand reference + preservation manifest | Yeni ikon yaratılmayacak; kullanıcı onaylı görsel aynen tutulacak. |

## Tamamlanmamış kritik çalışmalar

- Hazır inference kodunun varlığı **yerel adapter'ın çalıştığı anlamına gelmez**. Özellikle FPD'nin kaydedilmiş scoring head ağırlıklarının farklı planner latentlerine doğrudan uygulanması mümkün değildir; yeniden eğitim/projeksiyon gerekir.
- LEAD `main` ve `cvpr2026` deneyleri ayrı veri ve checkpoint aileleri; birbirlerinin checkpoint'leriyle değiştirilemez.
- Strong baseline yayın skorları ile bizim ölçülmemiş mimarinin tahminleri aynı tabloda yalnız statü sütunuyla tutulur.
- P0–P3 çalışma profilleri ve 2× RTX A5000 performansı henüz ölçülmedi.
- 20 Hz NMPC/guardian 50 ms hedefi sert gerçek zamanlı veya güvenlik sertifikası değildir.
- Erken güvenlik etkisi ile dönemlik CVaR ayrılmalı; critic ile RL value-function aynı ağ/etiket sayılmamalıdır.

## İlgili belgeler

- [Detaylı yeni mimari ve nedenleri](architecture-v1.2-extended.md)
- [Safety Critic yöntemi](safety-critic-and-supervision.md)
- [Çevrim dışı veri, uzman, görünürlük, çok hedef](training-and-data-v1.2.md)
- [Benchmark ve model matrisi](benchmark-matrix-v1.2.md)
- [Kaynak kod / lisans / yeniden kullanım](reuse-register-v1.2.md)
- [Arayüz uzantıları](interfaces-v1.2-addendum.md)
- [Düşük seviye validasyon planı](verification-v1.2.md)
- [Yeni konuşma tarihçesi](../history/README.md)
