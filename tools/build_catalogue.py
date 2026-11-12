#!/usr/bin/env python3
"""Generate effective module catalogue, CSV and full dependency view; no runtime code."""
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def write(p,s): (ROOT/p).write_text(s,encoding='utf-8')
def build():
    modules=json.loads((ROOT/'specs/components.json').read_text())
    edges=json.loads((ROOT/'specs/architecture_edges.json').read_text())
    parts=[]
    for m in modules:
        body=f"### {m['id']} — {m['name']}\n\n"
        for label,k in [('Neden var','necessity'),('Girdi','input'),('Çıktı','output'),('Hazır yöntem','reuse'),('Kaynak','source'),('Köprü','bridge'),('Öğrenme','training'),('Hata davranışı','failure'),('Kabul kanıtı','acceptance'),('Deneyler','experiments')]:
            body+=f"**{label}:** {m[k]}\n\n"
        if 'v1_2_extension' in m: body+=f"**Korunan v1.2 eklemesi:** {m['v1_2_extension']}\n\n"
        parts.append(body)
    write('docs/components.md','# Bileşen kataloğu — 24 bileşen\n\nArchitecture Specification v1.3.1. Etkin alanlar v1.2 genişlemelerini içerir. Runtime: NOT_RUN.\n\n'+''.join(p.replace('### ','## ',1) for p in parts))
    p=ROOT/'docs/FINAL_ARCHITECTURE_MASTER_TR.md'; s=p.read_text();a=s.index('### M00 —');b=s.index('## X. Kaynaklar')
    p.write_text(s[:a]+''.join(parts)+'\n'+s[b:])
    keys=['id','name','necessity','reuse','source','input','output','bridge','training','failure','experiments','acceptance','implementation_status']
    with (ROOT/'specs/component_bom.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,keys,extrasaction='ignore');w.writeheader();w.writerows(modules)
    # Names from the English master, avoiding a second mutable name registry.
    en=(ROOT/'docs/FINAL_ARCHITECTURE_MASTER_EN.md').read_text()
    names={line.split('|')[1].strip():line.split('|')[2].strip() for line in en.splitlines() if line.startswith('| M')}
    lines=['flowchart TB']
    for m in modules: lines.append(f'    {m["id"]}["{m["id"]}: {names[m["id"]]}"]')
    for e in edges:
        label=e['id']+(' OFFLINE' if e['scope']=='OFFLINE_ONLY' else '')
        arrow='-.->' if e['scope']=='OFFLINE_ONLY' else '-->'
        lines.append(f'    {e["from"]} {arrow}|"{label}"| {e["to"]}')
    write('assets/diagrams/v1_3_1/dependencies.mmd','\n'.join(lines)+'\n')
    doc='# Complete dependency records — v1.3.1\n\nAll 24 modules and 54 payload records (52 unique directed module pairs). Dashed edges are offline-only. This logical data dependency graph is not a process/thread scheduling graph. Current ego, route and immutable candidate references are resolved by the shared snapshot contract.\n\nThe compact [main figure](../assets/diagrams/v1_3_1/main_architecture.svg) shows selected online paths for readability. This full view and the table below preserve every registered record.\n\n```mermaid\n'+'\n'.join(lines)+'\n```\n\n| Record | From | To | Scope | Payload |\n|---|---|---|---|---|\n'
    for e in edges:doc+=f"| {e['id']} | {e['from']} | {e['to']} | {e['scope']} | {e['payload']} |\n"
    write('docs/dependency-graph.md',doc)
if __name__=='__main__':build();print('Current catalogue, CSV and all dependency records generated')
