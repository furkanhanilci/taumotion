# Karşılaştırma geçerliliği ve doğrulama seviyeleri
## 1. Sensör, model ve hesap etkisi
Model mimarisi, eğitim verisi, pretrained checkpoint ve sensör erişimi çoğu hazır model kıyasında birlikte değişir. Yalnız aynı scene_id kullanılması bu değişkenleri sabitlemez. Tabloya sensör sütunu koymak da nedensel ayrıştırma sağlamaz.

| comparison_class | Sabitlenenler | İzinli çıkarım | Sınır |
|---|---|---|---|
| NATIVE_SYSTEM | Aynı sahne/split ve raporlanmış native ayarlar | Hazır sistemlerin toplam kalitesi | Saf mimari etkisi çıkarılamaz |
| WITHIN_MODEL_SENSOR | Aynı checkpoint, desteklenen girdi müdahalesi | O modelin bilgi erişimine duyarlılığı | Maskelenmiş sensör dağılım dışı olabilir |
| FIXED_CANDIDATE_SELECTOR | Aynı aday/kanıt/cache, kapasite ve eğitim bütçesi | Seçici veya semantik kanal katkısı | Üreticinin iç reasoning katkısı değildir |
| MATCHED_K | Aynı toplam aday sayısı ve scene | Aday kaynağı/tamamlayıcılık | Aynı hesap maliyeti değildir |
| MATCHED_COMPUTE | Ölçülmüş aynı GPU-s/scene ve donanım koşulu | Bütçe başına sistem kalitesi | Aynı K veya aynı bilgi değildir |
| SHARED_CONTROLLER | Aynı M13/M14/M22 ve izinli algı | Kontrol farkını azaltan planlama kıyası | Girdi/öğrenme farkları sürebilir |

Bir girdi ablasyonu native API tarafından desteklenmiyorsa bu deney OOD perturbation olarak işaretlenir; eşdeğer eğitilmiş model gibi sunulmaz. Kamerayı siyaha çevirmek yeni bir “adil temel model” yaratmaz. Saf mimari etkisini destekleyen eşlenmiş eğitim/checkpoint yoksa sonuç bölümünde bu etki tanımlanamaz denir. Kapsam korunur; iddia sınırı dar ve doğru tutulur.

Her sonuç satırında effective_camera_ids, history_span, input_resolution, route/map privilege, native_horizon, common_horizon, K, sampler_steps, precision, GPU-s, wall_time, controller, shield, scheduler_profile ve comparison_class olmalıdır.

## 2. Karar etkisi ve supervisor etkisi
Ham aday, residual önerisi, M13 kabul referansı, M14 çözümü, M22 komut kararı ve M15 uygulaması ayrı loglanır. M22'nin deadline reddi ile M13'ün geometrik reddi ayrı reason_code taşır. Aynı güvenlik/gözetim hattı ana kontrollü baseline'larda kullanılır.

M22 komut üretmeyi sürdürse bile kapalı döngü güvenliği ayrıca ölçülür. Heartbeat canlılığı, engel bilgisinin güncelliğini veya komutun doğru olduğunu kanıtlamaz. Deadline miss sonucu fallback uygulanması “başarılı normal kontrol” sayılmaz.

## 3. Doğrulama seviyeleri
| Seviye | Anlam | Gerekli kanıt | Bugünkü durum |
|---|---|---|---|
| D0 SPECIFICATION | Belge/JSON/diagram/link ve kapsam tutarlılığı | documentation_checks.json | Paket kontrolünde değerlendirilir |
| S0 SOURCE_INSPECTED | Kaynak dosya/API/release incelendi | Commit ve kaynak URL | Seçilmiş kaynaklarda var |
| R1 NATIVE_INFERENCE | Gerçek checkpoint native örnek çalıştırıldı | Weight hash, ortam, input ve output | NOT_RUN |
| R2 ADAPTER_PARITY | Native ve adapter çıktıları eşdeğer | Golden input, tolerans ve farklar | NOT_RUN |
| R3 RUNTIME_INTEGRATION | Worker'lar ve guardian birlikte çalıştı | Zaman çizelgesi, crash/late testleri | NOT_RUN |
| R4 CLOSED_LOOP | Gerçek CARLA episode'ları değerlendirildi | Route/seed, metrics ve failure trace | NOT_RUN |
| R5 REAL_TIME_PROFILE | Belirli donanım ve profil deadline hedefini karşıladı | Co-load latency/AoI/miss/fallback sonuçları | NOT_RUN |

R5 geçti ifadesi bütün donanımlarda veya bütün senaryolarda hard-real-time garanti anlamına gelmez. Ölçülen zarf ve örnek sayısı belirtilir. Üst seviye statü yalnız kanıt yolları ve hash'leriyle değişebilir; doküman script'i runtime seviyelerini yükseltemez.

## 4. Kanıt kaydı
specs/validation_registry.json bileşen ve sistem seviyesinde statüyü saklar. reports/documentation_checks.json yalnız D0 kapsamına aittir; global system_verified alanı içermez. Eksik runtime sonucu sıfır hata veya PASS olarak yazılmaz. Örnek packet açık SYNTHETIC etiketi taşır.

Kaynak pinleri kurulmuş ortam kilidi değildir. Bir model deposunun varlığı ile indirilmiş ağırlığın doğrulanması farklıdır. Runtime kayıtları oluştuğunda gerçek revision, dosya SHA256, preprocessing sürümü, cihaz ve input hash bağlanır.

## 5. Değişiklik yönetimi
Bu sürüm, v1.0'daki zamanlama ve 50 ms varsayımlarını daha kesin sözleşmelerle değiştirir. Araştırma modülleri çıkarılmadı. Donanım hedefi karşılanmazsa önce profiler verisine göre yerleşim, frekans, precision veya aynı işlevi sağlayan hazır backend değerlendirilir; işlev sessizce silinmez. Native referans ile optimize profil ayrı sonuç tablosudur.

## v1.2 addendum — current specification supersedes applicable v1.1 text

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.
