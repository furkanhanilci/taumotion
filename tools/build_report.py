#!/usr/bin/env python3
"""Build the consolidated specification, never the driving runtime."""
from pathlib import Path
import csv,html,json,re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Flowable,Image
from reportlab.pdfbase import pdfmetrics
from vector_art import Vector,mark
from build_diagrams import build as diagrams
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports';OUT.mkdir(exist_ok=True);W=A4[0]-88
pdfmetrics.registerFontFamily('Brand',normal='Brand',bold='BrandBold',italic='Brand',boldItalic='BrandBold')
S={'b':ParagraphStyle('Body',fontName='Brand',fontSize=9.2,leading=13.5,spaceAfter=6,textColor=colors.HexColor('#20394c')),
'h1':ParagraphStyle('H1',fontName='BrandBold',fontSize=19,leading=25,spaceAfter=15,keepWithNext=True,textColor=colors.HexColor('#12344a')),
'h2':ParagraphStyle('H2',fontName='BrandBold',fontSize=12.2,leading=17,spaceBefore=12,spaceAfter=7,keepWithNext=True,textColor=colors.HexColor('#147b85')),
'cell':ParagraphStyle('Cell',fontName='Brand',fontSize=7,leading=10),
'cap':ParagraphStyle('Caption',fontName='Brand',fontSize=8,leading=11,spaceAfter=12,textColor=colors.HexColor('#60798d'))}
class Drawing(Flowable):
    def __init__(self,v,width=W):self.v=v;self.width=width;self.height=width*v.h/v.w
    def draw(self):
        self.canv.saveState();self.canv.scale(self.width/self.v.w,self.width/self.v.w);self.v.draw(self.canv);self.canv.restoreState()
def inline(text,source=None,web=False):
    slots=[]
    def link(m):
        label,url=m.groups()
        if not url.startswith(('https://','http://')):
            if source:
                try:url='../'+str((source.parent/url).resolve().relative_to(ROOT))
                except ValueError:pass
            value=f'<a href="{html.escape(url,quote=True)}">{html.escape(label)}</a>' if web else html.escape(label)
        else:
            tag='a' if web else 'link';value=f'<{tag} href="{html.escape(url,quote=True)}">{html.escape(label)}</{tag}>'
        slots.append(value);return f'LINKSLOT{len(slots)-1}END'
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text);text=html.escape(text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text);text=re.sub(r'\x60([^\x60]+)\x60',r'<b>\1</b>',text)
    for i,s in enumerate(slots):text=text.replace(f'LINKSLOT{i}END',s)
    return text
FILES=['README.tr.md','docs/revisions-v1.1.md','docs/architecture.md','docs/runtime-contract.md','docs/components.md','docs/interfaces.md','docs/methods.md','docs/evidence-policy.md','docs/experiments.md','docs/pilot-protocol.md','docs/implementation.md','docs/scope-and-decisions.md','docs/research.md','docs/brand.md']
story=[];web=[]
cover=Vector(1600,500,'τMOTION Architecture Specification v1.1');cover.rect(0,0,1600,500,'#071522');mark(cover,0,-25,.63)
cover.text(600,170,'Architecture',49,'#edf6fc',True);cover.text(600,235,'Specification v1.1',49,'#edf6fc',True)
cover.text(600,308,'Evidence into intelligent motion.',25,'#87d8d0');cover.text(600,380,'11 NOV 2026  /  RESEARCH DESIGN',17,'#8daabd',True,2)
story.extend([Spacer(1,20),Drawing(cover),Spacer(1,26),Paragraph('Hazır bileşenlerin birleştirilmesi, çalışma zamanı sözleşmeleri ve kapsamlı araştırma protokolü',S['h1']),Paragraph('24 bileşen · RQ1–RQ9 korunur · Yeni zamanlama ve deadline deneyleri · Özgün τ ağırlıklı görsel kimlik',S['b']),Paragraph('Durum: mimari spesifikasyon. Native model inference, adapter parity, NMPC timing ve CARLA closed-loop sonuçları henüz doğrulanmadı. Dokümantasyon kontrolleri ayrı raporlanır.',S['b']),Spacer(1,20),Paragraph('Bu rapor Türkçe ayrıntılı teknik belgeleri birleştirir. GitHub README, İngilizce proje özeti ve kaynak haritasını sunar. Düzenlenebilir SVG/PDF şekiller, JSON kayıtları ve belge üretim araçları depoda yer alır.',S['b']),PageBreak()])
web.append('<header><img src="../assets/brand/repository_banner.svg" alt="τMOTION"><h1>Architecture Specification v1.1</h1><p>11 Kasım 2026 · Tasarım spesifikasyonu; runtime doğrulaması bekliyor.</p></header>')
web.append('<nav>'+''.join(f'<a href="#doc{i}">{html.escape(Path(p).stem)}</a> ' for i,p in enumerate(FILES))+'</nav>')
def table(lines,source):
    rows=[[x.strip() for x in l.strip().strip('|').split('|')] for l in lines]
    rows=[r for r in rows if not all(re.fullmatch(r'[-: ]+',x or '-') for x in r)]
    n=len(rows[0]);widths={2:[.27,.73],3:[.23,.36,.41],4:[.17,.29,.29,.25]}.get(n,[1/n]*n)
    if rows[0][0] in ['ID','Karar']:widths=[.09]+[.91/(n-1)]*(n-1)
    t=Table([[Paragraph(inline(x,source),S['cell']) for x in r] for r in rows],colWidths=[W*x for x in widths],repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dcebf2')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f7fa')]),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#c4d5df')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.extend([t,Spacer(1,10)])
    web.append('<div class="tablewrap"><table>'+''.join('<tr>'+''.join(f'<{"th" if i==0 else "td"}>{inline(x,source,True)}</{"th" if i==0 else "td"}>' for x in r)+'</tr>' for i,r in enumerate(rows))+'</table></div>')
for di,name in enumerate(FILES):
    if di:story.append(PageBreak())
    source=ROOT/name;lines=source.read_text().splitlines();i=0;web.append(f'<section id="doc{di}">')
    while i<len(lines):
        line=lines[i].strip()
        if not line or line.startswith('!['):i+=1;continue
        if line.startswith('|'):
            ls=[]
            while i<len(lines) and lines[i].strip().startswith('|'):ls.append(lines[i]);i+=1
            table(ls,source);continue
        if line.startswith('#'):
            level=len(line)-len(line.lstrip('#'));text=line[level:].strip()
            story.append(Paragraph(inline(text,source),S['h1' if level==1 else 'h2']))
            web.append(f'<h{min(level,3)}>{inline(text,source,True)}</h{min(level,3)}>')
        else:
            story.append(Paragraph(inline(line,source),S['b']));web.append('<p>'+inline(line,source,True)+'</p>')
        i+=1
    web.append('</section>')
    if name=='docs/architecture.md':
        for n,g in diagrams():
            story.extend([PageBreak(),Paragraph(n.replace('_',' ').title(),S['h1']),Drawing(g),Spacer(1,12),Paragraph('Bu şekil vektöreldir; tam boy SVG/PDF assets/diagrams klasöründe bulunur. Genel yöntem isimlerinin gerçek kaynakları bileşen kataloğunda belirtilir.',S['cap'])])
            web.append(f'<figure><img src="../assets/diagrams/{n}.svg" alt="{n}"></figure>')
    if name=='docs/brand.md':
        story.extend([PageBreak(),Paragraph('Convergent Tau — kimlik sistemi',S['h1']),Image(str(ROOT/'assets/brand/identity_board.png'),width=W,height=W*1300/1800)])
        web.append('<figure><img src="../assets/brand/identity_board.svg" alt="Brand identity"></figure>')
class Report(SimpleDocTemplate):
    def afterFlowable(self,f):
        if isinstance(f,Paragraph) and f.style.name in ['H1','H2']:
            key='section_'+str(getattr(self,'counter',0));self.counter=getattr(self,'counter',0)+1
            self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f.getPlainText(),key,0 if f.style.name=='H1' else 1,closed=True)
def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#c5d6df'));c.line(44,40,A4[0]-44,40);c.setFillColor(colors.HexColor('#60798d'));c.setFont('Brand',7)
    c.drawString(44,28,'τMOTION · Architecture Specification v1.1 · Runtime validation pending');c.drawRightString(A4[0]-44,28,str(d.page));c.restoreState()
doc=Report(str(OUT/'Architecture_Specification_v1.1.pdf'),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=42,bottomMargin=54,title='τMOTION — Architecture Specification v1.1',author='τMOTION research')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
css='body{font:16px/1.65 system-ui,sans-serif;color:#20394c;background:#f5f8fc;max-width:1180px;margin:auto;padding:28px}img{max-width:100%}h1,h2{line-height:1.3;color:#12344a}h2{margin-top:30px;color:#147b85}a{color:#087aa0}nav a{display:inline-block;margin:6px;font-size:12px}section{border-top:1px solid #c3d3df;padding-top:26px;margin-top:30px}table{border-collapse:collapse;font-size:13px;width:100%}th,td{padding:9px;border:1px solid #c3d3df;vertical-align:top}th{background:#dcebf2}.tablewrap{overflow-x:auto}figure{margin:35px 0}'
(OUT/'Architecture_Specification_v1.1.html').write_text('<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>τMOTION Architecture Specification v1.1</title><style>'+css+'</style>'+''.join(web)+'</html>')
cs=json.loads((ROOT/'specs/components.json').read_text())
with (ROOT/'specs/component_bom.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(cs[0]));w.writeheader();w.writerows(cs)
print(json.dumps({'documents':len(FILES),'components':len(cs),'report':'reports/Architecture_Specification_v1.1.pdf'}))
