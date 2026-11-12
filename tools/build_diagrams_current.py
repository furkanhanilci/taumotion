#!/usr/bin/env python3
"""Scientific diagrams for Architecture Specification v1.3.1; editable vector source."""
from pathlib import Path
import math,subprocess
from reportlab.pdfbase.pdfmetrics import stringWidth
from vector_art import Vector
ROOT=Path(__file__).resolve().parents[1]
def wrap(s,width,size,bold=False):
    words=s.split();out=[];line=''
    for word in words:
        nxt=(line+' '+word).strip()
        if stringWidth(nxt,'BrandBold' if bold else 'Brand',size)>width and line:out.append(line);line=word
        else:line=nxt
    if line:out.append(line)
    return out
class Diagram(Vector):
    def __init__(self,w,h,title,sub):
        super().__init__(w,h,title);self.rect(0,0,w,h,'#f5f8fc')
        self.text(60,65,title,34,'#113047',True);self.text(60,105,sub,18,'#607a90')
    def box(self,x,y,w,h,title,body,kind='blue'):
        palette={'blue':('#e7effa','#77a0d6'),'teal':('#e0f3ed','#67b8a3'),'purple':('#eee8f7','#a48dc7'),'gold':('#fff2d6','#d0a24b'),'gray':('#eaf0f5','#9eb1c2')}
        fill,stroke=palette[kind];self.rect(x,y,w,h,fill,stroke,14);yy=y+32
        for s in wrap(title,w-36,23,True):self.text(x+18,yy,s,23,'#13344b',True);yy+=28
        for p in body.split('\n'):
            for s in wrap(p,w-36,18):self.text(x+18,yy+7,s,18,'#4b697e');yy+=24
        if yy-3>y+h:raise ValueError('Box overflows: '+title)
    def arrow(self,pts,col='#507790',label=None,at=None,dash=False):
        self.line(pts,col,2.8,[9,6] if dash else None)
        x,y=pts[-1];xp,yp=pts[-2];a=math.atan2(y-yp,x-xp)
        self.path([('M',x,y),('L',x-13*math.cos(a-.43),y-13*math.sin(a-.43)),('L',x-13*math.cos(a+.43),y-13*math.sin(a+.43)),('Z',)],fill=col)
        if label:self.text(at[0],at[1],label,16,col)
def build():
    gs=[]
    g=Diagram(2200,1580,'Evidence-grounded dual planning','Architecture Specification v1.3.1 | 24 components | Control, evidence age and decision attribution')
    g.box(680,155,840,110,'M00–M01 | Synchronized scene and provenance','Cameras · ego history · calibration · allowed route context · simulation and operational clocks','gray')
    for x in [290,830,1370,1910]:g.arrow([(1100,265),(1100,305),(x,305),(x,345)])
    g.box(60,345,460,145,'M02 | Independent visual evidence','BEV, tracking, map, motion forecast and traffic-rule observations','teal')
    g.box(600,345,460,145,'M07 | Flow-matching planner','Native multimodal input and seeded trajectory proposals')
    g.box(1140,345,460,145,'M08 | Diffusion planner','Native multimodal input and seeded trajectory proposals')
    g.box(1680,345,460,145,'M03 | Semantic VLM','Causal scene context, short rationale and structured semantic proposals','purple')
    g.box(60,565,460,140,'M23 | Evidence time propagation','Native forecast alignment / Kalman prediction; original observation age retained','teal')
    g.box(600,565,1000,140,'M09–M10 | Canonical candidates + learned safety critic','Nominal 4 s / valid overlap · physical features + learned multihead safety critic · calibrated head types · MPC proxy')
    g.box(1680,565,460,140,'M04–M05 | Structured horizon reasoning','Actor / hazard / rule taxonomy; 0–4 s context; teacher or small student','purple')
    for x in [290,830,1370,1910]:g.arrow([(x,490),(x,565)])
    g.arrow([(520,630),(600,630)],'#34977e')
    g.box(60,800,460,145,'M06 | Claim-level grounding','Evidence support, contradiction, unknown state, calibration and age','teal')
    g.arrow([(290,705),(290,800)],'#34977e')
    g.arrow([(1910,705),(1910,752),(150,752),(150,800)],'#9476b8','structured claims',(1640,744))
    g.arrow([(500,800),(570,800),(570,720),(1550,720),(1550,705)],'#34977e','grounded claims to critic',at=(650,742))
    g.box(680,830,840,150,'M11 | Risk-aware learned selection','Candidate attention + recurrent memory; evidence-gated semantics; hybrid policy with CVaR research objective','gold')
    g.arrow([(520,872),(680,872)],'#34977e')
    g.arrow([(1100,705),(1100,830)],label='candidate features',at=(1120,795))
    g.arrow([(680,915),(550,915),(550,1050),(240,1050),(240,1130)],'#bc8e36','selected candidate',at=(270,1040))
    for x,title,body,k in [
      (60,'M12 | Bounded residual','4 speed + 4 lateral knots; valid horizon masks','gold'),
      (480,'M13 | Feasibility supervisor','Reference validity, constraints and fallback request','teal'),
      (900,'M14 | Dynamic NMPC','Vehicle model, nonuniform horizon / RTI options','teal'),
      (1320,'M22 | Deadline guardian','Independent timing; reject late results; command selection','gold'),
      (1740,'M15 | Vehicle actuation','Single writer; calibrated steer, throttle and brake','gray')]:
        g.box(x,1130,360,145,title,body,k)
    for x in [420,840,1260,1680]:g.arrow([(x,1200),(x+60,1200)])
    g.arrow([(500,705),(540,705),(540,1090),(1080,1090),(1080,1130)],'#34977e','aged forecasts / constraints',at=(700,1080))
    g.arrow([(660,1090),(660,1130)],'#34977e')
    g.box(1690,990,450,100,'M16 | Runtime scheduling','Age · deadlines · events · resource budgets','gray')
    g.arrow([(1690,1040),(1500,1040),(1500,1130)],'#8495a6')
    g.arrow([(1080,1275),(1080,1310),(660,1310),(660,1275)],'#bc8e36','solver veto',at=(790,1302),dash=True)
    g.arrow([(1500,1275),(1500,1360),(2165,1360),(2165,915),(1520,915)],'#bc8e36','solver / gate / tracking feedback',at=(1690,1351),dash=True)
    g.arrow([(1920,1275),(1920,1410),(25,1410),(25,210),(680,210)],'#7791a6',dash=True)
    for x,title,body in [(60,'M17 | Decision trace','Raw → refined → accepted → executed'),(600,'M18 | Counterfactual XAI','Fixed-path interventions and human study'),(1140,'M19–M20 | Evaluation','Versioned benchmarks and fair baselines'),(1680,'M21 | Transfer and data','Expert / visibility / multi-target labels')]:
        g.box(x,1460,460,95,title,body,'gray')
    gs.append(('main_architecture',g))
    g=Diagram(1900,1180,'Runtime composition and command ownership','Different model rates; one actuator writer; no blocking dependency on a late model or solver')
    g.box(60,165,530,140,'Scene and model services','Native environments and checkpoint contracts; M03/M07 can share one VLM weight service')
    g.box(685,165,530,140,'M16 | Resource and age scheduler','Bounded pending queue; generation IDs; periodic / EDF / AoI-event policies','gold')
    g.box(1310,165,530,140,'M23 | Evidence prediction bridge','Update time alignment, preserve capture time, expire unsupported information','teal')
    g.arrow([(590,235),(685,235)]);g.arrow([(1215,235),(1310,235)])
    g.box(60,440,530,160,'Perception · A · B · semantics','Frequency sweeps are pilot hypotheses.\nMeasure cold, warm, co-load and renderer contention.')
    g.box(685,440,530,160,'Policy and reference validation','Asynchronous proposals; fresh state snapshot; geometry and uncertainty checks','teal')
    g.box(1310,440,530,160,'M14 | NMPC worker','Preparation + feedback measured separately; late results cannot overwrite new generations','teal')
    g.arrow([(950,305),(950,365),(325,365),(325,440)])
    g.arrow([(590,520),(685,520)]);g.arrow([(1215,520),(1310,520)])
    g.box(685,740,530,160,'M22 | Independent deadline guardian','Accept current valid result, use a still-valid continuation, or select a calibrated stop profile','gold')
    g.box(1310,740,530,160,'M15 | Single vehicle command writer','Normal and fallback commands share one output path; log the actual executed command','gray')
    g.arrow([(1575,600),(1575,670),(950,670),(950,740)])
    g.arrow([(950,600),(950,740)],'#8495a6','deadline / state / reference',at=(650,655),dash=True)
    g.arrow([(1215,820),(1310,820)])
    g.box(60,740,530,160,'20 Hz critical path budget','Example only: 4 ms snapshot/check + 32 ms feedback + 4 ms gate/publish + 10 ms jitter reserve','gray')
    g.text(60,1000,'P0  Synchronous reference',24,'#13344b',True)
    g.text(60,1040,'P1  Asynchronous teacher + dual planners',24,'#13344b',True)
    g.text(1010,1000,'P2  Small semantic student + dual planners',24,'#13344b',True)
    g.text(1010,1040,'P3  Conditional planner calls',24,'#13344b',True)
    g.text(60,1130,'All profiles remain in scope. Successful synchronous driving does not establish real-time operation.',21,'#607a90')
    gs.append(('runtime_contract',g))
    g=Diagram(1900,1120,'Learning and evidence maturity','Offline initialization → closed-loop pilot → tail-risk study; document checks never imply runtime validation')
    for x,title,body,col in [(60,'1 | Native parity and profiling','Official checkpoints; adapter equivalence; joint inference and control timing','blue'),(520,'2 | Offline initialization','Visibility + multi-target labels; small critic, ranking and horizon-student training','purple'),(980,'3 | Small closed-loop PPO pilot','Masks, recurrent state, hybrid log-prob, reward and shared supervisor','gold'),(1440,'4 | CVaR pilot and full study','Policy-versioned episodes; quantile stability, tail uncertainty and compute budget','gold')]:
        g.box(x,180,400,210,title,body,col)
    for x in [460,920,1380]:g.arrow([(x,285),(x+60,285)])
    g.box(60,520,550,190,'Comparison classes','Native systems · within-model sensor ablations · fixed candidates · matched K · matched compute · shared controller','teal')
    g.box(675,520,550,190,'Preserved research scope','RQ1–RQ11; E1–E24 and E10-H.\nCritic, multi-target, visibility, strong challengers and compute studies retained.','purple')
    g.box(1290,520,550,190,'Attribution and statistics','Paired routes/seeds; cluster intervals; raw proposal, supervisor, NMPC, guardian and executed action','teal')
    g.box(60,825,1780,170,'Evidence levels — current runtime state: NOT RUN','D0 Specification checks   /   S0 Source inspection   /   R1 Native inference   /   R2 Adapter parity\nR3 Runtime integration   /   R4 Closed-loop evaluation   /   R5 Hardware-specific real-time profile','gray')
    gs.append(('learning_and_evidence',g))
    return gs
if __name__=='__main__':
    for name,g in build():
        p=ROOT/'assets/diagrams/v1_3_1'/name;p.parent.mkdir(parents=True,exist_ok=True);g.save(p)
        subprocess.run(['pdftocairo','-singlefile','-png','-scale-to','2200',str(p.with_suffix('.pdf')),str(p)],check=True)
    print('3 architecture diagrams built')
