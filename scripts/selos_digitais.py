CSS2 = """.sl{display:inline-flex;align-items:center;gap:.5em;height:2.4em;padding:0 .85em 0 .6em;border-radius:.6em;font-family:Outfit,Arboria,Arial,sans-serif;font-size:13px;font-weight:700;line-height:1;white-space:nowrap;box-sizing:border-box;border:1.5px solid currentColor;background:var(--bg);color:var(--fg);vertical-align:middle}
.sl svg{width:1.3em;height:1.3em;flex-shrink:0;display:block}
.sl .tb{font-size:.72em;font-weight:800;letter-spacing:.06em;padding:.3em .45em;border-radius:.35em;background:var(--fg);color:#fff;margin-left:.1em}
.sl.sm{font-size:11px;height:2.3em;padding:0 .7em 0 .5em}
.sl.ic{width:2.4em;padding:0;justify-content:center;border-radius:50%}
.sl.ic.sm{width:2.3em}
.sl.solid{background:var(--fg);color:#fff;border-color:var(--fg)}
.sl.solid .tb{background:#fff;color:var(--fg)}
.k-rg{--fg:#1F4E79;--bg:#E8F0F8}
.k-rep{--fg:#1F4E79;--bg:#E8F0F8}
.k-cons{--fg:#1E6B3A;--bg:#E8F4EC}
.k-reaf{--fg:#2F6B4F;--bg:#EAF4EF}
.k-sup{--fg:#B4470B;--bg:#FDF0E7}
.k-mod{--fg:#5B2490;--bg:#F3ECFA}
.k-contr{--fg:#8A5A00;--bg:#FFF6DC}
.k-div{--fg:#1F1F1F;--bg:#F1F1F1}
.k-fav{--fg:#1E6B3A;--bg:#E8F4EC}
.k-desf{--fg:#B42318;--bg:#FDECEA}
.k-ess{--fg:#7A5B00;--bg:#FFF4CC}
.k-novo{--fg:#1F4E79;--bg:#FFFFFF}
.k-pend{--fg:#475467;--bg:#F2F4F7}
.k-prova{--fg:#5B2490;--bg:#F3ECFA}
"""
def I(p): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
ICONS = {
'rg': I('<path d="M3 21h18M5 21V10M19 21V10M9.5 21V10M14.5 21V10M2.5 10 12 3.5 21.5 10z"></path>'),
'rep': I('<path d="M17 2.5 20.5 6 17 9.5"></path><path d="M3.5 11V9.5A3.5 3.5 0 0 1 7 6h13.5"></path><path d="M7 21.5 3.5 18 7 14.5"></path><path d="M20.5 13v1.5A3.5 3.5 0 0 1 17 18H3.5"></path>'),
'cons': I('<path d="M12 2.8l7.5 3v5.4c0 4.6-3.2 8.2-7.5 10-4.3-1.8-7.5-5.4-7.5-10V5.8z"></path><path d="M8.5 12.2l2.4 2.4 4.6-4.9"></path>'),
'reaf': I('<path d="M20.5 12a8.5 8.5 0 1 1-2.5-6"></path><path d="M20.5 3.5V8H16"></path><path d="M8.5 12.2l2.4 2.4 4.6-4.9"></path>'),
'sup': I('<path d="M4 7h11.5"></path><path d="M12 3.5 15.5 7 12 10.5"></path><path d="M20 17H8.5"></path><path d="M12 13.5 8.5 17 12 20.5"></path>'),
'mod': I('<rect x="3.5" y="4.5" width="17" height="16" rx="2"></rect><path d="M3.5 9.5h17M8 2.5v4M16 2.5v4M8 14.5h8"></path><path d="M13.5 12.5 16 14.5l-2.5 2"></path>'),
'contr': I('<path d="M12 21v-6.5M12 14.5 6 8.5M12 14.5l6-6"></path><circle cx="6" cy="6.5" r="2"></circle><circle cx="18" cy="6.5" r="2"></circle>'),
'div': I('<path d="M5 9h14M5 15h14M16 4.5 8 19.5"></path>'),
'fav': I('<path d="M3.5 17 9.5 11l4 4 7-7.5"></path><path d="M15.5 7.5h5v5"></path>'),
'desf': I('<path d="M3.5 7 9.5 13l4-4 7 7.5"></path><path d="M15.5 16.5h5v-5"></path>'),
'ess': '<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M12 3.2l2.6 5.5 6 .7-4.4 4.1 1.2 6-5.4-3-5.4 3 1.2-6-4.4-4.1 6-.7z"></path></svg>',
'novo': I('<circle cx="12" cy="12" r="8.5"></circle><path d="M12 8v8M8 12h8"></path>'),
'pend': I('<path d="M6.5 3h11M6.5 21h11M7.5 3v3.5L12 11l4.5-4.5V3M7.5 21v-3.5L12 13l4.5 4.5V21"></path>'),
'prova': I('<rect x="5" y="4" width="14" height="17" rx="2"></rect><path d="M9 2.5h6v3H9z"></path><path d="M8.8 13.2l2.2 2.2 4.2-4.4"></path>'),
}
DEF = [
 ('Força da decisão','Diz se a tese vincula os demais juízes e tribunais.',[
  ('rg','Repercussão geral','STF','Tema de repercussão geral julgado pelo STF. A tese vincula.'),
  ('rep','Recurso repetitivo','STJ','Tema repetitivo julgado pelo STJ. A tese vincula.')]),
 ('Situação do entendimento','Mostra se o julgado confirma, muda ou ainda divide a jurisprudência.',[
  ('cons','Entendimento consolidado',None,'Confirma jurisprudência já firme. Revisão rápida.'),
  ('reaf','Reafirmação de entendimento',None,'O tribunal reafirmou a posição que já tinha.'),
  ('sup','Superação de entendimento',None,'Mudou a jurisprudência. Atualize o material.'),
  ('mod','Modulação de efeitos',None,'A decisão vale a partir de uma data definida.'),
  ('contr','Entendimento controvertido',None,'Ainda não há posição pacífica no tribunal.'),
  ('div','Divergência STF e STJ',None,'Os dois tribunais decidem de forma diferente.')]),
 ('Impacto para a Fazenda Pública','O olhar da procuradoria sobre o resultado.',[
  ('fav','Favorável à Fazenda Pública',None,'Resultado favorável ao ente público.'),
  ('desf','Desfavorável à Fazenda Pública',None,'Resultado contrário ao ente público.')]),
 ('Novos selos sugeridos','Só fazem sentido no digital: viram filtro, alerta e trilha de estudo.',[
  ('ess','Essencial',None,'Entra no modo Essencial (a antiga Curadoria).'),
  ('novo','Tema novo',None,'Primeira vez que o tema aparece no JurisClub.'),
  ('pend','Julgamento não concluído',None,'Pedido de vista ou destaque. Avisamos quando terminar.'),
  ('prova','Já cobrado em prova',None,'O tema já caiu em concurso de procuradoria.')]),
]
def chip(k,label,trib,sm=False,solid=False,icon_only=False):
    cls='sl k-'+k+(' sm' if sm else '')+(' solid' if solid else '')+(' ic' if icon_only else '')
    aria=label+(f' ({trib})' if trib else '')
    if icon_only:
        return f'<span class="{cls}" role="img" aria-label="{aria}" title="{aria}">{ICONS[k]}</span>'
    tb=f'<span class="tb">{trib}</span>' if trib else ''
    return f'<span class="{cls}" role="img" aria-label="{aria}">{ICONS[k]}<span>{label}</span>{tb}</span>'
