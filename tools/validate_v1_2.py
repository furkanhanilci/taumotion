#!/usr/bin/env python3
"""Static documentation/provenance verification only, NEVER driving/runtime validation."""
from pathlib import Path
from datetime import datetime,timezone
import re,json,hashlib,csv,zipfile,sys
R=Path(__file__).resolve().parents[1]
checks=[]
def chk(name,ok,detail=''):
 checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':str(detail)})
 print(('PASS' if ok else 'FAIL'),name,str(detail)[:160]);return ok

def j(path):return json.loads((R/path).read_text(encoding='utf-8'))
comp=j('specs/components.json');edge=j('specs/architecture_edges.json');cv=j('specs/coverage.json');model=j('specs/model_selections.json');pin=j('specs/source_pins.json');v=j('specs/validation_registry.json')
ids={x['id'] for x in comp}
chk('24 unique main modules',len(comp)==len(ids)==24 and ids=={'M'+str(i).zfill(2) for i in range(24)},str(len(comp)))
chk('all architecture links valid',len(edge)>=44 and all(x['from'] in ids and x['to'] in ids for x in edge),str(len(edge)))
chk('new named critical submodule',any(x['id']=='M10' and 'Safety' in x.get('v1_2_extension','') for x in comp))
chk('v1.2 coverage and retained scope',cv.get('retained_24_main_modules') and cv.get('scope_reduction')==False and len(cv.get('added_v1_2_experiments',[]))==6,cv.get('added_v1_2_experiments'))
chk('new source pin registrations',all(x in {i['repo'] for i in pin['repositories']} for x in ['CountNemoChan/FPD-Drive','kesai-labs/lead','ShuLiu-ETHZ/BridgeDrive']),str(len(pin['repositories'])))
chk('no runtime outcome fabricated',v.get('runtime_claim')=='NO_RUNTIME_RESULTS' and all(x['status']=='NOT_RUN' for x in v['levels'].values()) and model.get('status','').endswith('no_runtime_or_new_critic_training'))
chk('original v1.1 ZIP byte-identical',hashlib.sha256((R/'archive/taumotion_original_v1_1.zip').read_bytes()).hexdigest()==hashlib.sha256(Path('/mnt/data/taumotion.zip').read_bytes()).hexdigest())
chk('original v1.0 ZIP byte-identical',hashlib.sha256((R/'archive/TAUMOTION_Final_Mimari_v1_0_2026-11-11.zip').read_bytes()).hexdigest()==hashlib.sha256(Path('/mnt/data/TAUMOTION_Final_Mimari_v1_0_2026-11-11.zip').read_bytes()).hexdigest())
chk('user-approved purple logo unchanged',hashlib.sha256((R/'assets/brand/APPROVED_PURPLE_TAU_REFERENCE_UNMODIFIED.png').read_bytes()).hexdigest()==hashlib.sha256(Path('/mnt/data/τmotion_açıklanabilir_otonom_sürüş_mimarisi.png').read_bytes()).hexdigest())
links=[];broken=[]
for f in list(R.glob('*.md'))+list((R/'docs').glob('*.md'))+list((R/'history').glob('*.md')):
 t=f.read_text(encoding='utf-8')
 for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',t):
  if url.startswith(('http://','https://','#','mailto:','sandbox:')):continue
  path=url.split('#')[0].split('?')[0]
  if path and not (f.parent/path).exists():broken.append((str(f.relative_to(R)),url))
  else:links.append((str(f.relative_to(R)),url))
chk('all internal markdown links resolve',not broken,broken[:20])
chk('post-v1.1 conversation has 15 verbatim visible user messages',len(re.findall(r'^## U\d+', (R/'history/post_v1_1_visible_user_messages_verbatim.md').read_text(encoding='utf-8'),re.M))==15)
chk('conversation integrity explicitly limits verbatim claims','VERBATIM DEĞİL' in (R/'history/post_v1_1_assistant_decision_summaries.md').read_text(encoding='utf-8'))
visual=R/'assets/diagrams/v1_2'
required=[f'{basename}_{lang}.{ext}' for basename in ['online','offline','control','full_modules'] for lang in ['tr','en'] for ext in ['dot','svg','pdf','png']]
chk('all 8 bilingual diagrams have editable/vector/raster formats',all((visual/n).is_file() and (visual/n).stat().st_size>500 for n in required),str(len(required)))
# Official code names forbidden only inside diagram labels, not source docs.
texts='\n'.join((visual/f'{b}_{l}.dot').read_text(encoding='utf-8') for b in ['online','offline','control','full_modules'] for l in ['tr','en'])
chk('no vendor project names in technical figure labels',not re.search(r'(?i)LEAD|FPD-Drive|BridgeDrive|Qwen|ReCogDrive|AutoE2E',texts))
chk('benchmark table labels measured tau data as N/A','τMOTION | **N/A**' in (R/'docs/benchmark-matrix-v1.2.md').read_text(encoding='utf-8'))
try:
 import fitz
 p=fitz.open(R/'reports/TAUMOTION_Architecture_Specification_v1.2.pdf')
 chk('v1.2 PDF opens and has substantial content',len(p)>=30 and 'Architecture Specification v1.2' in p[0].get_text(),str(len(p))+' pages')
 p.close()
except Exception as e:chk('v1.2 PDF opens and has substantial content',False,str(e))
for f in (R/'archive').glob('*.zip'):
 try:
  with zipfile.ZipFile(f) as z:chk('original archive ZIP CRC '+f.name,z.testzip() is None)
 except Exception as e:chk('original archive ZIP CRC '+f.name,False,str(e))
# Manifest excludes its own content and changing QA report, retaining all data files.
manifest=[]
for f in sorted(R.rglob('*')):
 if not f.is_file():continue
 rel=str(f.relative_to(R))
 if rel in ['reports/documentation_checks.json','reports/package_manifest_sha256.json']:continue
 if '__pycache__' in rel or rel.endswith('.pyc'):continue
 manifest.append({'path':rel,'size':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(R/'reports/package_manifest_sha256.json').write_text(json.dumps({'kind':'SHA256_MANIFEST_DOCUMENTATION_ARTIFACT','entries':manifest},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
passall=all(c['status']=='PASS' for c in checks)
report={'artifact_version':'1.2','date':'2026-11-11','kind':'DOCUMENTATION_AND_PACKAGE_VALIDATION_NOT_DRIVING_OR_MODEL_RUNTIME','overall_status':'PASS' if passall else 'FAIL','checks':checks,'files_hashed':len(manifest),'local_markdown_links_checked':len(links)+len(broken),'all_runtime_checks':'NOT_RUN','notes':['D0 static checks do not demonstrate model inference, adapter parity, GPU co-load, safety critic calibration or closed-loop driving.','Source pins are inspection baselines; downloaded weight hashes remain null.','Assistant chat texts are summaries, not complete verbatim platform transcripts.']}
(R/'reports/documentation_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Update machine registry D0 after validation, then refresh manifest to keep the report consistent.
v['v1_2_new']['D0_DOCUMENTATION']['status']='PASS' if passall else 'FAIL'
(R/'specs/validation_registry.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Hash registry again; no circular hash of the report itself.
for x in manifest:
 if x['path']=='specs/validation_registry.json':
  q=R/x['path'];x['size']=q.stat().st_size;x['sha256']=hashlib.sha256(q.read_bytes()).hexdigest()
(R/'reports/package_manifest_sha256.json').write_text(json.dumps({'kind':'SHA256_MANIFEST_DOCUMENTATION_ARTIFACT','entries':manifest},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('\nD0 DOCUMENTATION STATUS:',report['overall_status'],len(checks),'checks',len(manifest),'files')
sys.exit(0 if passall else 1)
