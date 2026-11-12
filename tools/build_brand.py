#!/usr/bin/env python3
"""Build original tau-dominant identity as SVG, PDF and transparent PNG."""
from pathlib import Path
import subprocess
from vector_art import Vector,mark
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/brand'
def export(v,name,transparent=False):
    p=OUT/name;v.save(p)
    cmd=['pdftocairo','-singlefile','-png','-scale-to','1800']
    if transparent:cmd.append('-transp')
    subprocess.run(cmd+[str(p.with_suffix('.pdf')),str(p)],check=True)
for theme in ['dark','light']:
    for mono in [False,True]:
        name='tau_'+('mono_' if mono else '')+theme
        v=Vector(800,800,'τMOTION — '+name);mark(v,0,0,theme=theme,mono=mono);export(v,name,True)
v=Vector(800,800,'τMOTION — compact tau symbol');mark(v,-40,-100,1.1,word=False);export(v,'tau_symbol',True)
v=Vector(1800,680,'τMOTION — evidence into motion')
v.rect(0,0,1800,680,'#071522')
for k in range(8):
    y=80+k*70
    v.path([('M',790,y),('C',1080,y-120,1250,y+100,1800,y-30)],stroke='#142d42',width=1.5)
for x,y in [(1070,170),(1330,350),(1550,170),(1650,530)]:
    v.circle(x,y,5,'#2e6474');v.circle(x,y,13,None,'#244353')
v.line([(80,76),(80,40),(116,40)],'#365568',2)
v.line([(1684,640),(1720,640),(1720,604)],'#365568',2)
mark(v,40,-50,.92)
v.text(850,190,'RESEARCH IN MOTION',17,'#71d9cd',True,4)
v.text(846,281,'Evidence into',62,'#eef7fd',True)
v.text(846,362,'intelligent motion.',62,'#eef7fd',True)
v.line([(850,410),(1455,410)],'#254559',1.4)
v.text(850,458,'Dual planning · Grounded reasoning · Predictive control',21,'#a6bacc')
v.text(850,547,'ARCHITECTURE SPECIFICATION',15,'#8ca4ba',True,2)
v.text(850,583,'v1.1  /  24 components  /  preserved research scope',18,'#718da5')
export(v,'repository_banner')
v=Vector(1800,1300,'τMOTION — identity system / Convergent Tau')
v.rect(0,0,1800,1300,'#edf2f7')
v.text(70,75,'τMOTION / CONVERGENT TAU',30,'#153047',True)
v.text(70,112,'Two paths. A shared direction. A custom Greek tau with a restrained secondary wordmark.',18,'#547083')
v.rect(55,155,840,850,'#071522',r=18);v.rect(920,155,825,850,'#ffffff',r=18)
mark(v,85,165,.96);mark(v,960,165,.96,theme='light')
v.text(90,958,'01  /  PRIMARY · DARK FIELD',17,'#849fb5',True,2)
v.text(955,958,'02  /  PRIMARY · LIGHT FIELD',17,'#627b91',True,2)
v.rect(55,1030,400,210,'#0a1b2a',r=14);mark(v,100,1000,.27,word=False,mono=True)
v.text(300,1142,'MONO',17,'#b3c7d8',True,2)
v.rect(480,1030,400,210,'#ffffff',r=14);mark(v,520,1000,.27,theme='light',word=False,mono=True)
v.text(730,1142,'MONO',17,'#3c5970',True,2)
palette=['#071522','#14334a','#24bfcc','#79f5d5','#4c67f2']
for i,c in enumerate(palette):
    v.rect(925+i*160,1050,138,112,c,r=8);v.text(925+i*160,1195,c,15,'#547083')
export(v,'identity_board')
print('Brand assets built:',len(list(OUT.glob('*.svg'))),'vector designs')
