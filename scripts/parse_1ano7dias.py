import re, json, sys
from docx import Document
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def runs(p):
    out=[]
    for r in p.iter(W+'r'):
        t=''.join((x.text or '') if x.tag==W+'t' else ('\t' if x.tag==W+'tab' else '') for x in r)
        if not t: continue
        rp=r.find(W+'rPr')
        def on(tag):
            if rp is None: return False
            e=rp.find(W+tag); return e is not None and e.get(W+'val') not in ('0','false')
        col=rp.find(W+'color') if rp is not None else None
        pur=col is not None and (col.get(W+'val') or '').upper()=='7030A0'
        fl=(1 if on('b') else 0)|(2 if on('i') else 0)|(4 if on('u') else 0)|(8 if pur else 0)
        if out and out[-1][1]==fl: out[-1][0]+=t
        else: out.append([t,fl])
    return out
def style(p):
    s=p.find(W+'pPr/'+W+'pStyle'); return s.get(W+'val') if s is not None else ''
def blocks(path):
    doc=Document(path); out=[]
    for el in doc.element.body.iterchildren():
        if el.tag==W+'p':
            rr=runs(el); t=''.join(x[0] for x in rr).strip()
            if not t: continue
            out.append({'k':'p','st':style(el),'r':rr,'t':t})
        elif el.tag==W+'tbl':
            fill=None
            for s in el.iter(W+'shd'):
                f=s.get(W+'fill')
                if f and f not in('auto','FFFFFF'): fill=f; break
            ps=[]
            for p in el.iter(W+'p'):
                rr=runs(p)
                if ''.join(x[0] for x in rr).strip(): ps.append(rr)
            if ps: out.append({'k':'tese' if fill else 'cit','fill':fill,'ps':ps})
    return out
SELOS={'favorável à fazenda pública':'fav','desfavorável à fazenda pública':'desf','repercussão geral':'rg','recurso repetitivo':'rep','entendimento consolidado':'cons','reafirmação de entendimento':'reaf','superação de entendimento':'sup','modulação de efeitos':'mod','entendimento controvertido':'contr','divergência stf e stj':'div'}
def material(path):
    B=blocks(path); title=None; temas=[]; cur=None
    for b in B:
        if b['k']=='p':
            if 'SUBT' in b['st'].upper() or 'SUB' in b['st'].upper():
                if title is None: title=b['t']; continue
                cur={'nome':b['t'],'selos':[],'blocos':[]}; temas.append(cur); continue
            if b['t'].startswith('<') and b['t'].endswith('>') and cur is not None:
                for x in re.findall(r'<\s*([^<>]+?)\s*>',b['t']): cur['selos'].append(SELOS.get(x.lower(),x))
                continue
            allb=all(r[1]&1 for r in b['r'] if r[0].strip())
            if allb and len(b['t'])<140 and not b['t'].startswith('“'):
                cur['blocos'].append({'k':'h','t':b['t']}); continue
            cur['blocos'].append({'k':'p','r':b['r']})
        else:
            cur['blocos'].append({'k':b['k'],'fill':b['fill'],'ps':b['ps']})
    return {'titulo':title,'temas':temas}
def questoes(path):
    B=blocks(path); qs=[]; q=None; mode=None
    for b in B:
        t=b.get('t','')
        if b['k']=='p':
            m=re.match(r'^(\d{1,2})\)\s*',t)
            if m and (q is None or mode=='fim'):
                q={'n':int(m.group(1)),'enun':b['r'],'alts':[],'meta':{},'com':[],'altc':{},'gab':None}; qs.append(q); mode='alts'
                # strip number from first run
                q['enun']=[list(x) for x in b['r']]
                continue
            if mode=='alts':
                m=re.match(r'^([A-E])\)\s*(.*)$',t)
                if m: q['alts'].append({'l':m.group(1),'r':b['r']}); continue
            m=re.match(r'^(Assunto Geral|Assunto Principal|Assunto Específico|Categoria|Nível):\s*(.*)$',t)
            if m: q['meta'][m.group(1).replace('Principal','Geral')]=m.group(2).strip(); mode='meta'; continue
            if t.upper().startswith('COMENTÁRIOS'): mode='com'; continue
            m=re.match(r'^([A-E])\)\s*(CORRETA|INCORRETA)\.?\s*(.*)$',t)
            if m and mode in('com','alt'):
                cur={'l':m.group(1),'ok':m.group(2)=='CORRETA','b':[]}; q['altc'][m.group(1)]=cur; mode='alt'
                if m.group(3): cur['b'].append({'k':'p','r':[[m.group(3),0]]})
                continue
            m=re.match(r'^GABARITO:\s*LETRA\s*([A-E])',t)
            if m: q['gab']=m.group(1); mode='fim'; continue
            blk={'k':'p','r':b['r']}
        else:
            blk={'k':b['k'],'fill':b['fill'],'ps':b['ps']}
        if mode=='com': q['com'].append(blk)
        elif mode=='alt': cur['b'].append(blk)
        elif mode=='alts' and q['alts']:
            q['alts'][-1]['r']+= [[' ',0]]+b['r'] if b['k']=='p' else []
    return qs
if __name__=='__main__':
    m=material(sys.argv[1]); q=questoes(sys.argv[2])
    print(m['titulo'], len(m['temas']))
    for t in m['temas']: print(' ',t['nome'],t['selos'],[b['k'] for b in t['blocos']][:30])
    print(len(q))
    for x in q: print(x['n'],len(x['alts']),x['meta'],len(x['com']),sorted(x['altc']),x['gab'])
    json.dump({'material':m,'questoes':q},open(sys.argv[3],'w'),ensure_ascii=False,separators=(',',':'))

# ---------- HTML (exportação do Word) ----------
from html.parser import HTMLParser
import html as _html
def _style(s):
    d={}
    for part in (s or '').split(';'):
        if ':' in part:
            k,v=part.split(':',1); d[k.strip().lower()]=v.strip()
    return d
class _H(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out=[]; self.stack=[]; self.cur=None; self.tbl=None; self.cell_fill=None; self.pstyle={}
    def _flags(self):
        fl=0
        for st in self.stack:
            if st.get('font-weight') in ('700','bold'): fl|=1
            if st.get('font-style')=='italic': fl|=2
            if 'underline' in st.get('text-decoration',''): fl|=4
            if st.get('color','').upper()=='#7030A0': fl|=8
        return fl
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); st=_style(a.get('style'))
        if tag=='table': self.tbl={'fill':None,'ps':[]}
        elif tag=='td' and self.tbl is not None:
            if st.get('background-color'): self.tbl['fill']=st['background-color'].lstrip('#').upper()
        elif tag=='p':
            self.cur=[]; self.pstyle=st
        elif tag=='br':
            if self.cur is not None: self._endp(keep=True)
        if tag in('span','b','strong','i','em','u','p'):
            if tag in('b','strong'): st['font-weight']='700'
            if tag in('i','em'): st['font-style']='italic'
            if tag=='u': st['text-decoration']='underline'
            self.stack.append(st)
    def handle_endtag(self,tag):
        if tag in('span','b','strong','i','em','u','p') and self.stack: self.stack.pop()
        if tag=='p' and self.cur is not None: self._endp()
        if tag=='table' and self.tbl is not None:
            if self.tbl['ps']: self.out.append({'k':'tese' if self.tbl['fill'] else 'cit','fill':self.tbl['fill'],'ps':self.tbl['ps']})
            self.tbl=None
    def _endp(self,keep=False):
        rr=self.cur; t=''.join(x[0] for x in rr).replace('\xa0',' ').strip()
        if t:
            rr=[[x[0].replace('\xa0',' '),x[1]] for x in rr]
            if self.tbl is not None: self.tbl['ps'].append(rr)
            else:
                big=False
                for stl in [self.pstyle]+self.stack:
                    pass
                self.out.append({'k':'p','st':'SUBT' if self._big else '','r':rr,'t':t})
        self.cur=[] if keep else None; self._big=False
    _big=False
    def handle_data(self,data):
        if self.cur is None: return
        if not data: return
        st=self.stack[-1] if self.stack else {}
        fs=st.get('font-size','')
        if fs.endswith('pt') and float(fs[:-2])>=15: self._big=True
        fl=self._flags()
        if self.cur and self.cur[-1][1]==fl: self.cur[-1][0]+=data
        else: self.cur.append([data,fl])
def blocks_html(path):
    h=_H(); h.feed(open(path,encoding='utf-8').read()); return h.out
_blocks_docx=blocks
def blocks(path):
    return blocks_html(path) if path.lower().endswith(('.html','.htm')) else _blocks_docx(path)
