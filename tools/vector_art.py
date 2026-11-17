"""Small native SVG/PDF renderer for project-owned vector artwork."""
from pathlib import Path
from html import escape
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
for n,f in [('Brand','DejaVuSans.ttf'),('BrandBold','DejaVuSans-Bold.ttf')]:
    if n not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
class Vector:
    def __init__(self,w,h,title):
        self.w,self.h,self.title=w,h,title;self.ops=[]
    def rect(self,x,y,w,h,fill,stroke=None,r=0):
        self.ops.append(('rect',x,y,w,h,fill,stroke,r))
    def text(self,x,y,s,size=18,fill='#dce8f4',bold=False,tracking=0):
        self.ops.append(('text',x,y,s,size,fill,bold,tracking))
    def path(self,commands,fill=None,stroke=None,width=1,gradient=None,dash=None):
        self.ops.append(('path',commands,fill,stroke,width,gradient,dash))
    def line(self,points,stroke='#6b8195',width=2,dash=None):
        self.path([('M',*points[0])]+[('L',*p) for p in points[1:]],stroke=stroke,width=width,dash=dash)
    def circle(self,x,y,r,fill,stroke=None,width=1):
        k=.5522847498*r
        self.path([('M',x+r,y),('C',x+r,y+k,x+k,y+r,x,y+r),('C',x-k,y+r,x-r,y+k,x-r,y),('C',x-r,y-k,x-k,y-r,x,y-r),('C',x+k,y-r,x+r,y-k,x+r,y),('Z',)],fill,stroke,width)
    def save(self,path):
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img"><title>{escape(self.title)}</title>']
        c=canvas.Canvas(str(path.with_suffix('.pdf')),pagesize=(self.w,self.h));c.setTitle(self.title)
        self.render(c,svg);c.save();svg.append('</svg>');path.with_suffix('.svg').write_text('\n'.join(svg))
    def draw(self,c):self.render(c,None)
    def render(self,c,svg):
        H=self.h
        for i,op in enumerate(self.ops):
            if op[0]=='rect':
                _,x,y,w,h,f,s,r=op
                c.setFillColor(HexColor(f))
                if s:c.setStrokeColor(HexColor(s))
                c.setLineWidth(1);c.roundRect(x,H-y-h,w,h,r,stroke=bool(s),fill=1)
                if svg is not None:svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}" stroke="{s or "none"}"/>')
            elif op[0]=='text':
                _,x,y,t,sz,f,b,tr=op
                c.setFont('BrandBold' if b else 'Brand',sz);c.setFillColor(HexColor(f))
                # PDF character spacing persists across text objects; reset it even at zero.
                tx=c.beginText(x,H-y)
                tx.setFont('BrandBold' if b else 'Brand',sz)
                tx.setCharSpace(tr)
                tx.textOut(t)
                c.drawText(tx)
                if svg is not None:svg.append(f'<text x="{x}" y="{y}" fill="{f}" font-family="DejaVu Sans,sans-serif" font-size="{sz}" font-weight="{700 if b else 400}" letter-spacing="{tr}">{escape(t)}</text>')
            else:
                _,cmds,f,s,width,gr,dash=op;p=c.beginPath()
                for cmd in cmds:
                    if cmd[0]=='M':p.moveTo(cmd[1],H-cmd[2])
                    elif cmd[0]=='L':p.lineTo(cmd[1],H-cmd[2])
                    elif cmd[0]=='C':p.curveTo(cmd[1],H-cmd[2],cmd[3],H-cmd[4],cmd[5],H-cmd[6])
                    elif cmd[0]=='Z':p.close()
                if gr:
                    x0,y0,x1,y1,stops=gr;c.saveState();c.clipPath(p,stroke=0,fill=0)
                    c.linearGradient(x0,H-y0,x1,H-y1,[HexColor(z) for z in stops],extend=True);c.restoreState()
                if f:c.setFillColor(HexColor(f))
                if s:c.setStrokeColor(HexColor(s))
                c.setLineWidth(width);c.setDash(dash or [])
                if s or f:c.drawPath(p,stroke=bool(s),fill=bool(f))
                c.setDash([])
                if svg is not None:
                    fill=f or 'none'
                    if gr:
                        x0,y0,x1,y1,stops=gr
                        svg.append(f'<defs><linearGradient id="g{i}" gradientUnits="userSpaceOnUse" x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}">'+''.join(f'<stop offset="{j/(len(stops)-1):.3f}" stop-color="{z}"/>' for j,z in enumerate(stops))+'</linearGradient></defs>');fill=f'url(#g{i})'
                    d=' '.join(cmd[0]+' '+' '.join(str(round(a,3)) for a in cmd[1:]) for cmd in cmds)
                    da=f' stroke-dasharray="{" ".join(map(str,dash))}"' if dash else ''
                    svg.append(f'<path d="{d}" fill="{fill}" stroke="{s or "none"}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{da}/>')
def transform(commands,x,y,scale):
    return [(c[0],*[round((x if i%2==0 else y)+v*scale,3) for i,v in enumerate(c[1:])]) for c in commands]
TAU=[('M',125,215),('C',170,174,210,155,265,155),('L',686,155),('L',630,247),('L',490,247),('L',445,473),('C',429,551,464,578,543,542),('L',585,522),('L',563,626),('C',510,655,448,671,396,649),('C',335,624,307,574,324,490),('L',375,247),('L',233,247),('C',194,247,163,260,133,281),('Z',)]
ACCENT=[('M',150,213),('C',189,186,225,176,267,176),('L',647,176),('L',625,210),('L',466,210),('L',407,493),('C',388,581,430,621,500,603),('L',546,583),('L',539,613),('C',480,639,429,638,395,610),('C',365,585,359,552,372,488),('L',431,210),('L',252,210),('C',210,210,180,224,151,241),('Z',)]
RIM=[('M',184,197),('C',210,185,237,181,268,181),('L',635,181)]
def mark(v,x,y,scale=1,theme='dark',word=True,mono=False):
    if mono:
        col='#ffffff' if theme=='dark' else '#0b2135';v.path(transform(TAU,x,y,scale),fill=col)
    else:
        colors=['#79f5d5','#24bfcc','#4c67f2'] if theme=='dark' else ['#009b8c','#157eaa','#3653cd']
        v.path(transform(TAU,x,y,scale),gradient=(x+130*scale,y+155*scale,x+560*scale,y+655*scale,colors))
        v.path(transform(ACCENT,x,y,scale),fill='#c7fff0' if theme=='dark' else '#73e6d1')
        v.path(transform(RIM,x,y,scale),stroke='#f4fffc' if theme=='dark' else '#baf9e7',width=2.2*scale)
    if word:
        col=('#9bb1c6' if theme=='dark' else '#527084') if not mono else ('#ffffff' if theme=='dark' else '#0b2135')
        v.text(x+265*scale,y+730*scale,'MOTION',32*scale,col,True,12*scale)
