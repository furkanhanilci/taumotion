#!/usr/bin/env python3
"""Publication vector poster inspired by the supplied two-tier reference layout."""
from pathlib import Path
import math, subprocess
from reportlab.pdfbase.pdfmetrics import stringWidth
from vector_art import Vector
R=Path(__file__).resolve().parents[1]
W,H=3200,2220
INK='#202544'; MUTED='#52617c'; PURPLE='#6432ac'
PALETTE=[('#1763aa','#edf6ff'),('#7b40ad','#f6effd'),('#278451','#eef9f0'),('#b43b91','#fff0fa'),('#ad761b','#fff7e6'),('#7438b6','#f5efff'),('#2674a6','#eef7ff'),('#205e9e','#eef5ff')]
def wrap(s,width,size,bold=False):
    out=[];line=''
    for word in s.split():
        test=(line+' '+word).strip()
        if line and stringWidth(test,'BrandBold' if bold else 'Brand',size)>width:out.append(line);line=word
        else:line=test
    if line:out.append(line)
    return out
class Poster(Vector):
    def gradient(self,x,y,w,h,a,b):
        self.path([('M',x,y),('L',x+w,y),('L',x+w,y+h),('L',x,y+h),('Z',)],gradient=(x,y,x,y+h,[a,b]))
    def para(self,x,y,text,width,size=24,color=MUTED,bold=False):
        for line in wrap(text,width,size,bold):self.text(x,y,line,size,color,bold);y+=size*1.34
        return y
    def arrow(self,x1,y1,x2,y2,color=PURPLE,dash=False):
        self.line([(x1,y1),(x2,y2)],color,4,[10,9] if dash else None)
        a=math.atan2(y2-y1,x2-x1)
        self.path([('M',x2,y2),('L',x2-14*math.cos(a-.5),y2-14*math.sin(a-.5)),('L',x2-14*math.cos(a+.5),y2-14*math.sin(a+.5)),('Z',)],fill=color)
    def icon(self,x,y,kind,c):
        if kind=='camera':
            self.rect(x,y+8,42,29,'#ffffff',c,5);self.circle(x+22,y+23,9,'#ffffff',c,3);self.line([(x+7,y+8),(x+12,y),(x+28,y),(x+33,y+8)],c,3)
        elif kind=='shield':
            self.path([('M',x+22,y),('L',x+43,y+9),('L',x+39,y+28),('L',x+22,y+44),('L',x+5,y+28),('L',x+1,y+9),('Z',)],stroke=c,width=3)
            self.line([(x+11,y+20),(x+20,y+29),(x+33,y+13)],c,3)
        elif kind=='nodes':
            for a,b in [((0,20),(21,0)),((0,20),(23,41)),((21,0),(43,20)),((23,41),(43,20)),((0,20),(43,20))]:self.line([(x+a[0],y+a[1]),(x+b[0],y+b[1])],c,2)
            for a,b in [(0,20),(21,0),(23,41),(43,20)]:self.circle(x+a,y+b,6,'#ffffff',c,3)
        elif kind=='stack':
            for dy in [0,12,24]:self.line([(x,y+dy+10),(x+22,y+dy),(x+44,y+dy+10),(x+22,y+dy+20),(x,y+dy+10)],c,3)
        elif kind=='trajectory':
            for dy in [0,12,24]:self.path([('M',x,y+dy+15),('C',x+13,y+dy-8,x+26,y+dy+30,x+44,y+dy)],stroke=c,width=3)
        else:
            self.circle(x+22,y+22,20,'#ffffff',c,3);self.line([(x+22,y+8),(x+22,y+22),(x+34,y+26)],c,3)
    def box(self,x,y,w,title,body,color,fill,icon='stack',minheight=0):
        tl=wrap(title,w-88,25,True);bl=wrap(body,w-32,23)
        h=max(minheight,32+len(tl)*32+16+len(bl)*31+14)
        self.rect(x,y,w,h,'#ffffff',color,13);self.icon(x+16,y+17,icon,color)
        self.para(x+76,y+35,title,w-88,25,INK,True)
        self.para(x+16,y+32+len(tl)*32+16,body,w-32,23,MUTED)
        return y+h+16
    def road(self,x,y,w,h,c='#727cd2'):
        self.rect(x,y,w,h,'#edf2ff',None,12)
        self.path([('M',x+35,y+h),('L',x+w*.44,y+12),('L',x+w*.56,y+12),('L',x+w-35,y+h),('Z',)],fill='#b9c5e7')
        for t in [.25,.55,.85]:
            self.line([(x+w*.5,y+h*t),(x+w*.5,y+h*(t+.12))],'#ffffff',4)
        self.rect(x+w*.38,y+h*.55,w*.25,h*.28,'#ffffff',c,8)
        self.rect(x+w*.41,y+h*.58,w*.19,h*.09,c,None,3)
    def trajectories(self,x,y,w,h):
        self.rect(x,y,w,h,'#ffffff','#dfd9ea',12)
        for i,c in enumerate(['#2767d6','#39a874','#bd4eac','#d69a21']):
            yy=y+25+i*27
            self.path([('M',x+30,y+h/2),('C',x+w*.4,y+h/2,x+w*.62,yy,x+w-24,yy)],stroke=c,width=4,dash=[9,7]);self.circle(x+w-24,yy,6,c)
        self.rect(x+8,y+h/2-12,40,24,'#edf2ff',INK,6)

def build():
    p=Poster(W,H,'τMOTION — scientific architecture: online driving and offline research')
    p.gradient(0,0,W,H,'#f1f0ff','#ffffff')
    # Restrained road / city ribbon; no replacement of the approved logo.
    p.path([('M',0,155),('C',470,22,680,188,1030,165),('L',1030,190),('C',670,208,400,80,0,210),('Z',)],gradient=(0,140,1000,140,['#c8c5f5','#f5f6ff']))
    for i,hh in enumerate([40,72,52,105,80,128,68,98,47,83]):p.rect(2680+i*45,100-hh/2,27,hh,'#d5cff4',None,2)
    p.text(1060,78,'τMOTION',61,PURPLE,True,5)
    p.text(600,153,'Hybrid Autonomous Driving Architecture',58,INK,True)
    p.text(685,211,'Grounded reasoning  ·  Dual proposals  ·  Risk-aware learning  ·  Predictive control',29,MUTED)
    p.rect(40,245,3120,54,'#ffffff','#d9d2ed',15)
    p.text(64,281,'ARCHITECTURE v1.3.1',23,PURPLE,True)
    p.text(525,281,'24 modules  /  two frozen motion generators  /  20 Hz control target  /  runtime evaluation pending',23,MUTED)
    p.rect(30,320,3140,1150,'#ffffff','#a799d0',24)
    p.rect(48,309,820,61,PURPLE,None,20);p.text(80,351,'01   ONLINE DRIVING PIPELINE',31,'#ffffff',True)
    p.text(915,350,'Concurrent inference branches; arrows show selected data dependencies.',24,MUTED)
    titles=['Inputs &\nsynchronization','Independent\nperception','Grounded\nreasoning','Dual motion\ngeneration','Candidate\nevaluation','Risk-aware\ndecision','Refinement\n& control','Execution\n& explanation']
    modules=['M00–M01','M02 / M23','M03–M06','M07–M09','M10','M11','M12–M14 / M22','M15 / M17–M18']
    blocks=[
      [('Causal sensor history','Multi-camera images, calibration and native temporal sampling.','camera'),('Ego & route context','Pose, velocity, acceleration, steering state and permitted navigation.','trajectory'),('Time & provenance','Observation times, source versions, valid masks and data access rules.','clock')],
      [('BEV scene evidence','Object detection, actor tracking, drivable area and motion forecasts.','stack'),('Visibility & uncertainty','Occluded is not absent. Keep association confidence and unknown regions.','shield'),('Evidence propagation','Retiming / filtering preserves the original observation timestamp.','clock')],
      [('Vision–language reasoning','Scene meaning, actor intent, rules and a structured rationale.','nodes'),('Horizon reasoning','Actor / hazard / cause / action claims for now through +4 seconds.','stack'),('Evidence grounding','Supported, contradicted, unknown, conflict or stale; calibrated claim masks.','shield')],
      [('A · Flow matching','Frozen conditional trajectory generation; seeded multimodal proposals.','trajectory'),('B · Diffusion','Frozen iterative denoising planner; complementary candidate trajectories.','nodes'),('Canonical candidate pool','Nominal K=6 (3+3); common frame, valid time overlap and native provenance.','stack')],
      [('Physical features','Collision geometry, TTC, road area, progress, comfort and control proxy.','stack'),('Learned safety critic','Typed multihead outputs with ranking supervision and calibration.','shield'),('Control feasibility','Evaluate age, valid horizon and physical limits; retain per-head uncertainty.','clock')],
      [('Recurrent policy','Candidate attention + GRU; evidence-gated semantic features.','nodes'),('Hybrid PPO action','Select candidate j and its conditional bounded residual distribution.','trajectory'),('Episode tail risk','CVaR objective during policy learning; separate reward and cost values.','shield')],
      [('8D residual','4 speed + 4 lateral knots; smooth correction.','trajectory'),('Feasibility gate','Check fresh scene evidence, road and vehicle limits.','shield'),('Dynamic NMPC','Constrained vehicle dynamics; receding-horizon tracking.','stack'),('Deadline guardian','Independent timing gate; reject late results; authorize fallback.','clock')],
      [('Single command writer','Calibrated steering, throttle and brake; one actuation authority.','shield'),('Full decision trace','Raw → refined → accepted → executed; record solver and gate interventions.','stack'),('Decision explanation','Grounded rationale, selected path, risk estimates and actual motion.','nodes')]
    ]
    xs=[52+i*390 for i in range(8)]
    for i,x in enumerate(xs):
        c,fill=PALETTE[i];p.rect(x+4,409,374,926,'#e6e6f0',None,18);p.rect(x,402,374,926,fill,c,18)
        p.gradient(x+1,403,372,110,c,'#443472' if i in [1,3,5] else c)
        p.text(x+18,437,f'{i+1:02d}   {modules[i]}',21,'#ffffff',True)
        for j,line in enumerate(titles[i].split('\n')):p.text(x+18,473+j*31,line,28,'#ffffff',True)
        yy=532
        for title,body,ico in blocks[i]:yy=p.box(x+12,yy,350,title,body,c,fill,ico)
        if yy>1318:raise ValueError(f'Lane {i} overflow {yy}')
        free=1308-yy
        if free>125:
            if i in [0,1,7]:p.road(x+16,yy+5,342,min(free-10,155),c)
            elif i==3:p.trajectories(x+16,yy+5,342,min(free-10,155))
            elif i==5:
                p.text(x+24,yy+42,'π(j, r | s)',32,c,True);p.para(x+24,yy+83,'Small trainable policy; large generators stay frozen.',320,23,MUTED)
        # Only true adjacent dependencies; perception/reasoning do not feed frozen planners.
        if i in [0,1,3,4,5,6]:p.arrow(x+374,920,x+390,920)
    # Explicit scene bus to the two independent model branches.
    p.line([(238,402),(238,384),(1409,384)],'#7d8caa',3)
    for x in [1006,1396]:p.arrow(x,384,x,402,'#7d8caa')
    p.line([(1005,1328),(1005,1350),(1788,1350)],PURPLE,3)
    p.arrow(1788,1350,1788,1328,PURPLE)
    p.text(1100,1381,'Grounded claims → critic + policy; fresh scene evidence also constrains control.',23,PURPLE)
    p.line([(2980,1328),(2980,1428),(220,1428)],PURPLE,5)
    p.arrow(220,1428,220,1328,PURPLE)
    p.rect(440,1400,2355,55,'#f1ecfc',None,20)
    p.text(471,1437,'CLOSED LOOP  ·  actuator → environment → next observation    |    M16: multirate scheduling, age, deadlines and compute',25,PURPLE,True)
    # Offline tier: general methods, not source-project names.
    p.rect(30,1530,3140,535,'#ffffff','#a799d0',24)
    p.rect(48,1508,1170,61,PURPLE,None,20);p.text(80,1550,'02   OFFLINE LEARNING, EVALUATION & RESEARCH',29,'#ffffff',True)
    p.text(1260,1550,'M19–M21  ·  Future / oracle labels stay outside live policy inputs.',25,MUTED)
    off=[
      ('Data generation', 'stack', 'Expert demonstrations, causal sensor logs, diverse routes, weather and rare events. Versioned splits and cache fingerprints.', 'TRAIN ONLY: iterate on training failures.'),
      ('Annotation & supervision','shield','Visibility / occlusion labels, multiple valid trajectory targets, grounded reasoning and counterfactual rollout outcomes.','Privileged future information is label-only.'),
      ('Small-model learning','nodes','Critic + ranking + calibration; horizon-student distillation; supervised initialization → closed-loop PPO → CVaR studies.','Train selector / residual; freeze large planners.'),
      ('Evaluation & explanation','trajectory','Trajectory error, driving success, safety events, tail risk, comfort, latency and memory. Paired semantic / world interventions.','Matched sensors, candidates, compute and control.'),
      ('Failure analysis & transfer','clock','Ablations, expert comparisons, robustness, human explanation studies, visual representations and cross-domain transfer.','Preserve held-out tests; version every data cycle.')]
    for i,(title,ico,body,note) in enumerate(off):
        x=52+i*624;c,fill=PALETTE[[0,1,2,4,5][i]];p.rect(x,1598,600,440,fill,c,18)
        p.rect(x+1,1599,598,76,c,None,16);p.text(x+20,1648,f'{i+1:02d}  {title}',28,'#ffffff',True)
        p.icon(x+26,1700,ico,c);p.para(x+92,1726,body,474,26,INK)
        p.rect(x+18,1929,564,90,'#ffffff',None,12);p.para(x+32,1961,note,534,24,c,True)
        if i<4:p.arrow(x+600,1817,x+624,1817)
    p.rect(40,2103,3120,72,'#ece8f7',None,19)
    p.text(70,2148,'RESEARCH CONTRIBUTIONS',25,PURPLE,True)
    for x,s in [(575,'Evidence-conditioned choice'),(1235,'Calibrated risk assessment'),(1875,'Physically constrained motion'),(2575,'Causal explanation analysis')]:p.text(x,2148,s,24,INK,True)
    p.text(55,2202,'Design specification · numerical rates are targets · illustrative overview; the complete 54-record dependency graph remains the implementation reference.',21,MUTED)
    return p
if __name__=='__main__':
    dest=R/'assets/diagrams/v1_3_1/architecture_poster';build().save(dest)
    subprocess.run(['pdftocairo','-singlefile','-png','-scale-to','4000',str(dest.with_suffix('.pdf')),str(dest)],check=True)
    print('Scientific poster: SVG / PDF / 4000px PNG')
