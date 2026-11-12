# Asistan yanıtlarından üretilmiş karar özeti — VERBATIM DEĞİL

**UYARI:** Aşağıdaki kayıtlar asistanın bütün cevaplarının birebir transkripti değildir; güncel bağlamdan ve paketlerden türetilmiş konu/karar özetleridir. Bu durum önceki transkript bütünlüğü ilkesini sürdürür.

## U01

v1.1 ZIP incelemesi yapıldı: 24 modül/44 kenar; güçlü M22 deadline ve M23 evidence propagation; D0 `documentation_checks.json` eksikliği ve runtime testlerinin henüz yapılmadığı not edildi.

## U02–U04

Mimarinin görsel yeniden tasarımında mor τ işareti ve MOTION marka kimliği kullanıcı tarafından beğenildi; önceki logo varyantları tercih edilmedi. v1.1 içerikle uyum hedeflendi.

## U05–U06

24 modüllü ana/çevrim dışı/gerçek-zamanlı akışlar, neden/nasıl/girdi/çıktı anlatımları, iki planner 5s vs 4s ve 4s/0.1s ortak traj, 20Hz NMPC, CoT/grounding/PPO/CVaR ile uzun teknik anlatım oluşturuldu.

## U07

NAVSIM, CARLA, KITScenes, klasik/privileged expert ve VLA/IL karşılaştırma çerçevesi kuruldu. Yayınlanmış sonuçlar ile τMOTION için henüz ölçülmemiş koşullu hedeflerin farklı olduğu özellikle belirtildi.

## U08

AutoE2E KITScenes örnek sayısı farklı sonuçları, canonical ground truth dönüşümü düzeltmesi, ADE/FDE ve model/sürüme bağlı gecikme testleri incelendi; basit kinematik baseline eklendi.

## U09

En güçlü modellerin önüne geçme sorusu için güçlü benchmarklar (FPD/LEAD), oracle candidate set üst sınırı ve RL/critic ile gerçekten elde edilebilecek kazanımın ayrılması önerildi.

## U10

FPD native inference/scorer/ranking/refiner ve LEAD expert/path/speed/occlusion/logging kodları incelendi; FPD eğitim teacher kodu yayımlanmamış, LEAD main/cvpr2026 checkpointleri uyumsuz. BridgeDrive optional challenger bulundu.

## U11–U13

Öğrenilmiş M10 Safety Critic, multi-target offline teacher ve visibility/occlusion labels ekleme kararı verildi. Bilimsel görsellerde external proje isimlerinin kullanılmaması, TR/EN şemaların ayrılması, mor kullanıcı-onaylı τ işaretinin bozulmaması istendi.

## U14

Yeni sistemin akışı uzun teknik metin halinde açıklandı: M10 critic ile PPO Value ayrımı, 8D residual, teacher-only future, dynamic NMPC, independent guardian, AoI/async, XAI counterfactual ve benchmark ayrımları.

## U15

Yeni v1.2 folder update, kaynaklar/specs/methods/benchmark/figure/transcript addendum ve geçmişi kaybetmeyen sürümleme talep edildi; bu paket buna karşılık hazırlanmıştır.
