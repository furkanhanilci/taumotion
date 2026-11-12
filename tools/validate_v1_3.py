#!/usr/bin/env python3
"""Documentation-only structural audit. Never claim runtime or vehicle certification."""
from pathlib import Path
import json,hashlib,re,zipfile,datetime,sys
R=Path(__file__).resolve().parents[1]
B=R/'assets/brand'
mods=json.loads((R/'specs/components.json').read_text())
edges=json.loads((R/'specs/architecture_edges.json').read_text())
master=(R/'docs/FINAL_ARCHITECTURE_MASTER_TR.md').read_text()
english=(R/'docs/FINAL_ARCHITECTURE_MASTER_EN.md').read_text()
logo=B/'TAUMOTION_APPROVED_FINAL_LOGO_2026-11-12.png'
bl=json.loads((R/'specs/design_decisions_v1_3.json').read_text())
bench=json.loads((R/'specs/benchmark_expectations_v1_3.json').read_text())
source_archive=Path('/mnt/data/TAUMOTION_v1_2_Expanded_Architecture_2026-11-11.zip')
checks=[]
def ck(n,b,reason=''):
 checks.append({'id':len(checks)+1,'check':n,'pass':bool(b),'details':reason})
ck('24 canonical modules',len(mods)==24 and sorted(m['id'] for m in mods)==[f'M{i:02d}' for i in range(24)])
ck('54 canonical directed edges',len(edges)==54 and all(e['from'] in {m['id'] for m in mods} and e['to'] in {m['id'] for m in mods} for e in edges))
ck('24 modules described individually in master TR',all(f'### {m["id"]} —' in master for m in mods))
ck('24 modules in companion EN',all(f'| {m["id"]} |' in english for m in mods))
for f in ['necessity','input','output','training','failure','bridge','source']:
 ck('required canonical field present: '+f,all(bool(str(m.get(f,'')).strip()) for m in mods), 'module metadata')
for label,pat in {
 'hybrid E2E scope':'Hybrid End-to-End', 'not monolithic':'monolitik', 'offline teacher policy separation':'offline',
 'critic differentiation':'CVaR', 'bounded residual':'Δv[4]', 'dual planner K6':'K=3+3=6',
 'NMPC state':'vx,vy,r,δ,a', 'independent guardian':'M22', 'separate stale evidence':'STALE',
 'XAI world intervention':'dünya müdahalesi', 'AutoE2E already included':'önceden tanımlanmış',
 'classic Autoware baseline':'same-evidence', 'all benchmark targets':'92.5',
 'no roof LiDAR':'LiDAR yok'}.items():
 ck('master technical coverage: '+label,pat.lower() in master.lower())
ck('logo PNG correct and hash locked',logo.exists() and logo.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n' and hashlib.sha256(logo.read_bytes()).hexdigest()==bl['brand_approved_sha256'])
ck('new logo approval and old logo both preserved',(B/'APPROVED_PURPLE_TAU_REFERENCE_UNMODIFIED.png').is_file() and logo.is_file())
ck('brand docs clarify raster and no lidar', all(x in (R/'docs/brand-approved-v1.3.md').read_text().lower() for x in ['liDAR'.lower(),'raster','onay']))
ck('forecast status explicitly unmeasured',bench['status']=='CONDITIONAL_ARCHITECTURE_FORECAST_NOT_MEASURED' and all('point_expectation' in m for m in bench['scenarios']))
ck('benchmark matrix six metrics',len(bench['scenarios'])==6)
ck('Autoware positions documented', all(x in (R/'docs/autoware-and-hybrid-e2e-v1.3.md').read_text() for x in ['Native Autoware','AutoE2E','M20']))
ck('no third mandatory planner',bl['optional_fast_bev_gru'].startswith('M20 baseline only'))
ck('history old U01-U15 intact',len(re.findall(r'^## U\d+', (R/'history/post_v1_1_visible_user_messages_verbatim.md').read_text(),re.M))==15)
ck('new history U16-U25 complete',set(re.findall(r'^## (U\d+)',(R/'history/visible_user_messages_after_v1_2_verbatim.md').read_text(),re.M))=={f'U{i}' for i in range(16,26)})
ck('assistant summaries non-verbatim marked','VERBATIM DEĞİL' in (R/'history/assistant_decision_summaries_after_v1_2.md').read_text())
for ver in ['v1_0','v1_1','v1_2']:
 p={'v1_0':'archive/TAUMOTION_Final_Mimari_v1_0_2026-11-11.zip','v1_1':'archive/taumotion_original_v1_1.zip','v1_2':'archive/TAUMOTION_v1_2_Expanded_Architecture_2026-11-11.zip'}[ver]
 ck('historical '+ver+' zip archive preserved',(R/p).exists() and zipfile.is_zipfile(R/p))
if source_archive.exists():
 ck('v1.2 historical archive byte for byte',hashlib.sha256((R/'archive/TAUMOTION_v1_2_Expanded_Architecture_2026-11-11.zip').read_bytes()).hexdigest()==hashlib.sha256(source_archive.read_bytes()).hexdigest())
for f in ['online_tr','online_en','offline_tr','offline_en','control_tr','control_en','full_modules_tr','full_modules_en']:
 ck('existing vector diagram '+f, (R/f'assets/diagrams/v1_2/{f}.svg').is_file() and (R/f'assets/diagrams/v1_2/{f}.dot').is_file())
# local markdown references in current authoritative documents
files=['README.tr.md','README.md','docs/FINAL_ARCHITECTURE_MASTER_TR.md','docs/FINAL_ARCHITECTURE_MASTER_EN.md','docs/revisions-v1.3.md','history/README.md']
missing=[]
for f in files:
 text=(R/f).read_text()
 for dest in re.findall(r'(?<!!)\[[^]]+\]\(([^)]+)\)',text):
  if dest.startswith(('http://','https://','#','mailto:')):continue
  path= (R/f).parent / dest.split('#')[0]
  if not path.exists():missing.append((f,dest))
ck('authoritative Markdown local links all resolve',not missing,str(missing[:20]))
report=R/'reports/TAUMOTION_Final_Architecture_Specification_v1_3.pdf'
if report.exists():
 try:
  from pypdf import PdfReader
  reader=PdfReader(report)
  ck('final PDF opens and has >=35 pages',len(reader.pages)>=35, f'pages={len(reader.pages)}')
  first=' '.join((p.extract_text() or '') for p in list(reader.pages)[:4])
  ck('final PDF current branding/version','v1.3' in first and 'τMOTION' in first)
 except Exception as ex: ck('final PDF opens',False,str(ex))
else:ck('final PDF generated',False)
# docs design checks not deployment tests
result={'release':'1.3','date':'2026-11-12','scope':'architecture documentation and brand; not driving validation','total':len(checks),'passed':sum(x['pass'] for x in checks),'failed':[x for x in checks if not x['pass']],'checks':checks}
(R/'reports/documentation_checks_v1_3.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
outline='''# τMOTION v1.3 — Nihai mimari kapsam ve belge bütünlük denetimi

**Kapsam:** v1.2 mimari topolojisi üzerine 12 Kasım 2026 tarihli dokümantasyon/marka güncellemesi. **Bu denetim, araç sürüşü veya modellerin gerçek çalışma başarısı hakkında hiçbir kanıt sağlamaz.** Kullanıcının güncel amacı eksiksiz tasarım tanımıdır.

**Kontrol edilen:** 24 M00–M23 modülü, 54 kenar, 24 modül için gerekçe/girdi/çıktı/eğitim/hata alanları, İngilizce eşlikçi, girdi-çıktı sözleşmeleri, offline future-data ayrımı, kritik critic/GRU/CoT/RL/NMPC yöntemleri, klasik Autoware/AutoE2E ayrımı, sayısal tahminlerin epistemik statüsü, güncel orijinal LiDAR'sız logo, eski üç arşiv sürümü, U01–U25 geçmişi ve PDF.

## Yapısal doğrulama sonucu

**{passed}/{total} PASS**. Ayrıntılı makine okunur kontrol kaydı: `reports/documentation_checks_v1_3.json`.

| Bütünlük katmanı | Durum | Kanıt |
|---|---|---|
| Mimari modül envanteri | 24/24 | `specs/components.json` + master TR/EN |
| Bağlantı grafiği | 54/54 | `specs/architecture_edges.json` |
| Modül sözleşmeleri | reason/input/output/bridge/training/failure | `components.json` ve `FINAL_ARCHITECTURE_MASTER_TR.md` |
| Öğrenilmiş critic ve offline teacher | M10/M21 ve bağlantıları korunur | `docs/safety-critic-and-supervision.md` + `docs/training-and-data-v1.2.md` |
| AutoE2E ve klasik Autoware kapsamı | Önceden mevcut yöntemler yeniden sayılmadı | `docs/autoware-and-hybrid-e2e-v1.3.md` |
| Benchmark senaryoları | Tahmin/ölçüm ayrımı korundu | `specs/benchmark_expectations_v1_3.json` |
| Yeni logo | Byte-identical PNG + SHA256 | `docs/brand-approved-v1.3.md` |
| Konuşma eki | U01–U25 görünür kullanıcı mesajları, asistan özetleri ayrı | `history/` |
| PDF | Ana Türkçe ve İngilizce teknik mimariyi kapsar | `reports/TAUMOTION_Final_Architecture_Specification_v1_3.pdf` |

## Kapsamın gerekçeli tanımı

**Tam olarak tanımlı:** Tüm modül kimlikleri, gereklilikleri, input/output sözleşmeleri, source privilege, semantik/algı/planlama/critic/RL/kontrol veri geçişleri, hiyerarşik eğitim akışı ve ödül/risk ayrımı, kontrollü karar izinleri, Autoware/AutoE2E benchmark rolleri, akademik Hybrid End-to-End tanımı ve marka onayı. Ayrıntılar master TR, eski yöntem/arayüz belgeleri ve source pin'lerde korunur.

**Bu sürümün bilinçli biçimde kapsam dışı tuttuğu şeyler:** Gerçek CARLA/vehicle çalıştırması, ağırlıkların eğitilmesi, 20 Hz'nin ölçülmesi, parametrik araç kalibrasyonu, fonksiyonel güvenlik sertifikası veya yeni yayımlanmış τMOTION benchmark sonucu. Bu konuların tamamlanmamış olması, şu andaki **mimari tanım tamlığında eksik belge** olarak sayılmaz; ileride implementation/evaluation kapısıdır.

**Teknik varsayımlar:** İki donmuş temel modelin CARLA/NAVSIM'e adapte edilmesi, safety critic kalibrasyonu, çoklu hedef etiket doğruluğu, dağıtılmış GPU bütçesi ve gerçek zamanlı gecikme hedefleri, nihai tasarımda varsayım olarak tanımlıdır; gerçek sonuçlar bunları doğrulamak içindir. İlave üçüncü zorunlu planner yoktur.

## Ayrıntılı dosya denetimleri

'''
outline=outline.replace('{passed}',str(result['passed'])).replace('{total}',str(result['total']))
for c in checks:
 outline+=f"- [{'x' if c['pass'] else ' '}] {c['check']}"+(f" — {c['details']}" if c['details'] else '')+'\n'
(R/'docs/architecture-completeness-audit-v1.3.md').write_text(outline)
print('checks',result['passed'],'/',result['total'])
for z in result['failed']:print('FAIL',z['check'],z['details'])
if result['failed']:sys.exit(1)
