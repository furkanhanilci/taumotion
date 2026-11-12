# τMOTION — Nihai Hibrit Uçtan Uca Sürüş Mimarisi

**Architecture Specification v1.3.1 · 12 Kasım 2026 · 24 modül · kapsam korunmuştur**

<p align="center"><img src="assets/brand/TAUMOTION_APPROVED_FINAL_LOGO_2026-11-12.png" alt="Onaylı τ + LiDAR’sız araç logosu" width="760"></p>

τMOTION, hazır güçlü algı, görsel-dil ve hareket üretim uygulamalarını açık veri sözleşmeleriyle birleştirir. İki büyük hareket üreticisi dondurulur; küçük güvenlik eleştirmeni, kanıt koşullu seçici, sınırlı residual ve zamansal öğrenci öğrenilir. Fiziksel ana kontrolcü Dynamic NMPC'dir.

Bu sürüm, sağladığın v1.3 klasörünün ayrıntılı incelemesinden sonra hazırlanmıştır. Son onaylı logo değişmedi. Mimari tanımlama teslimi tamamlanabilir; gerçek model inference, eğitim, CARLA sürüş ve iki A5000 üzerinde gerçek zaman başarısı henüz ölçülmüş değildir.

![Güncel bilimsel mimari](assets/diagrams/v1_3_1/main_architecture.svg)

[Tam boy SVG](assets/diagrams/v1_3_1/main_architecture.svg) · [Vektör PDF](assets/diagrams/v1_3_1/main_architecture.pdf) · [Zamanlama şeması](assets/diagrams/v1_3_1/runtime_contract.svg) · [Eğitim şeması](assets/diagrams/v1_3_1/learning_and_evidence.svg) · [54 bağımlılığın tam grafiği](docs/dependency-graph.md)

## Okuma yolu

1. [Ayrıntılı inceleme ve yapılan düzeltmeler](docs/prepublication-review-v1.3.1.md).
2. [Türkçe tam ana mimari](docs/FINAL_ARCHITECTURE_MASTER_TR.md) ve [İngilizce eşlikçi](docs/FINAL_ARCHITECTURE_MASTER_EN.md).
3. [24 bileşenin gerekliliği, hazır kaynağı, köprüsü ve eğitimi](docs/components.md).
4. [Kesinleştirilen entegrasyon sözleşmesi](docs/integration-contract-v1.3.1.md), [arayüzler](docs/interfaces.md), [critic](docs/safety-critic-and-supervision.md), [offline veri](docs/training-and-data-v1.2.md).
5. [Bütün deneyler](docs/experiments.md), [E19–E24](docs/experiments-v1.2-addendum.md), [kaynak incelemesi](docs/source-audit-v1.3.1.md), [hazır parça haritası](docs/reuse-register-v1.2.md).
6. [Güncel teknik PDF](reports/TAUMOTION_Architecture_Specification_v1_3_1.pdf), [belge kontrol raporu](reports/documentation_checks.json), [çalışma zamanı durumları](specs/validation_registry.json).

## Neler düzeltildi?

M10'un öğrenilmiş critic eklemesi ana modül alanlarına taşındı; offline teacher/cache bağlantılarının kapsam etiketleri düzeltildi. 54 kayıt/52 farklı modül çifti ayrımı açıklandı. Asenkron gecikmeyle kısalan plan ufku için ortak geçerli süre, maske ve fallback sözleşmesi eklendi. LEAD benchmark satırındaki expert nitelemesi düzeltildi; LEAD/BridgeDrive sürüm ayrımı kesinleştirildi. PDF satır kesme sorunu giderildi; güncel CI tanımı şablon olarak hazırlandı. Eski marka varlıkları tarihçe olarak işaretlendi.

RQ1–RQ11, E1–E24 ve E10-H, N0–N9/C0–C10; VLM/CoT, bağımsız kanıt, iki frozen planner, çok başlıklı critic, görünürlük, multi-target, GRU/attention PPO/CVaR, 8D residual, NMPC, guardian, student, insan XAI, veri çeşitliliği ve keşifsel aktarım kapsamda kalır. Üçüncü online ağır planner zorunlu değildir.

## Sayısal beklentiler

İstediğin 92.5 PDMS / 53 EPDMS / 82 DS / %60 SR / 0.60m ADE / 1.55m FDE değerleri [senaryo tablosunda](docs/benchmark-expectations-v1.3.md) korunur. Bunlar öznel planlama varsayımlarıdır; ölçüm, kalibre tahmin veya güven aralığı değildir. Yayımlanmış kaynak skorları kendi protokolleriyle ayrı tutulur.

## Yeniden üretim ve yayın

Kurulum ve belge üretme komutları [ayrıntılı İngilizce README](README.md) içindedir. Güncel doğrulayıcı yalnız belge/spec/artifact bütünlüğünü sınar; model veya sürüş testi çalıştırmaz. Orijinal arşivler ve birebir sohbetler yerelde korunur; [Git yayın sınırı](docs/repository-publication.md) araştırma kapsamından yöntem çıkarmaz. [Onaylı logo ve hash](docs/brand-approved-v1.3.md).

**GitHub CI durumu:** Mevcut bağlantıda workflow yazma yetkisi yok. [CI şablonu](tools/ci/validate-docs.yml) etkin olmayan konumda tutulur; GitHub Actions çalışmış sayılmaz. Yerel ve temiz yayın kopyasındaki belge kontrolleri geçmiştir.
