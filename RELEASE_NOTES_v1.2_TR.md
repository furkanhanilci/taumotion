> Tarihsel sürüm kaydı. Güncel yayın v1.3.1; [güncel belge denetimi](reports/documentation_checks.json). Arşiv/konuşma kopyaları yerel teslimde korunur, Git yayınına dahil değildir.

# τMOTION v1.2 — Teslimat ve değişiklik özeti

**11 Kasım 2026.** Bu paket önceki `taumotion.zip` / Architecture Specification v1.1 üzerinde oluşturulmuş, **yeni v1.2 tasarım arşividir**. Önceki v1.1 ve v1.0 paketlerinin byte-byte kopyaları `archive/` içinde korunur. Kaynak kodu/uygulama veya çalıştırılmış otonom araç yazılımı içerdiği iddiasında bulunmaz.

## Genişletilmiş mimari

1. **M10 SafetyPerformanceCritic** — NC/DAC/TTC/DDC/EP/comfort/MPC feasibility için farklı başlıklar, risk yanlış sıralama, ranking ve kalibrasyon. Fiziksel risk özellikleri korunur; yeni critic'in eğitimi henüz yapılmadı.
2. **Görünürlük/örtülme ve learner–expert asymmetry** — gerçek CARLA actor-truth ile sensörlerin görebildiği nesneler eğitimde ayrılır; teacher-only veriler politika girdisine geçmez (M02/M06/M21).
3. **Offline multi-target trajectory supervision** — tek uzman yörüngesi tek doğru sayılmaz; counterfactual etiket gerekirse rollout ile doğrulanır. Teacher'ın future knowledge bilgisi çevrim içi kullanılmaz (M21).
4. **Güçlü ekspert ve kural tabanlı baseline** — privileged expert ile aynı-girdi rule-based+NMPC ayrı kıyaslanır; dış kaynak native inference bağımsız baseline olarak tutulur, üçüncü büyük model zorunlu çevrim içi bileşen olmaz (M20).
5. **Kanıt koşullu risk duyarlı RL** — critic ile PPO value/CVaR cost ayrı ağ ve görevler; Candidate Attention+GRU, 8D Δv/Δd residual, M13 supervisor, 20Hz hedef Dynamic NMPC ve M22 deadline guardian korunur.
6. **Kaynak kayıtları** — FPD-Drive/LEAD/BridgeDrive gerçek GitHub revision pinleri ve lisans notları eklendi. Genel bilimsel figürlere bu proje adları yazılmadı, kaynak dokümanlarında açıkça atıf yapıldı.
7. **Benchmark matrisi** — AutoE2E KITScenes canonical vs old GT, NAVSIM v1 PDMS / v2 EPDMS, Bench2Drive DS/SR ve önceki model sonuçları; *published*, *target* ve *not-run* ayrımları.
8. **Deney planı** — E19–E24: critic, multi-target, occlusion, strong challenger, PPO+CVaR, cross-domain/compute. RQ1–RQ9 ve eski E1–E18 korunur.
9. **Vektörel şemalar** — `assets/diagrams/v1_2/`: online, offline, kontrol ve full M00–M23 modül haritası; TR/EN ayrı, DOT/SVG/PNG/PDF.
10. **Logo kilidi** — onaylanan eski mor τMOTION referans görseli aynen saklandı. Eski turkuaz deneysel SVG değiştirilmedi ama artık tercih edilen logo diye işaretlenmiyor.
11. **Konuşma geçmişi eki** — v1.1 sonrası 15 görünür kullanıcı mesajı birebir, asistan kararları özet olarak ve açık bütünlük sınırıyla kaydedildi.
12. **Belge doğrulaması ve CI** — v1.1'de eksik bulunan `reports/documentation_checks.json` üretildi, iç bağlantılar ve kaynaklar denetlendi. GitHub Actions dokümantasyon kontrolü eklendi.

## İnceleme için önerilen dosya sırası

`README.tr.md` → `docs/revisions-v1.2.md` → `docs/architecture-v1.2-extended.md` → `docs/safety-critic-and-supervision.md` → `docs/training-and-data-v1.2.md` → `docs/interfaces-v1.2-addendum.md` → `docs/experiments-v1.2-addendum.md` → `docs/benchmark-matrix-v1.2.md` → `docs/reuse-register-v1.2.md` → `history/README.md` → `reports/TAUMOTION_Architecture_Specification_v1.2.pdf`.

**D0 doküman kontrolleri gerçek sürüş performansı değildir.** Native inference, adapter parity, GPU co-load, critic kalibrasyonu, CARLA closed-loop ve 20Hz zaman bütçesi için testlerin tümü `NOT_RUN` durumundadır.
