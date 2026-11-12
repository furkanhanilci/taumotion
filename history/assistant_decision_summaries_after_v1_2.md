# v1.2 sonrası asistan karar özetleri — VERBATIM DEĞİL

Bu dosya, görünen asistan cevaplarının bilimsel/tasarımsal kararlarını **özetler**. Birebir tam platform transcript değildir; asistanın bütün uzun mesajlarını veya görüntü üretim payload'larını yeniden oluşturmaz.

| Görüşme | Sonuç / nihai karar | Modül/dosya etkisi |
|---|---|---|
| U16 | Klasik Autoware Universe ve AutoE2E benchmark/baseline ayrımı eklenecek; published vs estimate ayrılacak | M19/M20; `benchmark-expectations-v1.3.md` |
| U17 | τMOTION için tablolarda nokta performans beklentileri verilecek: NAVSIM v1 92.5, v2 53; B2D 82 DS/60% SR; KITScenes .60/.1.55 | M19; `specs/benchmark_expectations_v1_3.json` |
| U18 | AutoE2E'nin temporal BEV/GRU, 0–4s reasoning, zero-init coupling ve XAI faithfulness gibi güçlü yönlerinin adaptasyon durumu sorgulandı | M02/M04/M05/M11/M18/M20 |
| U19 | ZIP kontrolünde bu yöntemlerin **önceden** mimariye dahil olduğu doğrulandı; yeni model olarak ekleme önerisi geri çekildi. AutoE2E planner yalnız M20 baseline | Tasarım 24 modülle sabit |
| U20 | Kullanıcı şu anda mimarinin tanımlanmasını yeterli sayıyor; test ve runtime sonuçları tasarım için gerekli önkoşul değil | Doküman revizyon önceliği |
| U21 | Sistem kamera→komut uçtan uca zinciri kapsasa da frozen planner + ayrı RL + NMPC nedeniyle doğru adlandırma `Hybrid End-to-End Autonomous Driving Framework` | Tez adı, README, kapsam |
| U22–U23 | τ simgesi ve araç tasarımıyla yaratıcı fütüristik logo üretildi | Marka varlıkları |
| U24 | Araç üzerinde LiDAR/sensör maketi olmayacak; yalnız otomobil silüeti + τ. Yeni raster üretildi | Güncel görsel varlık |
| U25 | “tamam logo güzel” onayıyla son görsel tercih edildi; mevcut arşiv güncellenecek ve tamlık denetlenecek | v1.3 brand lock / master document / history |

**Kritik düzeltme:** Bazı önceki cevaplarda “AutoE2E bileşenlerini mimariye ekleyelim” gibi gelecek kipinin kullanılması yanıltıcıydı. Zaten M04/M05/M11/M18/M20/M16/M21 içinde tanımlanmış adaptasyonlar bu sürümde **yeniden eklenen bağımsız modüller** değildir. Mevcut mimari yalnız uygulama değil, kapsam tasarımı olarak tamamlanmıştır.
