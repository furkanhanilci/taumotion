# Araştırma bulguları, kaynak seçimi ve yeniden kullanım haritası
İnceleme tarihi 11 Kasım 2026. Birincil kaynaklar: proje kodu, resmi dokümantasyon, model kartı ve araştırma makaleleri. Bu çalışma kaynak kod okuyarak yapılmıştır; depolar bu teslimde kurulup çalıştırılmadı. “Kaynakta var” ile “bizim rig üzerinde doğrulandı” ayrı statülerdir.

## 1. Planlayıcı A: flow ve VLM parçaları
Qwen-Drive veri belgesi üç kameranın dört geçmiş anını, ego geçmişini ve beş saniyelik yerel yörüngeyi tanımlar. Planlama ve ayrı perception yolunun görüntü sözleşmeleri aynı değildir. Bu nedenle planlayıcıyı ve bütün algı başlıklarını aynı görüntü/tensor ile çalıştırılabilir kabul etmiyoruz. Hazır inference, preprocessing, plan expert ve checkpoint tekrar kullanılacak; yeni kod seed, çıktı ve zaman sözleşmesidir. [Veri sözleşmesi](https://github.com/QwenLM/Qwen-Drive-1.0/blob/28091c1532e869bc7aee91fc0aef6b3e6fd0b2e0/docs/data.md), [model](https://github.com/QwenLM/Qwen-Drive-1.0/blob/28091c1532e869bc7aee91fc0aef6b3e6fd0b2e0/docs/model.md), [perception](https://github.com/QwenLM/Qwen-Drive-1.0/blob/28091c1532e869bc7aee91fc0aef6b3e6fd0b2e0/docs/perception.md), [makale](https://arxiv.org/abs/2609.00111)

## 2. Planlayıcı B: hazır diffusion, online özellik köprüsü
İncelenen ReCogDrive agent/config yolu dört saniye ve 0.5 saniyelik aralık kullanır. Feature builder'da cache_hidden_state/cache_mode kombinasyonu backbone oluşturma ve tüketme dallarıyla birlikte değerlendirilmelidir; varsayılan bayrakları kopyalayıp çevrimiçi çalışacağını varsaymak yeterli değildir. Görüntü yolu ve explicit CUDA kullanımı da canlı worker adaptörü gerektirir. Bunlar checkpoint'i yeniden eğitme gerekçesi değildir. [Agent](https://github.com/xiaomi-research/recogdrive/blob/5831ee83c7a6a40bf6919715b96b0e9ba2b48335/navsim/agents/recogdrive/recogdrive_agent.py), [features](https://github.com/xiaomi-research/recogdrive/blob/5831ee83c7a6a40bf6919715b96b0e9ba2b48335/navsim/agents/recogdrive/recogdrive_features.py), [diffusion](https://github.com/xiaomi-research/recogdrive/blob/5831ee83c7a6a40bf6919715b96b0e9ba2b48335/navsim/agents/recogdrive/recogdrive_diffusion_planner.py), [config](https://github.com/xiaomi-research/recogdrive/blob/5831ee83c7a6a40bf6919715b96b0e9ba2b48335/navsim/planning/script/config/common/agent/recogdrive_agent.yaml)

## 3. AutoE2E: parçaları almak ve baseline'ı korumak
Taksonomi, beş ufuklu head, reasoning coupling ve faithfulness yardımcıları doğrudan yeniden kullanım adaylarıdır. Head belirli girdi boyutlarını bekler; τMOTION özelliklerine projeksiyon gerekir. Faithfulness yordamı da kendi model API'sine bağlıdır; müdahale mantığı alınır, bizim policy/state API'sine uyarlanır. Modelin bütünü N9 baseline olarak kalır. Böylece hem alt parçalar değerlendirilir hem hazır uygulamayla tam sistem karşılaştırması korunur. [Taksonomi](https://github.com/autowarefoundation/auto_e2e/blob/bc7e27cdfaa961cbc6aabab8c75ea0304479e795/Model/model_components/reasoning/reasoning_taxonomy.py), [horizon head](https://github.com/autowarefoundation/auto_e2e/blob/bc7e27cdfaa961cbc6aabab8c75ea0304479e795/Model/model_components/reasoning/horizon_reasoning_head.py), [coupling](https://github.com/autowarefoundation/auto_e2e/blob/bc7e27cdfaa961cbc6aabab8c75ea0304479e795/Model/model_components/trajectory_planning/reasoning_coupling.py), [faithfulness](https://github.com/autowarefoundation/auto_e2e/blob/bc7e27cdfaa961cbc6aabab8c75ea0304479e795/Model/evaluation/faithfulness.py), [model giriş noktası](https://github.com/autowarefoundation/auto_e2e/blob/bc7e27cdfaa961cbc6aabab8c75ea0304479e795/Model/README.md)

## 4. Bağımsız kanıt: doğru Zoo dalı ve küçük dışa aktarım yaması
Bench2DriveZoo'da uniad/vad-0.0.4 dalı, 0.0.4 benchmark uyumu için seçildi; varsayılan dalın eski commit'i kaynak kilidi yapılmadı. UniAD detector bazı ara tensorleri sonuç döndürmeden temizler. Kanıt adaptörü bunları temizleme öncesinde kontrollü dışa aktarır. Native ajan yol çıktısını PID'ye verir; bizim bağlama noktası bu kontrol aşamasından öncedir. Tiny checkpoint, gerçek tiny config şekilleriyle strict-load sınanacaktır; README bağlantı başlığı tek doğrulama kaynağı değildir. [Uyumlu dal](https://github.com/Thinklab-SJTU/Bench2DriveZoo/tree/d9caa0af805ec3c435533aa268e2723d80c20017), [detector](https://github.com/Thinklab-SJTU/Bench2DriveZoo/blob/d9caa0af805ec3c435533aa268e2723d80c20017/mmcv/models/detectors/uniad_e2e.py), [ajan](https://github.com/Thinklab-SJTU/Bench2DriveZoo/blob/d9caa0af805ec3c435533aa268e2723d80c20017/team_code/uniad_b2d_agent.py), [tiny config](https://github.com/Thinklab-SJTU/Bench2DriveZoo/blob/d9caa0af805ec3c435533aa268e2723d80c20017/adzoo/uniad/configs/stage2_e2e/tiny_e2e_b2d.py), [weights deposu](https://huggingface.co/rethinklab/Bench2DriveZoo)

Orijinal UniAD'nin gerçek veri sürümü ve Zoo'nun CARLA sürümü farklı backend'lerdir. Sensör/alan uyumu kanıtlanmadan NAVSIM'e sıfır uyarlama iddiası yapılmaz. [Orijinal UniAD](https://github.com/OpenDriveLab/UniAD)

## 5. Trafik ışığı için hazır alt uygulama
Autoware traffic_light_classifier, ROI üzerinden HSV veya CNN sınıflandırma yolları sunar. Tasarımda ilk hazır referans HSV; CNN yolu ayrıca kıyaslanır. Kaynak kodun bulunması her alana uygun pretrained ağırlığın doğrulandığı anlamına gelmez. ROI detection, renk sınıflandırma ve ilgili şerit ilişkisi ayrı entegrasyon işleridir. [Paket belgesi](https://github.com/autowarefoundation/autoware_universe/blob/5f8fccaaf85d7aed68c723a7d6b566dff6d49c99/perception/autoware_traffic_light_classifier/README.md)

## 6. RL ve kontrol altyapısı
TorchRL/PyTorch dağılım, rollout ve PPO hesaplarını sağlar. SafePO maliyet/Lagrange altyapısı için kaynak; CVaR terminal maliyeti ve quantile güncellemesi özel küçük araştırma kodudur. acados OCP örneği model/çözücü kurulumunu sağlar; CARLA araç tanılama ve actuator bridge bize aittir. [TorchRL](https://github.com/pytorch/rl), [SafePO](https://github.com/PKU-Alignment/Safe-Policy-Optimization), [acados örneği](https://github.com/acados/acados/blob/7d43f571d8ea7488821bfa78b6110eba575d005e/examples/acados_python/race_cars/acados_settings.py)

Alternatif SB3/SB3-Contrib, ayrık MaskablePPO baseline'ı için tutuldu. Ana hibrit recurrent policy'yi ayrı hazır algoritmaları kontrolsüz birleştirerek kurmuyoruz. [SB3-Contrib](https://github.com/Stable-Baselines-Team/stable-baselines3-contrib)

## 7. Benchmark, modeller ve ek araştırma
NAVSIM v1.1 ve v2.1.2 ayrı kaynak commitleriyle sabitlendi. v2.1.2 release'inin EPDMS değişiklikleri nedeniyle genel “NAVSIM v2” etiketi tek başına yeterli değildir. Bench2Drive 0.0.4 ve Robust farklı deney profilleridir. Robust'un gecikme/bozulma senaryoları tekrar kullanılabilir. [NAVSIM releases](https://github.com/autonomousvision/navsim/releases), [metrikler](https://github.com/autonomousvision/navsim/blob/937cefc1b116f930990abea1c54185308a96029f/docs/metrics.md), [B2D 0.0.4 değişiklikleri](https://github.com/Thinklab-SJTU/Bench2Drive/blob/7ec25d1c9f7522d923ce5f3420986cef1cb2d956/docs/v004_update.md), [Robust](https://github.com/Thinklab-SJTU/Bench2Drive-Robust/blob/ae1b5867324710bf0574cba797062280d9d97105/README.md)

Qwen3.8-27B model kartı doğrulandı; sürüş görevinde Qwen3.5'ten üstün olduğuna dair sonuç bu incelemeden çıkmaz. Sürüm kıyası E11'dir. SimLingo güçlü bir hazır dil/sürüş baseline adayıdır; KITScenes ve AlpaSim ayrı veri/simülasyon yolları olarak korunur. [Qwen3.8 model kartı](https://huggingface.co/Qwen/Qwen3.8-27B), [SimLingo makalesi](https://arxiv.org/abs/2503.09594), [SimLingo kodu](https://github.com/RenzKa/simlingo), [KITScenes](https://github.com/KIT-MRT/kitscenes), [AlpaSim](https://github.com/NVlabs/alpasim)

Reasoning-action coupling ve karşıolgusal CoT çalışmaları, açıklamanın akıcı olmasının karar üzerinde doğru etkisini kanıtlamadığını araştırmak için ilgili kaynaklardır. Buradaki tasarım çıkarımı, τMOTION'da metin yolu ve ortam müdahalesini ayrı deney yapmaktır; bu kaynakların sonucu bizim sistemde ölçülmüş sonuç değildir. [Reasoning-action coupling](https://arxiv.org/abs/2610.30953), [C-CoT](https://arxiv.org/abs/2605.10744)

## 8. Kaynak sürümleri
Aşağıdaki commitler inceleme sırasında çözülmüştür. Kaynak seçimi tamamdır; runtime uyumluluğu G0/G1'de doğrulanacaktır. Lisans metni, ağırlık lisansı, veri koşulları ve indirme revision/hash alanları ayrı kaydedilmelidir. Bu paket üçüncü taraf kodunu veya ağırlıklarını yeniden dağıtmaz.

| Kaynak | Commit / sürüm | Kullanım |
|---|---|---|
| QwenLM/Qwen-Drive-1.0 | [28091c1532e8](https://github.com/QwenLM/Qwen-Drive-1.0/tree/28091c1532e869bc7aee91fc0aef6b3e6fd0b2e0) | Kaynak incelemesi; çalıştırma bekliyor |
| xiaomi-research/recogdrive | [5831ee83c7a6](https://github.com/xiaomi-research/recogdrive/tree/5831ee83c7a6a40bf6919715b96b0e9ba2b48335) | Kaynak incelemesi; çalıştırma bekliyor |
| autowarefoundation/auto_e2e | [bc7e27cdfaa9](https://github.com/autowarefoundation/auto_e2e/tree/bc7e27cdfaa961cbc6aabab8c75ea0304479e795) | Kaynak incelemesi; çalıştırma bekliyor |
| autonomousvision/navsim | [0a380a9063d7](https://github.com/autonomousvision/navsim/tree/0a380a9063d7162ec93d0f51e9990ebac585f720) | İncelenen main; deney için aşağıdaki release'ler |
| Thinklab-SJTU/Bench2Drive | [7ec25d1c9f75](https://github.com/Thinklab-SJTU/Bench2Drive/tree/7ec25d1c9f7522d923ce5f3420986cef1cb2d956) | Kaynak incelemesi; çalıştırma bekliyor |
| Thinklab-SJTU/Bench2Drive-Robust | [ae1b58673247](https://github.com/Thinklab-SJTU/Bench2Drive-Robust/tree/ae1b5867324710bf0574cba797062280d9d97105) | Kaynak incelemesi; çalıştırma bekliyor |
| OpenDriveLab/UniAD | [609ee083ea51](https://github.com/OpenDriveLab/UniAD/tree/609ee083ea51c3521c323f1279dfc4cee0e60467) | Kaynak incelemesi; çalıştırma bekliyor |
| acados/acados | [7d43f571d8ea](https://github.com/acados/acados/tree/7d43f571d8ea7488821bfa78b6110eba575d005e) | Kaynak incelemesi; çalıştırma bekliyor |
| Thinklab-SJTU/Bench2DriveZoo | [d9caa0af805e](https://github.com/Thinklab-SJTU/Bench2DriveZoo/tree/d9caa0af805ec3c435533aa268e2723d80c20017) | Kaynak incelemesi; çalıştırma bekliyor |
| RenzKa/simlingo | [743b243afd6c](https://github.com/RenzKa/simlingo/tree/743b243afd6cf5ff51b9fa1f8cac86f22d569684) | Kaynak incelemesi; çalıştırma bekliyor |
| autowarefoundation/autoware_universe | [5f8fccaaf85d](https://github.com/autowarefoundation/autoware_universe/tree/5f8fccaaf85d7aed68c723a7d6b566dff6d49c99) | Kaynak incelemesi; çalıştırma bekliyor |
| pytorch/rl | [a711ef99d29f](https://github.com/pytorch/rl/tree/a711ef99d29f31ce6bc49ce5da499ddd87b4b1f8) | Kaynak incelemesi; çalıştırma bekliyor |
| pytorch/tensordict | [4a877a258392](https://github.com/pytorch/tensordict/tree/4a877a258392dcf12aa45ebbe3819070c7daa83e) | Kaynak incelemesi; çalıştırma bekliyor |
| PKU-Alignment/Safe-Policy-Optimization | [8d0fa763b5e9](https://github.com/PKU-Alignment/Safe-Policy-Optimization/tree/8d0fa763b5e9091db8bed502b7efe76f81b1d263) | Kaynak incelemesi; çalıştırma bekliyor |
| DLR-RM/stable-baselines3 | [0cdcd200deef](https://github.com/DLR-RM/stable-baselines3/tree/0cdcd200deef06b9ad0af72f6ddfb07c06c6df39) | Kaynak incelemesi; çalıştırma bekliyor |
| Stable-Baselines-Team/stable-baselines3-contrib | [a8af63682070](https://github.com/Stable-Baselines-Team/stable-baselines3-contrib/tree/a8af63682070df0bda9707400b2e971055600910) | Kaynak incelemesi; çalıştırma bekliyor |
| KIT-MRT/kitscenes | [7765cdec5490](https://github.com/KIT-MRT/kitscenes/tree/7765cdec5490894266070ab46e23724b58b3da42) | Kaynak incelemesi; çalıştırma bekliyor |
| NVlabs/alpasim | [affc2eab209f](https://github.com/NVlabs/alpasim/tree/affc2eab209fa43bdfa2f26c0f8d437922d78a68) | Kaynak incelemesi; çalıştırma bekliyor |
| autonomousvision/navsim | [3e8291bfa89f / v1.1](https://github.com/autonomousvision/navsim/tree/3e8291bfa89ff247231e0227778840cd0a036896) | Kaynak incelemesi; çalıştırma bekliyor |
| autonomousvision/navsim | [937cefc1b116 / v2.1.2](https://github.com/autonomousvision/navsim/tree/937cefc1b116f930990abea1c54185308a96029f) | Kaynak incelemesi; çalıştırma bekliyor |

## 9. Kaynak durumlarının doğru okunması
Doğrulandı: dosyanın/sürümün varlığı, incelenen API ve kod davranışı. Önerildi: bu parçaların τMOTION sözleşmesiyle birleştirilmesi, başlangıç hyperparametreleri, worker yerleşimi. Ölçülecek: closed-loop kazanç, bütün modellerin GPU'ya yerleşmesi, gerçek latency, algı doğruluğu, CVaR iyileşmesi ve insan çalışması.

Kaynakların bir arada listelenmesi onların aynı ortamda kurulduğu veya aynı checkpoint lisansını taşıdığı anlamına gelmez. Kaynak kod/weight hash kilidi ancak indirilen gerçek dosyalar üzerinden tamamlanır.
## 10. Ek hazır parçalar ve somut model depoları
Semantik başlangıç ve A planlayıcısı [Qwen-Drive-1.0-4B](https://huggingface.co/Qwen/Qwen-Drive-1.0-4B) ailesinden seçildi. planner-rl reasoning kipinde; planner-sft desteklediği direct/reasoning kıyasında kullanılacak. B için [ReCogDrive-VLM-2B](https://huggingface.co/owl10/ReCogDrive-VLM-2B) ile [ReCogDrive-2B-RL](https://huggingface.co/owl10/ReCogDrive-2B-RL) seçildi. Model sayfalarının varlığı doğrulandı; indirme ve ağırlık eşdeğerliği henüz yapılmadı.

AutoE2E'nin [teacher_client](https://github.com/autowarefoundation/auto_e2e/blob/bc7e27cdfaa961cbc6aabab8c75ea0304479e795/Model/data_processing/reasoning_label_generation/teacher_client.py) API'si eğitim etiket hattıdır; geleceği içerebilen istemleri online yola sokmamak gerekir. [control_rollout](https://github.com/autowarefoundation/auto_e2e/blob/bc7e27cdfaa961cbc6aabab8c75ea0304479e795/Model/training/losses/control_rollout.py) ivme/eğrilik çıktısının native integrasyonunu sağlar. [speed_benchmark](https://github.com/autowarefoundation/auto_e2e/blob/bc7e27cdfaa961cbc6aabab8c75ea0304479e795/Model/speed_benchmark/README.md) ölçüm iskeleti yeniden kullanılır.

[AlpaSim sürücü eklentisi](https://github.com/autowarefoundation/auto_e2e/blob/bc7e27cdfaa961cbc6aabab8c75ea0304479e795/Model/plugins/alpasim_driver/README.md) parser, kalibrasyon profilleri ve yörünge geri verme hattı sunar. Yerel AutoE2E modelini çalıştıran bu köprü, E15'in temelidir; τMOTION servislerine yönlendirme gerekir. Kaynak, sahnenin istenen kameraları render edebilmesini şart koşar. Bu nedenle hazır plugin, her veri kümesi için hazır rekonstrüksiyon bulunduğu anlamına gelmez.

## 11. Seçilmeyen alternatiflere göre gerekçe
| Karar | Alternatif | Seçim nedeni ve bedeli |
|---|---|---|
| Hazır UniAD kanıt hattı | Yeni BEV ağı; yalnız Qwen perception | Track/map/motion parçaları hazır; farklı ağırlık kaynağı. Bedel: eski bağımlılıklar ve alan uyarlaması |
| Yapılandırılmış ufuklu semantik | Yalnız uzun serbest metin | Müdahale/kalibrasyon ve küçük policy girdisi mümkün. Bedel: parser ve etiket kaybı |
| Küçük PPO seçici/residual | Büyük üreticilere DiffGRPO; DQN; SAC | Hazır üreticileri korur; hibrit eylemi küçük ağda öğrenir. Bedel: on-policy veri maliyeti |
| TorchRL altyapısı | MaskablePPO + RecurrentPPO'yu doğrudan birleştirme | Hibrit koşullu dağılımı açık tanımlamaya uygun. Bedel: özel dağılım/state köprüsü |
| CVaR kısıtı | Yalnız sabit risk cezası | Kötü episode kuyruğunu açık hedefler. Bedel: tail örnek ihtiyacı ve ek güncelleme |
| acados dinamik NMPC | Yeni optimizasyon çözücüsü; ana PID/Stanley | Hazır çözüm altyapısı ve fiziksel sınırlar. Bedel: model/aktüatör tanılama |
| Ortak 4 s kıyas | B'yi yapay olarak 5 s'ye uzatma | Doğal ortak kapsama ve dürüst skor. A'nın 5 s çıktısı ayrıca saklanır |
| Asenkron süreçler | Tek dev Python ortamı | Kaynakların farklı bağımlılıklarını korur. Bedel: IPC ve zaman sözleşmesi |

## v1.2 addendum — current specification supersedes applicable v1.1 text

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.

As of 11 Nov 2026 the **current v1.2 decisions** are specified in [revisions-v1.2.md](revisions-v1.2.md), [extended architecture](architecture-v1.2-extended.md), [critic](safety-critic-and-supervision.md), [offline training](training-and-data-v1.2.md), [interfaces](interfaces-v1.2-addendum.md), [benchmark matrix](benchmark-matrix-v1.2.md), [reuse](reuse-register-v1.2.md) and [verification](verification-v1.2.md). New M10 learner and M21 offline expert labels are subcomponents, **not new online foundation-model dependencies**. Previous v1.1 text remains for historical traceability; this addendum is authoritative for changed fields.
