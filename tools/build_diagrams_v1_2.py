#!/usr/bin/env python3
"""Bilingual editable DOT/SVG/PNG/PDF research diagrams. No new logo created."""
from pathlib import Path
import html, textwrap, subprocess, json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'/'diagrams'/'v1_2'
OUT.mkdir(parents=True,exist_ok=True)
C={'blue':'#eaf2ff','purple':'#f1eaff','green':'#e9f6ed','pink':'#ffedf5','amber':'#fff2d9','slate':'#edf1f8','white':'#ffffff'}
B={'blue':'#5284c7','purple':'#8452b0','green':'#429269','pink':'#bd527e','amber':'#ca943a','slate':'#7089a2'}
colors=['blue','purple','green','pink','amber','slate']
def esc(s): return s.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')
def name(s): return 'N_'+''.join(x if x.isalnum() else '_' for x in s)
def node(k,heading,desc='',kind='blue',shape='box',width=2.55,fontsize=13):
 text=heading+'\n'+desc if desc else heading
 # use plain multiline; DOT wraps according to manual newlines
 return f'"{k}" [label="{esc(text)}",shape={shape},style="rounded,filled",fillcolor="{C[kind]}",color="{B[kind]}",penwidth=1.8,fontname="DejaVu Sans",fontsize={fontsize},width={width},margin="0.22,0.18"];'
def edge(a,b,label='',style='solid',color='#77619b',constraint='true'):
 return f'"{a}"->"{b}" [color="{color}",penwidth=2.0,arrowsize=.8,style={style},constraint={constraint}' +(f',label="{esc(label)}",fontsize=10,fontcolor="#47556c"' if label else '')+'];'
def compose(title,subtitle,nodes,edges,clusters=(),size='16,10'):
 s=['digraph architecture {','graph [rankdir=LR,bgcolor="white",pad="0.4",nodesep=".5",ranksep=".85",splines=polyline,compound=true,labelloc="t",labeljust="l",label="'+esc(title+'\n'+subtitle)+'",fontname="DejaVu Sans",fontsize=26,fontcolor="#61268c",size="'+size+'",ratio=auto];','node [fontname="DejaVu Sans"];','edge [fontname="DejaVu Sans"];']
 for c in clusters:
  cid,color,ns,clabel=c
  s+=['subgraph cluster_'+cid+' {label="'+esc(clabel)+'";color="'+B[color]+'";style="rounded,dashed";penwidth=1.8; bgcolor="'+C[color]+'";']
  s += [nodes[x] for x in ns if x in nodes]
  s+=['}']
 done={x for _,_,ns,_ in clusters for x in ns}
 s += [v for k,v in nodes.items() if k not in done]
 s+=edges+['}']
 return '\n'.join(s)

def online(lang):
 tr=lang=='tr'
 T=lambda trS,enS:trS if tr else enS
 ns={
 'i':node('i',T('M00–M01  GİRİŞ VE SENKRONİZASYON','M00–M01  INPUTS & SYNCHRONIZATION'),T('Kameralar · ego durumu · rota\nKalibrasyon · kaynak izinleri · t0/AoI','Cameras · ego state · route\nCalibration · data privilege · t0/AoI'),'blue',width=3.1),
 'e':node('e',T('M02 / M23  BAĞIMSIZ KANIT','M02 / M23  INDEPENDENT EVIDENCE'),T('BEV, 3B aktör izleri, yol alanı\nTahmin, örtülme, veri yaşı','BEV, 3D actor tracks, drivable area\nForecast, occlusion, observation age'),'blue',width=3.05),
 'vlm':node('vlm',T('M03  GÖRSEL–DİL MUHAKEMESİ','M03  VISION–LANGUAGE REASONING'),T('Sahne bağlamı · kurallar · niyet','Scene semantics · rules · intent'),'purple'),
 'cot':node('cot',T('M04–M05  CoT + ZAMANSAL MUHAKEME','M04–M05  CoT + HORIZON REASONING'),T('Aktör, tehlike, neden, eylem, 0–4s','Actor, hazard, cause, action, 0–4s'),'purple'),
 'ground':node('ground',T('M06  KANIT / GÖRÜNÜRLÜK','M06  CLAIM / VISIBILITY GROUNDING'),T('Destekli / çelişkili / bilinmiyor\nÖrtülme, belirsizlik ve kalibrasyon','Supported / contradicted / unknown\nOcclusion, uncertainty, calibration'),'purple',width=3.0),
 'a':node('a',T('M07  AKIŞ TABANLI PLANLAYICI','M07  FLOW-BASED PLANNER'),T('Dondurulmuş model · doğal 5s ufuk','Frozen model · native 5s horizon'),'green'),
 'b':node('b',T('M08  DİFÜZYON PLANLAYICISI','M08  DIFFUSION PLANNER'),T('Dondurulmuş model · doğal 4s ufuk','Frozen model · native 4s horizon'),'green'),
 'pool':node('pool',T('M09  ORTAK ADAY HAVUZU','M09  CANONICAL CANDIDATE POOL'),T('4s / 0,1s · K=6 (3+3)\nGirdi/seed/horizon metaverisi korunur','4s / 0.1s · K=6 (3+3)\nKeep native input/seed/horizon metadata'),'green',width=3.0),
 'feature':node('feature',T('M10-a  FİZİKSEL ADAY ÖZELLİKLERİ','M10-a  PHYSICAL CANDIDATE FEATURES'),T('TTC · yol · ilerleme · konfor\nMPC uygunluk tahmini','TTC · area · progress · comfort\nMPC feasibility proxy'),'amber',width=3.0),
 'critic':node('critic',T('M10-b  ÖĞRENİLMİŞ GÜVENLİK CRITIC','M10-b  LEARNED SAFETY CRITIC'),T('NC / DAC / TTC / DDC / EP\nKonfor · uygulanabilirlik · kalibrasyon','NC / DAC / TTC / DDC / EP\nComfort · feasibility · calibration'),'amber',width=3.15),
 'rl':node('rl',T('M11  RİSK DUYARLI RL SEÇİCİ','M11  RISK-AWARE RL SELECTOR'),T('Aday dikkat + GRU · PPO/CVaR\nAyrık aday j · risk/ödül dengesi','Candidate attention + GRU · PPO/CVaR\nDiscrete candidate j · reward/risk'),'pink',width=3.0),
 'res':node('res',T('M12  8 BOYUTLU ARTIK DÜZELTME','M12  8-D BOUNDED RESIDUAL'),T('4 Δv + 4 Δd düğümü; düzgün eğri','4 Δv + 4 Δd knots; smooth reference'),'pink'),
 'safe':node('safe',T('M13  GÜVENLİK / UYGUNLUK','M13  SAFETY / FEASIBILITY SUPERVISOR'),T('Engel, yol, dinamik, zaman geçerliliği','Obstacle, road, dynamics, freshness'),'amber'),
 'nmpc':node('nmpc',T('M14  DİNAMİK NMPC','M14  DYNAMIC NMPC'),T('Araç modeli + OCP 4s / 40 aralık\nHedef: 20 Hz / 50ms kritik yol','Vehicle model + OCP 4s / 40 nodes\nTarget: 20 Hz / 50ms critical path'),'green',width=3.1),
 'gate':node('gate',T('M22  BAĞIMSIZ KOMUT GÖZETMENİ','M22  INDEPENDENT DEADLINE GUARDIAN'),T('Geç sonuç / eski ID / fallback','Late result / stale ID / fallback'),'green'),
 'act':node('act',T('M15  TEK ARAÇ KOMUT YAZICISI','M15  SINGLE VEHICLE COMMAND WRITER'),T('Direksiyon + gaz + fren; gerçekleşen eylem','Steering + throttle + brake; executed action'),'slate'),
 'runtime':node('runtime',T('M16  ASENKRON ZAMANLAYICI','M16  ASYNCHRONOUS SCHEDULER'),T('P0–P3 · kuyruk · AoI · GPU bütçesi','P0–P3 · queues · AoI · GPU budget'),'slate',width=3.0),
 'trace':node('trace',T('M17–M19  İZ / XAI / BENCHMARK','M17–M19  TRACE / XAI / BENCHMARK'),T('Ham teklif → onay → gerçek eylem\nPaired karşı-olgusal değerlendirme','Raw proposal → approval → executed action\nPaired counterfactual evaluation'),'slate',width=3.1),
 }
 es=[edge('i','e'),edge('i','vlm'),edge('vlm','cot'),edge('e','ground'),edge('cot','ground'),edge('i','a'),edge('i','b'),edge('a','pool'),edge('b','pool'),edge('pool','feature'),edge('feature','critic'),edge('ground','critic'),edge('critic','rl'),edge('ground','rl'),edge('rl','res'),edge('res','safe'),edge('safe','nmpc'),edge('nmpc','gate'),edge('gate','act'),edge('nmpc','rl',T('önceki kontrol verisi','prior control feedback'),'dashed','#ad88ce','false'),edge('act','i',T('yeni sahne','new observation'),'dashed','#8060ab','false'),edge('runtime','gate',T('deadline','deadline'),'dashed','#6c85a8','false'),edge('runtime','critic',T('güncellik','freshness'),'dashed','#6c85a8','false'),edge('act','trace','','dashed','#6c85a8','false'),edge('rl','trace','','dashed','#6c85a8','false')]
 groups=[('in','blue',['i','e'],T('GİRDİ ve ALGILAMA','INPUT & PERCEPTION')),('sem','purple',['vlm','cot','ground'],T('MUHAKEME ve KANIT','REASONING & EVIDENCE')),('plan','green',['a','b','pool'],T('ADAY ÜRETİMİ','CANDIDATE GENERATION')),('crit','amber',['feature','critic'],T('YENİ v1.2 GÜVENLİK KATMANI','NEW v1.2 SAFETY LAYER')),('policy','pink',['rl','res'],T('ÖĞRENİLMİŞ KARAR','LEARNED DECISION')),('exec','green',['safe','nmpc','gate','act'],T('FİZİKSEL YÜRÜTME','PHYSICAL EXECUTION')),('support','slate',['runtime','trace'],T('YATAY SERVİSLER','CROSS-CUTTING SERVICES'))]
 return compose('τMOTION  |  '+T('Nihai Çevrim İçi Sürüş Mimarisi','Final Online Driving Architecture'),T('v1.2 · Aynı 24 ana modül · M10 içinde yeni küçük Safety Critic · Birden çok hız ve geri besleme','v1.2 · Same 24 main modules · New small Safety Critic inside M10 · Multi-rate with feedback'),ns,es,groups,'30,15')

def offline(lang):
 tr=lang=='tr'; T=lambda a,b:a if tr else b
 ns={
 'data':node('data',T('ÇEŞİTLİ SÜRÜŞ KAYITLARI','DIVERSE DRIVING EPISODES'),T('Gerçek kayıtlar + CARLA / NAVSIM\nRig/rota/senaryo/seed fingerprint','Recorded data + CARLA / NAVSIM\nRig/route/scenario/seed fingerprints'),'blue'),
 'expert':node('expert',T('UZMAN POLİTİKA ve DATA','EXPERT POLICY & DATA'),T('Klasik ayrıcalıklı uzman + native kontrol\nÖğrenciye oracle bilgi VERİLMEZ','Privileged classical expert + native control\nOracle data NEVER passed to student'),'blue',width=3.1),
 'vis':node('vis',T('GÖRÜNÜRLÜK / ÖRTÜLME ETİKETİ','VISIBILITY / OCCLUSION LABELS'),T('Nesne mevcut ≠ sensörde görünür\nOffline instance/depth/LiDAR etiketleri','Actor exists ≠ sensor-visible\nOffline instance/depth/LiDAR labels'),'purple',width=3.0),
 'teacher':node('teacher',T('GELECEK BİLGİLİ ÖĞRETMEN','FUTURE-PRIVILEGED TEACHER'),T('Yalnız eğitimde gelecek veri\nKarşı-olgusal sonuç: rollout gerekir','Future allowed in training ONLY\nCounterfactual outcomes need rollout'),'purple',width=3.15),
 'multi':node('multi',T('ÇOKLU GEÇERLİ YÖRÜNGE HEDEFİ','MULTIPLE VALID TRAJECTORY TARGETS'),T('Tek insan hareketi tek doğru değil\nGeçerlilik maskesi + etiket kaynağı','One expert path is not the only valid option\nValid masks + source protocol'),'purple',width=3.1),
 'cache':node('cache',T('VERSİYONLU VERİ ÖNBELLEĞİ','VERSIONED DATA CACHE'),T('Ön işleme / model / dataset hash\nEski cache uyuşmazsa RED','Preprocess / model / dataset hashes\nReject stale cache'),'blue'),
 'critic':node('critic',T('SAFETY CRITIC EĞİTİMİ','SAFETY CRITIC TRAINING'),T('NC/DAC/TTC/DDC/EP/konfor\nRanking + false-safe + kalibrasyon','NC/DAC/TTC/DDC/EP/comfort\nRanking + false-safe + calibration'),'amber',width=3.1),
 'ranker':node('ranker',T('SUPERVISED ADAY SIRALAMA','SUPERVISED CANDIDATE RANKING'),T('Heuristic / fiziksel / çoklu skor\nAynı frozen aday havuzu','Heuristic / physical / multihead scores\nSame frozen candidate pool'),'amber'),
 'rl':node('rl',T('CARLA KAPALI DÖNGÜ PPO','CARLA CLOSED-LOOP PPO'),T('Aday seçimi + 8D residual\nEpisode maliyeti / CVaR pilotu','Candidate selection + 8D residual\nEpisode cost / CVaR pilot'),'pink'),
 'eval':node('eval',T('BAĞIMSIZ KIYASLAMA','INDEPENDENT BENCHMARKING'),T('NAVSIM PDMS/EPDMS · KITScenes ADE/FDE\nCARLA DS/SR · XAI · P95/P99 gecikme','NAVSIM PDMS/EPDMS · KITScenes ADE/FDE\nCARLA DS/SR · XAI · P95/P99 delay'),'green',width=3.4),
 'fail':node('fail',T('HATA ANALİZİ ve YENİ SÜRÜM','FAILURE ANALYSIS & NEXT REVISION'),T('Örtülme · domain · risk kuyruğu\nTest rotası eğitime karıştırılmaz','Occlusion · domain · risk tail\nNever train on held-out test routes'),'green')}
 es=[edge('data','expert'),edge('data','vis'),edge('expert','teacher'),edge('teacher','multi'),edge('vis','multi'),edge('multi','cache'),edge('vis','cache'),edge('cache','critic'),edge('cache','ranker'),edge('critic','rl'),edge('ranker','rl'),edge('rl','eval'),edge('eval','fail'),edge('fail','data',T('yeni TRAIN senaryosu','new TRAIN scenarios'),'dashed','#7b57b1','false')]
 groups=[('ing','blue',['data','expert','cache'],T('VERİ / KAYNAK SINIRI','DATA & PROVENANCE')),('teac','purple',['vis','teacher','multi'],T('OFFLINE DENETİM - ORACLE İZOLASYONU','OFFLINE SUPERVISION — ORACLE ISOLATION')),('train','amber',['critic','ranker'],T('EĞİTİM AŞAMASI I','TRAINING STAGE I')),('ppo','pink',['rl'],T('EĞİTİM AŞAMASI II','TRAINING STAGE II')),('eva','green',['eval','fail'],T('ÖLÇÜM / İYİLEŞTİRME','EVALUATION & IMPROVEMENT'))]
 return compose('τMOTION  |  '+T('Çevrim Dışı Eğitim ve Doğrulama','Offline Training and Validation'),T('v1.2 · Uzman → görünürlük → çoklu hedef → critic → PPO/CVaR → held-out benchmark','v1.2 · Expert → visibility → multi-target → critic → PPO/CVaR → held-out benchmark'),ns,es,groups,'25,10')

def control(lang):
 tr=lang=='tr';T=lambda a,b:a if tr else b
 ns={
 'policy':node('policy',T('M11  RL ADAY SEÇİMİ','M11  RL CANDIDATE SELECTION'),T('j + 8D Δv/Δd\ncritic ve CoT bilgileriyle','j + 8D Δv/Δd\ncritic and CoT-conditioned'),'pink'),
 'res':node('res',T('M12  RESIDUAL REFERANS','M12  RESIDUAL REFERENCE'),T('4 hız, 4 yanal ofset düğümü\nBaşlangıç sürekliliği','4 speed, 4 lateral knots\nStart-state continuity'),'pink'),
 'safety':node('safety',T('M13  PLAN UYGUNLUK DENETİMİ','M13  PLAN FEASIBILITY SUPERVISOR'),T('Araç sınırları · aktör riskleri\nSürüş alanı · yaş/mask','Vehicle limits · actor hazards\nRoad boundaries · age/masks'),'amber'),
 'nmpc':node('nmpc',T('M14  DİNAMİK NMPC / OCP','M14  DYNAMIC NMPC / OCP'),T('[X,Y,ψ,vx,vy,r,δ,a]\n[δ̇,jerk] · 4s / 40 düğüm','[X,Y,ψ,vx,vy,r,δ,a]\n[δ̇,jerk] · 4s / 40 nodes'),'green',width=3.2),
 'gate':node('gate',T('M22  DEADLINE / ID GÖZETMENİ','M22  DEADLINE / ID GUARDIAN'),T('Hedef toplam kontrol bütçesi 50ms\nGecikmiş / eski sonuç reddi','Target total control budget 50ms\nReject late / stale results'),'green'),
 'fallback':node('fallback',T('YEDEK KONTROL DALl','FALLBACK CONTROL BRANCH'),T('Yalnız hâlâ geçerli kontrol dizisi\nveya kontrollü yavaşlama','Only valid leftover control sequence\nor controlled deceleration'),'slate'),
 'car':node('car',T('M15  TEK KOMUT YAZICISI','M15  SINGLE ACTUATOR WRITER'),T('Direksiyon + gaz + fren\nCARLA araç durumu değişir','Steering + throttle + brake\nCARLA vehicle state changes'),'slate'),
 'trace':node('trace',T('M17  İZ VE NEDENSELLİK','M17  TRACE & CAUSALITY'),T('seçilen / önerilen / kabul edilen\nsolver / guardian / gerçek eylem','selected / proposed / accepted\nsolver / guardian / actual'),'purple')}
 es=[edge('policy','res'),edge('res','safety'),edge('safety','nmpc'),edge('nmpc','gate'),edge('gate','car'),edge('gate','fallback',T('reddet','reject'),'dashed','#9869ab'),edge('fallback','car'),edge('nmpc','policy',T('önceki kontrol','prior tracking'),'dashed','#9869ab','false'),edge('car','trace','','dashed','#9869ab','false'),edge('res','trace','','dashed','#9869ab','false'),edge('gate','trace','','dashed','#9869ab','false')]
 return compose('τMOTION  |  '+T('Gerçek Zamanlı Kontrol ve Geri Besleme','Real-Time Control and Feedback'),T('v1.2 · Plan güvenliği ile komut gecikmesi iki ayrı sorumluluk · 20Hz TASARIM HEDEFİ','v1.2 · Plan feasibility and command timing are separate concerns · 20Hz DESIGN TARGET'),ns,es,[('p','pink',['policy','res'],T('ÖĞRENİLMİŞ ÖNERİ','LEARNED PROPOSAL')),('n','amber',['safety'],T('FİZİKSEL KAPİ','PHYSICAL GATE')),('c','green',['nmpc','gate'],T('KONTROL ve ZAMANLAMA','CONTROL & TIMING')),('o','slate',['fallback','car','trace'],T('KOMUT / İZ','ACTUATION / TRACE'))],'20,8')

def full(lang):
 tr=lang=='tr'; T=lambda a,b:a if tr else b
 items=json.loads((ROOT/'specs/components.json').read_text())
 ns={}
 for x in items:
  i=x['id'];idx=int(i[1:]);kind='blue' if idx<=2 or idx==23 else 'purple' if 3<=idx<=6 else 'green' if 7<=idx<=9 else 'amber' if idx==10 else 'pink' if idx in (11,12) else 'green' if idx in (13,14,15,22) else 'slate'
  txt=x['name'] if tr else {'M00':'Data privilege','M01':'Synchronization','M02':'Independent evidence','M03':'Semantic VLM','M04':'Structured reasoning','M05':'Horizon reasoning','M06':'Claim grounding','M07':'Flow planner','M08':'Diffusion planner','M09':'Canonical candidates','M10':'Features + NEW safety critic','M11':'Risk-aware RL selection','M12':'Bounded 8D residual','M13':'Feasibility supervisor','M14':'Dynamic NMPC','M15':'Single command writer','M16':'Scheduling / freshness','M17':'Trace and versions','M18':'Counterfactual XAI','M19':'Benchmark / statistics','M20':'Baselines / expert','M21':'Data / multi-target training','M22':'Deadline guardian','M23':'Evidence time propagation'}[i]
  ns[i]=node(i,i+'  '+txt,'','pink' if i=='M10' else kind,width=2.65,fontsize=12)
 d=[('M00','M01'),('M01','M02'),('M02','M23'),('M01','M03'),('M03','M04'),('M04','M05'),('M02','M06'),('M23','M06'),('M05','M06'),('M01','M07'),('M01','M08'),('M07','M09'),('M08','M09'),('M09','M10'),('M06','M10'),('M10','M11'),('M06','M11'),('M11','M12'),('M12','M13'),('M13','M14'),('M14','M22'),('M22','M15')]
 es=[edge(a,b) for a,b in d]+[edge('M14','M11','','dashed','#8a6bb8','false'),edge('M15','M01','','dashed','#8a6bb8','false'),edge('M16','M22','','dashed','#8a6bb8','false'),edge('M15','M17','','dashed','#8a6bb8','false'),edge('M17','M18','','dashed','#8a6bb8','false'),edge('M17','M19','','dashed','#8a6bb8','false'),edge('M20','M19','','dashed','#8a6bb8','false'),edge('M21','M10','','dashed','#8a6bb8','false'),edge('M21','M06','','dashed','#8a6bb8','false')]
 groups=[('input','blue',['M00','M01','M02','M23'],T('Girdi/kanıt','Input/evidence')),('sem','purple',['M03','M04','M05','M06'],T('Semantik/XAI','Semantics/XAI')),('plan','green',['M07','M08','M09'],T('Yörünge','Motion proposal')),('learner','pink',['M10','M11','M12'],T('Risk & RL','Risk & RL')),('ctl','green',['M13','M14','M22','M15'],T('Fiziksel kontrol','Physical control')),('sup','slate',['M16','M17','M18','M19','M20','M21'],T('Destek/eğitim/benchmark','Support/training/benchmark'))]
 return compose('τMOTION  |  '+T('Modül Arayüz Haritası M00–M23','Module Interface Map M00–M23'),T('Siyah kutular değil; denetlenebilir veri sözleşmeleri. Kesikli bağlantılar: destek/eğitim/geri besleme','Explicit interfaces, not black boxes. Dashed edges: support/training/feedback'),ns,es,groups,'30,17')

def render(name,src):
 file=OUT/(name+'.dot');file.write_text(src,encoding='utf-8')
 for fmt in ['svg','pdf','png']:
  cmd=['dot','-T'+fmt,'-o',str(OUT/(name+'.'+fmt)),str(file)]
  if fmt=='png':cmd[1:1]=['-Gdpi=135']
  subprocess.run(cmd,check=True,timeout=65)
 print(name, [round((OUT/(name+'.'+fmt)).stat().st_size/1024) for fmt in ['svg','pdf','png']])
if __name__=='__main__':
 for language in ['tr','en']:
  render('online_'+language,online(language))
  render('offline_'+language,offline(language))
  render('control_'+language,control(language))
  render('full_modules_'+language,full(language))
