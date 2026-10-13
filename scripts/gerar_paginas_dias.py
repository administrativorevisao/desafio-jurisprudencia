import json, re, sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/b59ab43a-0ca2-5b61-bced-286e816ffb35/scratchpad/jc-canvas/tags')
sys.path.insert(0,'/tmp/claude-0/-home-claude/b59ab43a-0ca2-5b61-bced-286e816ffb35/scratchpad/tools')
from tags2 import chip
import parse_dia as P
BASE='/tmp/claude-0/-home-claude/b59ab43a-0ca2-5b61-bced-286e816ffb35/scratchpad/'
PROJ=BASE+'jc-canvas/project/'
src=open(BASE+'jc-canvas/_dia_template.html').read()
NAMES={'rg':('Repercussão geral','STF'),'rep':('Recurso repetitivo','STJ'),'cons':('Entendimento consolidado',None),'reaf':('Reafirmação de entendimento',None),'sup':('Superação de entendimento',None),'mod':('Modulação de efeitos',None),'contr':('Entendimento controvertido',None),'div':('Divergência STF e STJ',None),'fav':('Favorável à Fazenda Pública',None),'desf':('Desfavorável à Fazenda Pública',None)}
def sel_html(prefix, sm):
    return ''.join(f'<sc-if value="{{{{{prefix}.s_{k}}}}}" hint-placeholder-val="{{{{ false }}}}">{chip(k,n,t,sm=sm)}</sc-if>' for k,(n,t) in NAMES.items())
s=src
# selos sidebar (one line with 4 sc-ifs) and tema (4 lines)
s=re.sub(r'(<sc-if value="\{\{t\.s_fav\}\}".*?)(\n<span style="font-size: 12px; color: #5B5872; font-weight: 600">\{\{t\.nq\}\}</span>)', lambda m: sel_html('t',True)+m.group(2), s, count=1, flags=re.S)
s=re.sub(r'<sc-if value="\{\{tema\.s_fav\}\}".*?<sc-if value="\{\{tema\.s_cons\}\}".*?</sc-if>', lambda m: sel_html('tema',False), s, count=1, flags=re.S)
assert s.count('k-mod')>=2, 'selos'
s=s.replace('<h1 style="margin: 0; font-size: 42px; line-height: 1.05; font-weight: 900; letter-spacing: -.02em">Dia 01 · Direito Administrativo</h1>','<h1 style="margin: 0; font-size: 42px; line-height: 1.05; font-weight: 900; letter-spacing: -.02em">{{titulo}}</h1>')
s=s.replace('<span style="font-size: 15px; color: #D9D2F5">7 temas · 10 questões comentadas</span>','<span style="font-size: 15px; color: #D9D2F5">{{subt}}</span>')
s=s.replace('<span style="{{d.st}}" aria-current="{{d.cur}}"><span style="font-size: 11px; font-weight: 600; opacity: .8">Dia</span><span style="font-size: 18px; font-weight: 800; line-height: 1">{{d.n}}</span></span>',
 '<sc-if value="{{d.ok}}" hint-placeholder-val="{{ true }}"><a href="{{d.href}}" style="{{d.st}}" aria-current="{{d.cur}}" aria-label="Dia {{d.n}}"><span style="font-size: 11px; font-weight: 600; opacity: .8">Dia</span><span style="font-size: 18px; font-weight: 800; line-height: 1">{{d.n}}</span></a></sc-if><sc-if value="{{d.no}}" hint-placeholder-val="{{ false }}"><span style="{{d.st}}" aria-label="Dia {{d.n}} em breve"><span style="font-size: 11px; font-weight: 600; opacity: .8">Dia</span><span style="font-size: 18px; font-weight: 800; line-height: 1">{{d.n}}</span></span></sc-if>')
s=s.replace('Caderno de questões · {{acertos}}/10</button>','Caderno de questões · {{qLabel}}</button>')
a=s.index('<div style="margin-top: 22px; padding: 20px 22px; border-radius: 12px; background: #F1EAFE')
b=s.index('</div>',s.index('{{tema.irQ}}'))+len('</div>')
s=s[:a]+'<sc-if value="{{tema.temQ}}" hint-placeholder-val="{{ true }}">'+s[a:b]+'</sc-if>'+s[b:]
s=s.replace('<sc-if value="{{isQ}}" hint-placeholder-val="{{ false }}">','''<sc-if value="{{isQvazio}}" hint-placeholder-val="{{ false }}">
<main style="max-width: 1320px; margin: 0 auto; padding: 48px 32px 80px"><div style="max-width: 640px; margin: 0 auto; background: #fff; border: 1px solid #E3E0F0; border-radius: 14px; padding: 36px; text-align: center; display: flex; flex-direction: column; gap: 10px; align-items: center"><span style="font-size: 20px; font-weight: 800; color: #3D0A87">Caderno de questões em breve</span><span style="font-size: 15px; line-height: 1.6; color: #4A475F">As questões deste dia ainda não foram publicadas. Quando o caderno chegar, ele aparece aqui ligado aos temas do material.</span><button type="button" onClick="{{goMat}}" style="margin-top: 6px; min-height: 46px; padding: 0 20px; border: 0; border-radius: 10px; background: #7703DD; color: #fff; font-family: Outfit, Arboria, sans-serif; font-weight: 700; font-size: 15px; cursor: pointer">Voltar ao material</button></div></main>
</sc-if>
<sc-if value="{{isQ}}" hint-placeholder-val="{{ false }}">''',1)
# JS patches
s=s.replace("const dias = [1, 2, 3, 4, 5, 6, 7].map((n) => ({ n: String(n).padStart(2, '0'), cur: n === 1 ? 'page' : 'false',\n      st: 'display: flex; flex-direction: column; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 12px; ' + (n === 1 ? 'background: #7703DD; color: #fff; box-shadow: 0 0 0 2px #B79CFF' : 'background: rgba(255,255,255,.06); color: #8E86B5; border: 1px dashed rgba(255,255,255,.25)') }));",
"const dias = [1, 2, 3, 4, 5, 6, 7].map((n) => { const ok = DISP.includes(n); const cur = n === DIA; return { n: String(n).padStart(2, '0'), ok, no: !ok, href: 'Dia' + String(n).padStart(2, '0') + '.dc.html', cur: cur ? 'page' : 'false',\n      st: 'display: flex; flex-direction: column; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 12px; text-decoration: none; ' + (cur ? 'background: #7703DD; color: #fff; box-shadow: 0 0 0 2px #B79CFF' : ok ? 'background: rgba(255,255,255,.12); color: #fff; border: 1px solid rgba(255,255,255,.35)' : 'background: rgba(255,255,255,.06); color: #8E86B5; border: 1px dashed rgba(255,255,255,.25)') }; });")
assert 'DISP.includes' in s
s=s.replace("return { num: String(i + 1).padStart(2, '0'), nome: temaCurto(t.nome), s_fav: t.selos.includes('fav'), s_desf: t.selos.includes('desf'), s_reaf: t.selos.includes('reaf'), s_cons: t.selos.includes('cons'),",
            "return { num: String(i + 1).padStart(2, '0'), nome: temaCurto(t.nome), ...SEL(t.selos),")
s=s.replace("nq: qPorTema[i] + (qPorTema[i] === 1 ? ' questão' : ' questões'),","nq: qs.length ? qPorTema[i] + (qPorTema[i] === 1 ? ' questão' : ' questões') : '',")
s=s.replace("const tema = { nome: T.nome, s_fav: T.selos.includes('fav'), s_desf: T.selos.includes('desf'), s_reaf: T.selos.includes('reaf'), s_cons: T.selos.includes('cons'),",
            "const tema = { nome: T.nome, ...SEL(T.selos), temQ: nq > 0,")
assert s.count('SEL(')==2, s.count('SEL(')
s=s.replace("const Q = lista[pos] || { ...qs[0], i: 0 };","const Q = lista[pos] || (qs[0] ? { ...qs[0], i: 0 } : { n: 0, alts: [], meta: {}, com: [], altc: {}, gab: '', temas: [], enun: [], i: 0 });")
s=s.replace("dias, isMat: s.tab === 'mat', isQ: s.tab === 'q',","dias, isMat: s.tab === 'mat', isQ: s.tab === 'q' && qs.length > 0, isQvazio: s.tab === 'q' && qs.length === 0,\n      titulo: TITULO, subt: temas.length + ' temas' + (qs.length ? ' · ' + qs.length + ' questões comentadas' : ' · caderno de questões em breve'), qLabel: qs.length ? acertos + '/' + qs.length : 'em breve',")
s=s.replace("const temaCurto = ","const SEL = (arr) => { const o = {}; ['rg','rep','cons','reaf','sup','mod','contr','div','fav','desf'].forEach((k) => { o['s_' + k] = arr.includes(k); }); return o; };\nconst temaCurto = ")
s=s.replace("<title>1 Ano em 7 Dias · Dia 01</title>","<title>1 Ano em 7 Dias · @@TITLE@@</title>")
s=re.sub(r'const D = \{.*?\};\n', 'const D = @@DATA@@;\nconst DIA = @@DIA@@;\nconst DISP = @@DISP@@;\nconst TITULO = @@TITULO@@;\n', s, count=1, flags=re.S)
assert '@@DATA@@' in s and '@@TITLE@@' in s
def titulo(raw,n):
    rest=re.sub(r'^DIA\s*\d+\s*[-–—]\s*','',raw).strip()
    small={'e','de','do','da','dos','das'}
    words=rest.lower().split()
    out=[]
    for i,w in enumerate(words):
        core=w.strip('()')
        c=core if (core in small and i>0) else core[:1].upper()+core[1:]
        out.append(w.replace(core,c))
    return 'Dia %02d · %s'%(n,' '.join(out))
DAYS={1:('dia01/in/adm.docx','dia01/in/q.docx'),2:('dias/in/d02.html',None),3:('dias/in/d03.docx',None),4:('dias/in/d04.html',None)}
disp=sorted(DAYS)
for n,(mat,q) in DAYS.items():
    m=P.material(BASE+mat)
    if q:
        d=json.load(open(BASE+'dia01/dia01.json'))
        qs=d['questoes']
    else: qs=[]
    data={'material':m,'questoes':qs}
    js=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace(' ',' ').replace(' ',' ').replace('</','<\\/')
    t=titulo(m['titulo'],n)
    out=s.replace('@@DATA@@',js).replace('@@DIA@@',str(n)).replace('@@DISP@@',json.dumps(disp)).replace('@@TITULO@@',json.dumps(t,ensure_ascii=False)).replace('@@TITLE@@','Dia %02d'%n)
    open(PROJ+'Dia%02d.dc.html'%n,'w').write(out)
    print(n,t,len(m['temas']),len(qs),len(out))
