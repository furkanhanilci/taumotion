# Architecture Specification v1.3.1

12 Kasım 2026. Kullanıcının sağladığı v1.3 klasörünün GitHub yayını öncesindeki inceleme revizyonu. Kaynak klasör ve onaylı logo dosyası değiştirilmedi; 24 modül ve bütün yöntem/deney kapsamı korundu.

Etkin M10 critic ve M21 teacher tanımları katalog/JSON/CSV'de birleştirildi. Offline veri yolları düzeltildi; asenkron kalan ufuk, per-head metric/calibration ve LEAD/BridgeDrive native environment sözleşmeleri kesinleştirildi. 54 bağımlılık kaydının 52 farklı yönlü modül çifti olduğu açıklandı. LEAD skorunun oracle-expert diye yanlış etiketlenmesi giderildi. Kullanıcının istediği sayısal benchmark senaryoları korunarak ölçümden ayrıldı.

Geniş README, üç güncel vektör figür, tüm bağımlılıkları içeren Mermaid, güncel 71 sayfalık PDF ve taşınabilir D0 doğrulayıcı eklendi. Önceki sekiz iki dilli figür ve bilimsel belgeler korunur. Orijinal ZIP ve birebir sohbetler yerel teslimdedir; Git bilimsel dokümanları ve karar özetlerini taşır.

[Ayrıntılı değerlendirme](docs/prepublication-review-v1.3.1.md) · [Entegrasyon sözleşmesi](docs/integration-contract-v1.3.1.md) · [Kaynak yeniden incelemesi](docs/source-audit-v1.3.1.md) · [Belge denetimi](reports/documentation_checks.json).

Native inference, model/adapter eşdeğerliği, critic eğitimi, CARLA sürüşü ve gerçek zaman başarısı **NOT_RUN** durumundadır. Bu sürüm araştırma mimarisi spesifikasyonudur.
