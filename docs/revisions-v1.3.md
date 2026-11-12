# τMOTION v1.3 — Final Documentation & Approved Brand Revision

**12 Kasım 2026.** v1.2 araştırma mimarisi korunur; bu sürüm **mimari kapsamın kapsamlı biçimde açıklanması, son kararların kaydı ve yeni onaylı logonun kilitlenmesi** içindir. Bileşen sayısı **24**, mimari edge sayısı **54**; yeni runtime foundation model ve yeni topoloji eklenmemiştir.

1. **Yeni bir ana kaynak:** `docs/FINAL_ARCHITECTURE_MASTER_TR.md` tüm çevrim içi/çevrim dışı zinciri, algoritmaları, girdi/çıktı sözleşmelerini, 24 modülün görev/hata/yeniden-kullanım alanlarını, eğitim aşamalarını, akademik adlandırmayı, karşılaştırmaları ve trafik sahnesi örneğini bütün halinde açıklar. İngilizce teknik eşleniği `docs/FINAL_ARCHITECTURE_MASTER_EN.md`.
2. **Son onaylı logo:** `assets/brand/TAUMOTION_APPROVED_FINAL_LOGO_2026-11-12.png` birebir kaynak PNG'den kopyalanır. Tau + araç silüeti, **tavanda LiDAR yok**. Eski purple reference ve diğer deneyler arşivde kalır; en son onaylı logo ile karıştırılmaz.
3. **Hybrid End-to-End adı:** Kamera/ego/rota→öğrenilmiş yörünge→RL→NMPC→komut zinciri kapsanır, fakat tek ağ olarak birlikte eğitilen model değildir; bu akademik ayrım dokümana işlendi.
4. **AutoE2E mükerrerliği düzeltildi:** M04 taxonomy, M05 0–4s student, M11 zero-init coupling/GRU, M18 faithfulness, M20 BEV+GRU baseline, M16/M21 yöntem/adaptörleri önceden vardı. Üçüncü aktif zorunlu planner eklenmedi.
5. **Klasik Autoware ile adil baseline:** Native Autoware Universe, ortak evidence+NMPC classical, AutoE2E learned planner ve uygun şekilde yeni learned mode ayrı sınıflandırıldı; benchmark sonucu olmayan sistemlere sayı uydurulmadı.
6. **τMOTION tahminleri:** NAVSIM v1 92.5 PDMS; v2 53 EPDMS; B2D 82 DS/60% SR; KITScenes 0.60 ADE/1.55 FDE, bunlar ölçüm değil koşullu nokta beklentisi. KITScenes ≤0.565 ADE/≤1.397 FDE ise ayrı güçlü hedef olarak korundu.
7. **Kullanıcı önceliği:** Mimari tanımının tam olması yayınlama önkoşulu; runtime/benchmark tamamlanması şu aşamada istenmiyor. Önceki dosyaların gerçek test durumunu yanlış değiştirmiyoruz.
8. **Sohbet eki:** U16–U25 görünür kullanıcı mesajları birebir, asistan özetleri açıkça non-verbatim, karar zaman çizelgesi eklendi.
9. **Önceki sürümler:** v1.0 ve v1.1 ZIP'leri ile v1.2 ZIP'i arşivde byte-byte korunur.
10. **Tamlık denetimi:** 24 modülün tümü gereklilik/girdi/çıktı/training/failure alanlarıyla master belgeye bağlanır; 54 edge ve dosya varlıkları otomatik doğrulanır; yeni approved logo hash'i güvence altına alınır.

Bunlar **tasarım dokümantasyonu revizyonudur**; benchmark sonuçları, solver çalıştırmaları ve fiziksel güvenlik sertifikası gibi iddialar içermez.
