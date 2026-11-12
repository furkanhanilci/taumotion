#!/usr/bin/env python3
"""Compile authoritative v1.3.1 final documented architecture into a readable PDF. Documentation only."""
from pathlib import Path
import html,re,json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_LEFT
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, LongTable, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
R=Path(__file__).resolve().parents[1]
OUT=R/'reports'/'TAUMOTION_Architecture_Specification_v1_3_1.pdf'
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
W=A4[0]-88
st={
 'title':ParagraphStyle('Title',fontName='DVB',fontSize=28,leading=38,textColor=colors.HexColor('#67259c'),spaceAfter=16),
 'sub':ParagraphStyle('Subtitle',fontName='DV',fontSize=12.5,leading=18,textColor=colors.HexColor('#525f75'),spaceAfter=14),
 'h1':ParagraphStyle('H1',fontName='DVB',fontSize=17,leading=22,spaceBefore=10,spaceAfter=13,textColor=colors.HexColor('#4d2182'),keepWithNext=True),
 'h2':ParagraphStyle('H2',fontName='DVB',fontSize=12.4,leading=16,spaceBefore=12,spaceAfter=7,textColor=colors.HexColor('#306186'),keepWithNext=True),
 'h3':ParagraphStyle('H3',fontName='DVB',fontSize=10.6,leading=14,spaceBefore=10,spaceAfter=6,textColor=colors.HexColor('#405576'),keepWithNext=True),
 'p':ParagraphStyle('Body',fontName='DV',fontSize=8.65,leading=12.4,spaceAfter=6,textColor=colors.HexColor('#1a3048')),
 'cell':ParagraphStyle('Cell',fontName='DV',fontSize=7.0,leading=9.75,textColor=colors.HexColor('#1a3048')),
 'small':ParagraphStyle('Small',fontName='DV',fontSize=7.5,leading=11,spaceAfter=8,textColor=colors.HexColor('#6b7792')),
 'code':ParagraphStyle('Code',fontName='DV',fontSize=7.6,leading=11,leftIndent=13,spaceAfter=3,textColor=colors.HexColor('#4b5970')),
}
def rich(t):
 s=html.escape(t)
 s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'`([^`]+)`',r'<font color="#6a3695">\1</font>',s)
 s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="#306186">\1</link>',s)
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1 (\2)',s)
 return s
files=[
('Nihai mimari / tam Türkçe ana anlatım','docs/FINAL_ARCHITECTURE_MASTER_TR.md'),
('Final architecture — English','docs/FINAL_ARCHITECTURE_MASTER_EN.md'),
('v1.3.1 değişiklik ve kararlar','docs/revisions-v1.3.md'),
('Hibrit E2E ve AutoE2E / klasik Autoware karşılaştırma','docs/autoware-and-hybrid-e2e-v1.3.md'),
('Kıyaslama potansiyeli ve yayımlanmış referanslar','docs/benchmark-expectations-v1.3.md'),
('Logo kilidi ve güncel marka kuralları','docs/brand-approved-v1.3.md'),
('Yayın öncesi ayrıntılı inceleme','docs/prepublication-review-v1.3.1.md'),
('Entegrasyon sözleşmesi','docs/integration-contract-v1.3.1.md'),
('Kaynak yeniden incelemesi','docs/source-audit-v1.3.1.md'),
('v1.2 Safety Critic teknik ayrıntıları','docs/safety-critic-and-supervision.md'),
('Görünürlük ve multi-target öğretmen eğitimi','docs/training-and-data-v1.2.md'),
('Bütün modül girdi/çıktı ve hata kataloğu','docs/components.md'),
('Arayüz ve veri tipleri','docs/interfaces.md'),
('Arayüz uzantıları v1.2','docs/interfaces-v1.2-addendum.md'),
('Korunan matematiksel yöntemler','docs/methods.md'),
('Eşzamanlama ve yürütme sözleşmesi','docs/runtime-contract.md'),
('Ölçütler ve deney tasarımı','docs/experiments.md'),
('E19-E24 deney uzantıları','docs/experiments-v1.2-addendum.md'),
('Kaynak kod kullanım ve lisans kayıtları','docs/reuse-register-v1.2.md'),
('Kaynak veri ayrıcalığı ve kanıt politikası','docs/evidence-policy.md'),
('Son görüşmeler ve tarihsel kayıtlar','history/README.md')]


story=[]
story.extend([Spacer(1,16),Image(str(R/'assets/brand/TAUMOTION_APPROVED_FINAL_LOGO_2026-11-12.png'),width=400,height=267),Spacer(1,14),Paragraph('τMOTION',st['title']),Paragraph('Final Hybrid E2E Architecture  v1.3.1',st['title']),Paragraph('Nihai araştırma mimarisi · 12 Kasım 2026',st['sub']),HRFlowable(width='100%',thickness=2,color=colors.HexColor('#8956bc')),Spacer(1,24),Paragraph('Explainable, Risk-Aware Hybrid End-to-End Driving | VLM + Grounding + Dual Planners + Safety Critic + RL + NMPC',st['sub']),Spacer(1,16),Paragraph('<b>Durum:</b> Nihai mimari tanımı ve araştırma spesifikasyonu. Bu belgenin tamamlanması için runtime testleri önkoşul değildir; yayımlanmış skorlar, koşullu mimari tahminleri ve gerçekleşmiş deneyler birbirinden ayrılır. Mevcut pakette τMOTION sürüş testi yapılmış olduğu iddia edilmez.',st['p']),Spacer(1,26),Paragraph('Son onaylı LiDARsız araç silüeti ile birleşik τMOTION logosu kaynak PNG dosyasından değiştirilmeden kullanılmıştır. Bilimsel modül çizimleri dış araştırma markalarını içermez; akademik atıflar burada açıkça korunur.',st['p']),Spacer(1,24),Paragraph('Bölümler',st['h2'])])
for i,(label,path) in enumerate(files,1):story.append(Paragraph(f'{i:02d}. {rich(label)}',st['p']))
story.extend([Spacer(1,16),Paragraph('Özgün arşivler ve birebir sohbetler yerel teslimde korunur. Git deposu mimari, kaynak kayıtları ve karar özetlerini taşır; docs/repository-publication.md yayın sınırını açıklar.',st['small']),PageBreak()])

def addtable(lines):
 rows=[]
 for l in lines:
  a=[x.strip() for x in l.strip().strip('|').split('|')]
  if all(re.fullmatch('[-: ]+',x or '-') for x in a):continue
  rows.append(a)
 if not rows:return
 n=max(len(x) for x in rows)
 # Some markdown lines with literal | may exceed 4; wrap still safe.
 widths=[1/n]*n
 if n==2:widths=[.29,.71]
 if n==3:widths=[.21,.37,.42]
 if n==4:widths=[.18,.25,.25,.32]
 if n==5:widths=[.14,.20,.21,.21,.24]
 tab=[[Paragraph(rich(x),st['cell']) for x in (r+['']*(n-len(r)))[:n]] for r in rows]
 table=LongTable(tab,colWidths=[W*x for x in widths],repeatRows=1,hAlign='LEFT',splitByRow=1)
 table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9e2f4')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f6f7fb')]),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#c7cbd8')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
 story.extend([table,Spacer(1,11)])

# Current figures; full-size vectors remain separately available.
for name,label in [('main_architecture','Çevrim içi mimari'),('runtime_contract','Çalışma zamanı ve komut sahipliği'),('learning_and_evidence','Eğitim ve kanıt olgunluğu')]:
 story.append(Paragraph(label,st['h1']))
 image_path=R/'assets/diagrams/v1_3_1'/(name+'.png')
 iw,ih=ImageReader(str(image_path)).getSize()
 story.append(Image(str(image_path),width=W,height=W*ih/iw))
 story.append(Paragraph('Tam boy SVG/PDF: assets/diagrams/v1_3_1/'+name+'; şema seçili akışları gösterir. Tüm 54 bağımlılık docs/dependency-graph.md içindedir.',st['small']))
 story.append(PageBreak())

for idx,(label,path) in enumerate(files):
 if idx: story.append(PageBreak())
 story.append(Paragraph(f'{idx+1:02d}  {rich(label)}',st['h1']))
 story.append(Paragraph(rich(path),st['small']))
 txt=(R/path).read_text(encoding='utf-8');ls=txt.splitlines();in_code=False;table=[]
 def flush():
  nonlocal_dummy=None
  if table:
   addtable(table);table.clear()
 for line in ls:
  s=line.strip()
  if s.startswith('```') or s.startswith('~~~'):
   flush();in_code=not in_code;continue
  if in_code:
   if s:story.append(Paragraph(rich(s),st['code']))
   continue
  if s.startswith('|'):
   table.append(s);continue
  flush()
  if not s:continue
  if s.startswith('!['):continue
  if s.startswith('#'):
   k=len(s)-len(s.lstrip('#'))
   name=s[k:].strip()
   story.append(Paragraph(rich(name),st['h2'] if k<=2 else st['h3']))
  elif s.startswith('- ') or s.startswith('* '):
   story.append(Paragraph('• '+rich(s[2:]),st['p']))
  elif re.match(r'^\d+\.\s',s):
   story.append(Paragraph(rich(s),st['p']))
  else:
   # Lines with raw markdown inline math or bare syntax render as text, no hidden data loss
   story.append(Paragraph(rich(s),st['p']))
 flush()

class Doc(SimpleDocTemplate):
 def afterFlowable(self,fl):
  if isinstance(fl,Paragraph) and fl.style.name in ('H1','H2'):
   n=getattr(self,'_outline',0);self._outline=n+1
   key=f'b{n}';self.canv.bookmarkPage(key)
   try:self.canv.addOutlineEntry(fl.getPlainText()[:120],key,0 if fl.style.name=='H1' else 1,closed=True)
   except Exception:pass

def footer(c,d):
 c.saveState();c.setStrokeColor(colors.HexColor('#dbc9eb'));c.line(44,43,A4[0]-44,43)
 c.setFont('DV',7.5);c.setFillColor(colors.HexColor('#666287'))
 c.drawString(44,29,'τMOTION v1.3.1 | Final architecture specification')
 c.drawRightString(A4[0]-44,29,str(d.page));c.restoreState()

report=Doc(str(OUT),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=46,bottomMargin=58,title='τMOTION — Final Hybrid End-to-End Architecture v1.3.1',author='τMOTION research specification')
report.build(story,onFirstPage=footer,onLaterPages=footer)
print('GENERATED',OUT,OUT.stat().st_size)
