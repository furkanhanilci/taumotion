#!/usr/bin/env python3
"""Portable D0 documentation audit; explicitly not model/vehicle verification."""
from pathlib import Path
import ast,csv,hashlib,json,re,subprocess,sys,xml.etree.ElementTree as ET
from urllib.parse import unquote
R=Path(__file__).resolve().parents[1]
checks=[]
def check(name,ok,detail=''):
    checks.append({'check':name,'passed':bool(ok),'detail':detail})
def get(p):return json.loads((R/p).read_text())
def read(p):return (R/p).read_text()
release=get('specs/release.json'); mods=get('specs/components.json');edges=get('specs/architecture_edges.json')
ids={m['id'] for m in mods}
check('Canonical 24 modules',len(mods)==24 and ids=={f'M{i:02d}' for i in range(24)})
for key in ['name','necessity','input','output','source','reuse','bridge','training','failure','acceptance','experiments']:
    check('Effective field: '+key,all(isinstance(m.get(key),str) and m[key].strip() for m in mods))
check('M10 critic is in effective training and output', 'critic' in mods[10]['training'].lower() and 'SafetyScoreBundle' in mods[10]['output'])
check('54 dependency payload records',len(edges)==54)
check('52 unique directed pairs',len({(e['from'],e['to']) for e in edges})==52)
check('Dependency IDs and endpoints valid',len({e['id'] for e in edges})==54 and all(e['from'] in ids and e['to'] in ids for e in edges))
check('Every edge scope explicit',all(e['scope'] in ['OFFLINE_ONLY','ONLINE_OR_EVAL'] for e in edges))
check('Offline payload scopes enforced',all(e['scope']=='OFFLINE_ONLY' for e in edges if 'offline' in e['payload'].lower() or e['from']=='M21'))
check('Offline cache cannot be an online critic input',all(e['scope']=='OFFLINE_ONLY' for e in edges if e['from']=='M17' and e['to']=='M10'))
check('M22 is sole actuator authorizer',{e['from'] for e in edges if e['to']=='M15'}=={'M22'} and 'M22' in mods[15]['input'])
graph=read('assets/diagrams/v1_3_1/dependencies.mmd')
check('Full graph covers every dependency',all(f'"{e["id"]}' in graph for e in edges) and len(re.findall(r'\|"D\d+',graph))==54)
tr=read('docs/FINAL_ARCHITECTURE_MASTER_TR.md');en=read('docs/FINAL_ARCHITECTURE_MASTER_EN.md');cat=read('docs/components.md')
check('Master TR current modules and effective fields',all(f"### {m['id']} — {m['name']}" in tr and m['training'] in tr and m['output'] in tr for m in mods))
check('Master EN all module rows',all(f'| {i} |' in en for i in ids))
check('Catalogue current effective fields',all(m['training'] in cat and m['output'] in cat and m['necessity'] in cat for m in mods))
with (R/'specs/component_bom.csv').open() as f:bom=list(csv.DictReader(f))
check('CSV mirrors current effective fields',len(bom)==24 and all(b['output']==m['output'] and b['training']==m['training'] for b,m in zip(bom,mods)))
cov=get('specs/coverage.json')
check('Original RQ1–RQ9 retained',cov['original_RQs']==[f'RQ{i}' for i in range(1,10)])
exps=set(sum((v for k,v in cov.items() if 'experiment' in k and isinstance(v,list)),[]))
check('E1–E24 plus E10-H retained',{f'E{i}' for i in range(1,25)}|{'E10-H'} <= exps)
check('N0–N9 and C0–C10 retained',set(cov['original_baselines']+cov['added_baselines'])=={f'N{i}' for i in range(10)}|{f'C{i}' for i in range(11)})
check('No scope reduction',cov['scope_reduction'] is False and release['scope_reduction'] is False)
check('Exactly two mandatory online planners',release['main_online_planners']==2)
reg=get('specs/validation_registry.json')
check('R1–R5 runtime levels NOT_RUN',all(v['status']=='NOT_RUN' and v['evidence']==[] for v in reg['levels'].values()))
check('R6–R9 runtime levels NOT_RUN',all(v['status']=='NOT_RUN' and v['evidence']==[] for k,v in reg['v1_2_new'].items() if k.startswith('R')))
check('All module runtime evidence empty',set(reg['components'])==ids and all(v['runtime']=='NOT_RUN' and not v['evidence'] for v in reg['components'].values()))
bench=get('specs/benchmark_expectations_v1_3.json')
check('All six user planning values retained',[x['point_expectation'] for x in bench['scenarios']]==[92.5,53,82,60,.6,1.55])
check('Forecast is not measured and empirical basis absent',bench['status']=='CONDITIONAL_ARCHITECTURE_FORECAST_NOT_MEASURED' and bench['empirical_basis_for_tau_point_estimates'] is None)
logo=R/release['approved_logo']
check('Approved logo signature and exact SHA256',logo.read_bytes().startswith(b'\x89PNG\r\n\x1a\n') and hashlib.sha256(logo.read_bytes()).hexdigest()==release['approved_logo_sha256'])
for p in ['README.md','README.tr.md']:
    check(p+' uses approved original and current diagram',release['approved_logo'] in read(p) and 'assets/diagrams/v1_3_1/main_architecture.svg' in read(p))
    content=read(p)
    images=re.findall(r'<img\b[^>]*\bsrc="([^"]+)"',content)
    check(p+' opens with approved logo then scientific poster',images[:2]==[release['approved_logo'],'assets/diagrams/v1_3_1/architecture_poster.png'] and content.lstrip().startswith('<p align="center">'))
    check(p+' uses generic scientific labels',not re.search(r'\b(?:Autoware|LEAD|Qwen|ReCogDrive|UniAD|AutoE2E|FPD-Drive|BridgeDrive|TorchRL|TensorDict|acados|CasADi|FilterPy|CARLA|Bench2Drive|NAVSIM|KITScenes|AlpaSim|NuRec|SimLingo)\b',content,re.I))
walkthrough=read('docs/scientific-walkthrough.md').split('\n',2)[2].rstrip()
check('README contains the complete scientific walkthrough',walkthrough in read('README.md'))
poster=read('assets/diagrams/v1_3_1/architecture_poster.svg')
poster_ids=set(re.findall(r'\bM\d{2}\b',poster))
for first,last in re.findall(r'M(\d{2})[–-]M(\d{2})',poster):
    poster_ids.update(f'M{i:02d}' for i in range(int(first),int(last)+1))
check('Scientific poster covers all 24 modules',ids<=poster_ids)
check('Scientific poster uses generic scientific labels',not re.search(r'\b(?:Autoware|LEAD|Qwen|ReCogDrive|UniAD|AutoE2E|FPD-Drive|BridgeDrive|CARLA)\b',poster,re.I))
check('Current figure builder does not redraw logo','mark(self' not in read('tools/build_diagrams_current.py'))
for p in sorted((R/'specs').glob('*.json')):
    try:json.loads(p.read_text());check('JSON parses: '+p.name,True)
    except Exception as e:check('JSON parses: '+p.name,False,str(e))
pins=get('specs/source_pins.json')['repositories']
check('All source pins are full commit SHAs',all(re.fullmatch('[0-9a-f]{40}',x['sha']) for x in pins))
bad=[];count=0
for p in (R/'assets').rglob('*.svg'):
    try:ET.parse(p);count+=1
    except Exception as e:bad.append((str(p),str(e)))
check('SVG XML parses',not bad,f'{count} SVG files; {bad}')
for name in ['main_architecture','runtime_contract','learning_and_evidence','architecture_poster']:
    check('Current figure variants: '+name,all((R/f'assets/diagrams/v1_3_1/{name}.{ext}').is_file() for ext in ['svg','png','pdf']))
missing=[]
for p in sorted(list(R.glob('*.md'))+list((R/'docs').glob('*.md'))+list((R/'history').glob('*.md'))):
    if 'verbatim' in p.name:continue
    content=p.read_text()
    content=re.sub(r'(?ms)^(```|~~~).*?^\1[^\n]*','',content)
    destinations=re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)',content)+re.findall(r'(?:src|href)="([^"]+)"',content)
    for dest in destinations:
        if dest.startswith(('https://','http://','mailto:','#','data:')):continue
        dest=unquote(dest.split('#')[0])
        if not dest:continue
        q=(p.parent/dest).resolve()
        if not q.exists() or (q.suffix=='.md' and 'verbatim' in q.name):missing.append((str(p.relative_to(R)),dest))
check('Markdown links and embedded images resolve in publication',not missing,str(missing[:30]))
bad=[]
for p in (R/'tools').glob('*.py'):
    try:ast.parse(p.read_text())
    except SyntaxError as e:bad.append((p.name,str(e)))
check('Python build and validation tools parse',not bad,str(bad))
check('Current PDF builder never slices code lines','s[:135]' not in read('tools/build_report_current.py'))
check('Inactive CI template targets current validator','tools/validate_spec.py' in read('tools/ci/validate-docs.yml'))
pdf=R/release['pdf']
try:
    info=subprocess.run(['pdfinfo',str(pdf)],check=True,text=True,capture_output=True).stdout
    pages=int(re.search(r'Pages:\s+(\d+)',info).group(1))
    text=subprocess.run(['pdftotext',str(pdf),'-'],check=True,text=True,capture_output=True).stdout
    check('PDF opens, current release, full module coverage',pages>=30 and '1.3.1' in text and all(i in text for i in ids),f'{pages} pages')
    check('PDF contains reviewed contracts and sources','H_effective' in text and 'SafetyScoreBundle' in text and 'source-audit-v1.3.1.md' in text)
except Exception as e:check('PDF integrity via Poppler',False,str(e))
result={'release':release['version'],'scope':'D0_DOCUMENTATION_ONLY','all_documentation_checks_passed':all(x['passed'] for x in checks),'count':len(checks),'passed':sum(x['passed'] for x in checks),'runtime_status':'NOT_RUN','checks':checks}
(R/'reports/documentation_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(f"Documentation: {result['passed']}/{result['count']}; runtime NOT_RUN")
for c in checks:
    if not c['passed']:print('FAIL:',c['check'],c['detail'])
sys.exit(0 if result['all_documentation_checks_passed'] else 1)
