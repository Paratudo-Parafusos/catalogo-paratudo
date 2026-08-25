# -*- coding: utf-8 -*-
"""Gera o Catálogo de Linhas (simplificado) da Paratudo.

Lê tools/dados_simplificado.py + tools/fotos_docx/ e monta
simplificado/index.html — um arquivo só, com tudo embutido, que serve
pra web e pra imprimir (Ctrl+P → PDF A4).
"""
import base64, io, os, sys
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from dados_simplificado import (SECOES, VONIXX, TINTAS, ESCADAS, PARAFUSOS,
                                MARCAS_PARCEIRAS, CONTATO, PAGINAS)

FOTOS = os.path.join(AQUI, 'fotos_docx')
OUT_DIR = os.path.join(os.path.dirname(AQUI), 'simplificado')
ANO = '2026'

# ---------------------------------------------------------------- util
_cache = {}
def foto(n, maxpx=420, q=84):
    key = (n, maxpx)
    if key in _cache:
        return _cache[key]
    im = Image.open(os.path.join(FOTOS, f'{n}.jpg'))
    im.thumbnail((maxpx, maxpx), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q)
    uri = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    _cache[key] = uri
    return uri

def logo_uri():
    im = Image.open(os.path.join(AQUI, 'logo_full_q.png')).convert('RGB')
    im.thumbnail((900, 900), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

# ------------------------------------------------------------- ícones
IC = {
 'chave': '<path d="M14.5 6.5a4 4 0 0 0-5.6 4.9L4 16.3a2 2 0 1 0 2.8 2.8l4.9-4.9a4 4 0 0 0 4.9-5.6l-2.6 2.6-2.1-2.1 2.6-2.6z"/>',
 'serra': '<circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="1.6"/><path d="M12 5V2M19 12h3M12 19v3M5 12H2"/>',
 'disco': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2.5"/>',
 'bateria': '<rect x="3" y="8" width="15" height="9" rx="1"/><path d="M18 10.5h3v4h-3M9.5 10l-2 3h3l-2 3"/>',
 'plugue': '<path d="M9 3v5M15 3v5M7 8h10v3a5 5 0 0 1-10 0zM12 16v5"/>',
 'paquimetro': '<path d="M3 6h18M3 6v6l4 1V6M13 6v4l3 1V6M3 17h18"/>',
 'solda': '<path d="M4 20l8-8M12 12l3 3M14 5l5 5M17 3l4 4M12 8l1.5-1.5M16 12l1.5-1.5"/>',
 'ar': '<path d="M3 8h11a2.5 2.5 0 1 0-2.5-2.5M3 13h15a2.5 2.5 0 1 1-2.5 2.5M3 18h8"/>',
 'compressor': '<circle cx="10" cy="10" r="5.5"/><path d="M10 15.5V19M4 19h12M15.5 10H21M21 7v6"/>',
 'pintura': '<rect x="7" y="8" width="8" height="13" rx="1"/><path d="M9 8V5h4v3M15 3h4M17.5 5.5l2-2"/>',
 'macaco': '<path d="M4 19h16M6 19l6-9 6 9M12 10V6M9 6h6"/>',
 'paleteira': '<path d="M3 15h15M5 15V6h3v9M20 15V9h-2"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/>',
 'caixa': '<rect x="4" y="8" width="16" height="12" rx="1"/><path d="M4 12h16M9 8V5h6v3"/>',
 'oleo': '<path d="M12 3s6 7 6 11.5a6 6 0 0 1-12 0C6 10 12 3 12 3z"/>',
 'engrenagem': '<circle cx="12" cy="12" r="4.5"/><path d="M12 4v3M12 17v3M4 12h3M17 12h3M6.3 6.3l2.1 2.1M15.6 15.6l2.1 2.1M17.7 6.3l-2.1 2.1M8.4 15.6l-2.1 2.1"/>',
 'jato': '<path d="M3 12h9M12 8l8 4-8 4zM5 8V6M5 18v-2"/>',
 'quimico': '<path d="M10 3h4M11 3v6l-6 10a1.5 1.5 0 0 0 1.3 2.2h11.4A1.5 1.5 0 0 0 19 19L13 9V3"/>',
 'fita': '<circle cx="10" cy="10" r="6.5"/><circle cx="10" cy="10" r="2.3"/><path d="M15 15l6 5h-8"/>',
 'capacete': '<path d="M4 15a8 8 0 0 1 16 0M2.5 15h19M12 7V4"/>',
 'cadeado': '<rect x="5.5" y="11" width="13" height="9" rx="1.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 'folha': '<path d="M5 20C5 10 12 4 20 4c0 9-6 15-14 15M5 20c2-5 6-9 10-11"/>',
 'tijolo': '<rect x="3" y="6" width="18" height="12"/><path d="M3 12h18M9 6v6M15 12v6"/>',
 'suporte': '<path d="M5 4v16h14M5 9h7v6"/>',
 'raio': '<path d="M13 2L5 13h6l-1 9 8-11h-6z"/>',
 'parafuso': '<path d="M12 3l4 2.3v4.6L12 12 8 9.9V5.3zM12 12v9M9.5 14.5l5-1.4M9.5 17.5l5-1.4"/>',
}
def icone(k, cls=''):
    return (f'<svg viewBox="0 0 24 24" class="{cls}" fill="none" '
            f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
            f'stroke-linejoin="round">{IC.get(k, IC["chave"])}</svg>')

HEXB = '<span class="hexb"></span>'

# ------------------------------------------------------- páginas base
def pg(cls, inner, num=None):
    n = f'<div class="pgnum">{num:02d}</div>' if num else ''
    return f'<div class="pageframe"><div class="pagescale"><div class="page {cls}">{inner}{n}</div></div></div>'

def rodape_secao(marcas, num):
    m = ''.join(f'<span>{x}</span>' for x in marcas)
    return (f'<div class="cat-foot"><div class="marcas">{m}</div>'
            f'<div class="pgchip">{num:02d}</div></div>')

def header_secao(sec, slim=False):
    return (f'<div class="cat-head{" slim" if slim else ""}">'
            f'<div class="cat-ico">{icone(sec["icone"])}</div>'
            f'<h2>{sec["nome"]}</h2></div><div class="cat-rule"></div>')

def celulas(sec):
    linhas = sec['linhas']
    denso = sec.get('denso')
    cols = 5 if denso else 4
    # célula larga na 1ª e última linha quando sobra resto na grade
    resto = len(linhas) % cols
    wides = set()
    if not denso and resto:
        sobra = cols - resto           # células extras necessárias
        if sobra >= 1:
            wides.add(0)
        if sobra >= 2:
            wides.add(len(linhas) - 1)
    out = []
    for i, (nome, fotos) in enumerate(linhas):
        w = ' wide' if i in wides else ''
        out.append(f'<figure class="cell{w}"><div class="ph">'
                   f'<img src="{foto(fotos[0])}" alt="{nome}"></div>'
                   f'<figcaption>{nome}</figcaption></figure>')
    return (f'<div class="grid{" g5" if denso else ""}">{"".join(out)}</div>')

def pagina_secoes(ids, num):
    blocos = []
    marcas = []
    for i, sid in enumerate(ids):
        sec = SECOES[sid]
        blocos.append(header_secao(sec, slim=(len(ids) > 1)))
        if sec.get('chamada'):
            blocos.append(f'<div class="entrega luz chamada">{HEXB}'
                          f'<b>{sec["chamada"]}</b></div>')
        blocos.append(celulas(sec))
        marcas += [m for m in sec['marcas'] if m not in marcas]
    inner = ''.join(blocos) + rodape_secao(marcas[:6], num)
    return pg('cat', inner)

# ----------------------------------------------------------- especiais
def pagina_capa(num):
    idx = ''.join(f'<li>{HEXB}{SECOES[s]["nome"]}</li>'
                  for s in ['manuais', 'corte', 'abrasivos', 'bateria',
                            'eletricas', 'medicao', 'solda', 'pneumaticas',
                            'compressores', 'pintura', 'hidraulicos', 'cargas',
                            'armazenamento', 'maquinas', 'adesivos', 'epi',
                            'jardinagem', 'construcao', 'eletrica'])
    idx += f'<li>{HEXB}Parafusos e Cabos de Aço</li>'
    mosaico = ''.join(f'<div class="mtile"><img src="{foto(n)}" alt=""></div>'
                      for n in [76, 2, 52, 130, 310, 210])
    return pg('capa', f'''
    <div class="slab"></div>
    <div class="capa-top"><div class="logopanel"><img src="{logo_uri()}" alt="Paratudo"></div></div>
    <div class="capa-title">
      <div class="kicker">Paratudo Parafusos e Ferramentas</div>
      <h2>Catálogo<br>de Linhas <span>{ANO}</span></h2>
      <p class="sub">Ferramentas, parafusos, EPIs e suprimentos — tudo o que a
      sua obra, oficina ou indústria precisa, em um lugar só.</p>
    </div>
    <div class="capa-mid">
      <div class="indice"><h3>O que você encontra</h3><ul>{idx}</ul></div>
      <div class="mosaico">{mosaico}</div>
    </div>
    <div class="entrega">{HEXB}<b>{CONTATO["entrega"]}</b><span>{CONTATO["entrega_obs"]}</span></div>
    <div class="capa-foot"><span class="fone">{CONTATO["fones"]}</span><span class="site">{CONTATO["cidade"]}</span></div>''')

def pagina_apresentacao(num):
    wpp = 'https://wa.me/5535997580912'
    cards = f'''
    <div class="atend">
      <div class="acard">{icone('chave','aic')}<h4>Balcão</h4>
        <p>Atendimento direto na loja, com quem entende do assunto.
        Peça pelo nome, pela medida ou leve o exemplo — a gente acha.</p></div>
      <div class="acard">{icone('raio','aic')}<h4>WhatsApp</h4>
        <p>Orçamento rápido sem sair da obra:
        <a href="{wpp}"><b>(35) 9.9758-0912</b></a>.
        Manda a foto ou a lista, que a gente cota e separa.</p></div>
      <div class="acard">{icone('caixa','aic')}<h4>Empresas</h4>
        <p>Fornecimento pra indústrias, construtoras e oficinas da região,
        com cotação por lista e entrega programada.</p></div>
    </div>'''
    return pg('apres', f'''
    <div class="ap-band"><div class="kicker">Quem somos</div>
      <h2>A loja que tem<br><span>para tudo</span></h2></div>
    <div class="ap-body">
      <p class="lead">A <b>Paratudo Parafusos e Ferramentas</b> é a parceira de
      quem constrói, conserta e produz em Pouso Alegre e região: ferramentas,
      fixadores, EPIs e suprimentos industriais das marcas que o profissional
      confia, com estoque de verdade e atendimento que resolve.</p>
      <h3 class="ap-sec">{HEXB}Como você prefere comprar</h3>
      {cards}
      <div class="entrega luz">{HEXB}<b>{CONTATO["entrega"]}</b><span>{CONTATO["entrega_obs"]}</span></div>
    </div>
    <div class="capa-foot"><span class="fone">{CONTATO["fones"]}</span><span class="site">{CONTATO["cidade"]}</span></div>''', num)

def pagina_marcas(num):
    chips = ''.join(f'<span class="mchip">{m}</span>' for m in MARCAS_PARCEIRAS)
    return pg('marcaspg', f'''
    <div class="ap-band"><div class="kicker">Marcas parceiras</div>
      <h2>As marcas que o<br><span>profissional confia</span></h2></div>
    <div class="mwall">{chips}</div>
    <p class="mnota">Estas e muitas outras — o estoque completo você confere
    na loja ou no WhatsApp.</p>''', num)

def pagina_destaques(num):
    vx = ''.join(f'<div class="dph"><img src="{foto(n)}" alt=""></div>' for n in VONIXX['fotos'])
    tn = ''.join(
        f'<div class="tcard"><div class="tph"><img src="{foto(f[0])}" alt=""></div>'
        f'<h5>{t}</h5><p>{d}</p></div>'
        for t, d, f in TINTAS['chamadas'])
    es = ''.join(f'<figure class="dcell"><div class="dph"><img src="{foto(n)}" alt=""></div></figure>'
                 for n in ESCADAS['fotos'])
    return pg('dark destq', f'''
    <div class="dk-head"><div class="kicker">Destaque</div>
      <h2>{VONIXX['titulo']}</h2>
      <p class="sub">{VONIXX['texto']}</p></div>
    <div class="vx-band">{vx}<div class="vx-selo">Linha completa<br>na loja</div></div>
    <div class="dk-sec"><h3>{HEXB}{ESCADAS['titulo']} — {ESCADAS['marca']}</h3>
      <p class="dk-nota">{ESCADAS['texto']}</p>
      <div class="dgrid4">{es}</div></div>
    <div class="dk-sec"><h3>{HEXB}{TINTAS['titulo']}</h3>
      <div class="tintas">{tn}</div></div>''', num)

def pagina_parafusos(num):
    chips = ''.join(f'<span class="chip">{c}</span>' for c in PARAFUSOS['chips'])
    fx = ''.join(f'<figure class="dcell"><div class="dph"><img src="{foto(f[0])}" alt=""></div>'
                 f'<figcaption>{n}</figcaption></figure>' for n, f in PARAFUSOS['fixacao'])
    cb = ''.join(f'<figure class="dcell"><div class="dph"><img src="{foto(f[0])}" alt=""></div>'
                 f'<figcaption>{n}</figcaption></figure>' for n, f in PARAFUSOS['cabos'])
    return pg('dark', f'''
    <div class="dk-head"><div class="kicker">{PARAFUSOS['kicker']}</div>
      <h2>Parafusos <span>&amp;</span><br>Cabos de Aço</h2>
      <p class="sub">{PARAFUSOS['texto']}</p></div>
    <div class="chips">{chips}</div>
    <div class="dk-sec"><h3>{HEXB}Linhas de fixação</h3><div class="dgrid4">{fx}</div></div>
    <div class="dk-sec"><h3>{HEXB}Cabos de aço e acessórios</h3><div class="dgrid6">{cb}</div></div>
    <div class="dk-foot"><span class="frase">{PARAFUSOS['frase']}</span>
      <span class="fone">(35) 3427-2450</span></div>''')

def pagina_contracapa(num):
    chips = ''.join(f'<span class="mchip esc">{m}</span>' for m in MARCAS_PARCEIRAS[:36])
    return pg('dark contra', f'''
    <div class="ct-logo"><div class="logopanel"><img src="{logo_uri()}" alt="Paratudo"></div></div>
    <div class="ct-marcas">{chips}</div>
    <div class="dk-sec"><h3>{HEXB}Fale com a gente</h3></div>
    <div class="ct-info">
      <div><h5>Telefones</h5><p>{CONTATO['fones']}</p></div>
      <div><h5>Onde</h5><p>{CONTATO['cidade']}</p></div>
      <div><h5>Catálogo completo</h5><p>{CONTATO['catalogo_online']}</p></div>
    </div>
    <div class="entrega">{HEXB}<b>{CONTATO['entrega']}</b><span>{CONTATO['entrega_obs']}</span></div>
    <div class="dk-foot"><span class="frase">Paratudo — a loja que tem para tudo.</span>
      <span class="fone">{ANO}</span></div>''')

# ---------------------------------------------------------------- css
CSS = '''
:root{
  --ink:#19191b; --canvas:#232026; --red:#c12025; --red-deep:#8f171b;
  --paper:#ffffff; --steel:#6e696b; --line:#e7e3e2;
  --dtext:#f5f3f2; --dmut:#b7b1b3;
}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--canvas);color:var(--dtext);
  font-family:'Segoe UI','Archivo',system-ui,sans-serif;padding:28px 14px 60px}
.toolbar{max-width:794px;margin:0 auto 22px;display:flex;align-items:center;gap:14px}
.toolbar .t{font-size:14px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.toolbar button{margin-left:auto;background:var(--red);border:0;color:#fff;font:inherit;
  font-size:13px;font-weight:700;padding:9px 20px;cursor:pointer;
  clip-path:polygon(8px 0,100% 0,100% calc(100% - 8px),calc(100% - 8px) 100%,0 100%,0 8px)}
.pageframe{width:100%;display:flex;justify-content:center;margin-bottom:26px}
.pagescale{transform-origin:top center}
.page{width:794px;height:1122px;background:var(--paper);color:var(--ink);
  position:relative;overflow:hidden;box-shadow:0 18px 46px rgba(0,0,0,.4);
  display:flex;flex-direction:column}
.hexb{display:inline-block;width:9px;height:10px;background:var(--red);margin-right:10px;flex:none;
  clip-path:polygon(25% 0,75% 0,100% 50%,75% 100%,25% 100%,0 50%)}
.pgnum{position:absolute;bottom:14px;right:18px;font-size:10.5px;font-weight:700;
  letter-spacing:.1em;color:var(--steel)}
.dark .pgnum{color:var(--dmut)}

/* capa */
.capa{background:var(--ink);color:var(--dtext)}
.capa .slab{position:absolute;inset:0;pointer-events:none}
.capa .slab::before{content:'';position:absolute;top:-180px;right:-300px;width:560px;height:560px;
  background:var(--red);clip-path:polygon(25% 0,75% 0,100% 50%,75% 100%,25% 100%,0 50%);opacity:.92}
.capa .slab::after{content:'';position:absolute;bottom:-180px;left:-200px;width:420px;height:420px;
  background:rgba(255,255,255,.045);clip-path:polygon(25% 0,75% 0,100% 50%,75% 100%,25% 100%,0 50%)}
.capa-top{position:relative;padding:54px 56px 0;display:flex}
.logopanel{background:#fff;padding:26px 30px 20px;width:300px;
  clip-path:polygon(18px 0,100% 0,100% calc(100% - 18px),calc(100% - 18px) 100%,0 100%,0 18px)}
.logopanel img{width:100%;display:block}
.capa-title{position:relative;padding:46px 56px 0}
.capa-title .kicker{font-size:13px;font-weight:700;letter-spacing:.34em;text-transform:uppercase;color:var(--dmut)}
.capa-title h2{font-size:70px;line-height:.98;font-weight:900;letter-spacing:-.015em;
  text-transform:uppercase;margin-top:10px}
.capa-title h2 span{color:var(--red)}
.capa-title .sub{margin-top:14px;font-size:15px;color:var(--dmut);max-width:46ch;line-height:1.5}
.capa-mid{position:relative;padding:38px 56px 0;display:flex;gap:36px;flex:1;min-height:0}
.indice{flex:1.25}
.indice h3{font-size:12px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;
  color:var(--red);border-bottom:1px solid rgba(255,255,255,.16);padding-bottom:9px;margin-bottom:14px}
.indice ul{list-style:none;columns:2;column-gap:30px}
.indice li{display:flex;align-items:center;font-size:11.5px;font-weight:600;
  padding:5px 0;break-inside:avoid;color:var(--dtext)}
.mosaico{width:230px;display:grid;grid-template-columns:1fr 1fr;gap:11px;align-content:start}
.mtile{background:#fff;aspect-ratio:1;display:flex;align-items:center;justify-content:center;
  padding:10px;clip-path:polygon(10px 0,100% 0,100% calc(100% - 10px),calc(100% - 10px) 100%,0 100%,0 10px)}
.mtile img{max-width:100%;max-height:100%;object-fit:contain}
.entrega{position:relative;margin:24px 56px 22px;border:1.5px solid var(--red);
  clip-path:polygon(12px 0,100% 0,100% calc(100% - 12px),calc(100% - 12px) 100%,0 100%,0 12px);
  padding:13px 22px;display:flex;align-items:center;gap:14px;background:rgba(193,32,37,.10)}
.entrega .hexb{width:12px;height:13px;margin:0}
.entrega b{font-size:14px;font-weight:800;color:var(--dtext)}
.entrega span{font-size:11.5px;color:var(--dmut);margin-left:auto}
.entrega.luz b{color:var(--ink)}
.entrega.luz span{color:var(--steel)}
.entrega.luz{background:rgba(193,32,37,.06)}
.entrega.chamada{margin:14px 32px 0;flex:none}
.entrega.chamada b{font-size:12.5px}
.capa-foot{position:relative;margin-top:auto;background:var(--red);color:#fff;
  padding:15px 56px;display:flex;justify-content:space-between;align-items:center;
  font-size:13px;font-weight:700;flex:none}

/* seções */
.cat{background:var(--paper)}
.cat-head{background:var(--ink);display:flex;align-items:stretch;height:64px;flex:none}
.cat-head.slim{height:52px}
.cat-ico{width:64px;background:var(--red);display:flex;align-items:center;justify-content:center;flex:none;
  clip-path:polygon(0 0,100% 0,100% calc(100% - 14px),calc(100% - 14px) 100%,0 100%)}
.cat-head.slim .cat-ico{width:52px}
.cat-ico svg{width:30px;height:30px}
.cat-head.slim .cat-ico svg{width:25px;height:25px}
.cat-head h2{color:#fff;font-size:24px;font-weight:800;letter-spacing:.02em;text-transform:uppercase;
  display:flex;align-items:center;padding-left:24px}
.cat-head.slim h2{font-size:19px}
.cat-rule{height:4px;background:var(--red);flex:none}
.grid{flex:1;display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:1fr;
  gap:6px 14px;padding:18px 32px 8px;min-height:0}
.grid.g5{grid-template-columns:repeat(5,1fr);gap:5px 10px}
.cell{display:flex;flex-direction:column;min-height:0}
.cell.wide{grid-column:span 2}
.ph{flex:1;position:relative;min-height:30px}
.ph img{position:absolute;left:4px;right:4px;bottom:3px;margin:0 auto;
  width:auto;height:auto;
  max-width:calc(100% - 8px);max-height:min(calc(100% - 8px), 175px)}
.cell figcaption{text-align:center;font-size:10px;font-weight:700;letter-spacing:.04em;
  text-transform:uppercase;color:var(--ink);padding:4px 2px 2px;line-height:1.25}
.grid.g5 .cell figcaption{font-size:8.6px}
.cat-foot{border-top:1px solid var(--line);margin:8px 32px 0;padding:12px 0 16px;
  display:flex;align-items:center;justify-content:space-between;flex:none}
.marcas{display:flex;gap:22px;font-size:11px;font-weight:800;letter-spacing:.12em;
  text-transform:uppercase;color:var(--steel)}
.pgchip{background:var(--red);color:#fff;font-size:11px;font-weight:800;width:32px;height:24px;
  display:flex;align-items:center;justify-content:center;
  clip-path:polygon(6px 0,100% 0,100% calc(100% - 6px),calc(100% - 6px) 100%,0 100%,0 6px)}

/* apresentação / marcas */
.apres,.marcaspg{background:var(--paper)}
.ap-band{background:var(--ink);color:var(--dtext);padding:46px 56px 40px;position:relative;
  overflow:hidden;flex:none}
.ap-band::after{content:'';position:absolute;top:-120px;right:-160px;width:340px;height:340px;
  background:var(--red);opacity:.9;clip-path:polygon(25% 0,75% 0,100% 50%,75% 100%,25% 100%,0 50%)}
.ap-band .kicker{font-size:12px;font-weight:700;letter-spacing:.34em;text-transform:uppercase;color:var(--dmut)}
.ap-band h2{font-size:44px;font-weight:900;line-height:1.02;text-transform:uppercase;
  letter-spacing:-.01em;margin-top:8px;position:relative;z-index:1}
.ap-band h2 span{color:var(--red)}
.ap-body{padding:36px 56px 0;flex:1;display:flex;flex-direction:column}
.ap-body .lead{font-size:16px;line-height:1.65;color:#3a3538;max-width:64ch}
.ap-sec{display:flex;align-items:center;font-size:13px;font-weight:700;letter-spacing:.2em;
  text-transform:uppercase;color:var(--steel);margin:34px 0 18px}
.ap-sec::after{content:'';flex:1;height:1px;background:var(--line);margin-left:16px}
.atend{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.acard{border:1px solid var(--line);padding:20px 20px 18px;
  clip-path:polygon(14px 0,100% 0,100% calc(100% - 14px),calc(100% - 14px) 100%,0 100%,0 14px)}
.acard .aic{width:26px;height:26px;color:var(--red)}
.acard h4{font-size:15px;font-weight:800;text-transform:uppercase;letter-spacing:.05em;margin:10px 0 8px}
.acard p{font-size:12.5px;line-height:1.55;color:#4a4548}
.acard a{color:var(--red);text-decoration:none}
.ap-body .entrega{margin:auto 0 26px}
.mwall{padding:20px 56px;display:flex;flex-wrap:wrap;gap:13px;align-content:center;
  justify-content:center;flex:1}
.mchip{border:1px solid var(--line);color:var(--ink);font-size:14.5px;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;padding:13px 24px;
  clip-path:polygon(9px 0,100% 0,100% calc(100% - 9px),calc(100% - 9px) 100%,0 100%,0 9px);
  background:#faf8f8}
.mchip.esc{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.18);color:var(--dtext);
  font-size:10.5px;padding:7px 12px}
.mnota{padding:20px 56px 46px;font-size:12.5px;color:var(--steel)}

/* páginas escuras */
.dark{background:var(--ink);color:var(--dtext)}
.dark::before{content:'';position:absolute;bottom:-160px;left:-180px;width:400px;height:400px;
  background:rgba(255,255,255,.045);clip-path:polygon(25% 0,75% 0,100% 50%,75% 100%,25% 100%,0 50%)}
.dk-head{padding:52px 52px 0;position:relative;flex:none}
.dk-head::after{content:'';position:absolute;top:-90px;right:-150px;width:360px;height:360px;
  background:var(--red-deep);opacity:.35;clip-path:polygon(25% 0,75% 0,100% 50%,75% 100%,25% 100%,0 50%)}
.dk-head .kicker{font-size:12px;font-weight:700;letter-spacing:.34em;text-transform:uppercase;color:var(--red)}
.dk-head h2{font-size:52px;font-weight:900;line-height:.98;text-transform:uppercase;
  letter-spacing:-.015em;margin-top:8px;position:relative}
.dk-head h2 span{color:var(--red)}
.dk-head .sub{margin-top:12px;color:var(--dmut);font-size:14px;max-width:56ch;line-height:1.5;position:relative}
.chips{padding:28px 52px 0;display:flex;flex-wrap:wrap;gap:10px;flex:none}
.chip{border:1.5px solid var(--red);color:#fff;font-size:12px;font-weight:700;
  letter-spacing:.09em;text-transform:uppercase;padding:8px 16px;
  clip-path:polygon(9px 0,100% 0,100% calc(100% - 9px),calc(100% - 9px) 100%,0 100%,0 9px);
  background:rgba(193,32,37,.13)}
.dk-sec{padding:36px 52px 0;flex:none}
.dk-sec h3{display:flex;align-items:center;font-size:13px;font-weight:700;letter-spacing:.2em;
  text-transform:uppercase;color:var(--dmut)}
.dk-sec h3 .hexb{width:10px;height:11px}
.dk-sec h3::after{content:'';flex:1;height:1px;background:rgba(255,255,255,.14);margin-left:16px}
.dk-nota{margin-top:10px;font-size:13px;color:var(--dmut)}
.dgrid4{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:18px}
.dgrid6{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;margin-top:18px}
.dcell{display:flex;flex-direction:column}
.dph{background:#fff;aspect-ratio:1;display:flex;align-items:center;justify-content:center;padding:12px;
  clip-path:polygon(12px 0,100% 0,100% calc(100% - 12px),calc(100% - 12px) 100%,0 100%,0 12px)}
.dgrid6 .dph{padding:9px;clip-path:polygon(9px 0,100% 0,100% calc(100% - 9px),calc(100% - 9px) 100%,0 100%,0 9px)}
.dph img{max-width:100%;max-height:100%;object-fit:contain}
.dcell figcaption{text-align:center;font-size:10.5px;font-weight:700;letter-spacing:.07em;
  text-transform:uppercase;color:var(--dtext);padding-top:8px}
.dk-foot{margin-top:auto;background:var(--red);color:#fff;padding:17px 52px;
  display:flex;justify-content:space-between;align-items:center;flex:none;position:relative}
.dk-foot .frase{font-size:16px;font-weight:800}
.dk-foot .fone{font-size:13px;font-weight:700}

/* destaques (vonixx/tintas/escadas) */
.vx-band{margin:24px 52px 0;display:flex;gap:22px;align-items:center;flex:none}
.vx-band .dph{width:190px;flex:none}
.vx-selo{background:var(--red);color:#fff;font-size:16px;font-weight:800;line-height:1.3;
  padding:22px 26px;text-transform:uppercase;letter-spacing:.04em;
  clip-path:polygon(14px 0,100% 0,100% calc(100% - 14px),calc(100% - 14px) 100%,0 100%,0 14px)}
.tintas{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:18px}
.tcard{background:rgba(255,255,255,.05);padding:16px;
  clip-path:polygon(12px 0,100% 0,100% calc(100% - 12px),calc(100% - 12px) 100%,0 100%,0 12px)}
.tph{background:#fff;height:110px;display:flex;align-items:center;justify-content:center;padding:8px;
  clip-path:polygon(9px 0,100% 0,100% calc(100% - 9px),calc(100% - 9px) 100%,0 100%,0 9px)}
.tph img{max-width:100%;max-height:100%;object-fit:contain}
.tcard h5{font-size:13px;font-weight:800;text-transform:uppercase;letter-spacing:.06em;margin:10px 0 4px}
.tcard p{font-size:11.5px;color:var(--dmut)}

/* contracapa */
.contra .ct-logo{display:flex;justify-content:center;padding:48px 0 8px}
.contra .logopanel{width:260px}
.ct-marcas{padding:26px 52px 0;display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.ct-info{padding:18px 52px 0;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.ct-info h5{font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--red)}
.ct-info p{font-size:13.5px;font-weight:600;margin-top:6px}
.contra .entrega{margin-top:22px}

/* impressão */
@media print{
  body{background:#fff;padding:0}
  .toolbar{display:none}
  .pageframe{margin:0;display:block}
  .pagescale{transform:none!important;width:auto!important}
  .page{box-shadow:none;page-break-after:always;break-after:page}
  .pageframe:last-child .page{page-break-after:auto}
}
@page{size:A4;margin:0}
'''

JS = '''
function fit(){
  if (window.matchMedia && window.matchMedia('print').matches) return;
  document.querySelectorAll('.pageframe').forEach(function(f){
    var s = Math.min(1, f.clientWidth / 794);
    var inner = f.querySelector('.pagescale');
    inner.style.transform = 'scale(' + s + ')';
    inner.style.width = '794px';
    f.style.height = (1122 * s) + 'px';
  });
}
window.addEventListener('resize', fit); fit();
'''

# --------------------------------------------------------------- monta
def main():
    paginas = []
    num = 0
    for tipo, ids in PAGINAS:
        num += 1
        if tipo == 'capa':
            paginas.append(pagina_capa(num))
        elif tipo == 'apresentacao':
            paginas.append(pagina_apresentacao(num))
        elif tipo == 'marcas':
            paginas.append(pagina_marcas(num))
        elif tipo == 'secoes':
            paginas.append(pagina_secoes(ids, num))
        elif tipo == 'destaques':
            paginas.append(pagina_destaques(num))
        elif tipo == 'parafusos':
            paginas.append(pagina_parafusos(num))
        elif tipo == 'contracapa':
            paginas.append(pagina_contracapa(num))
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catálogo de Linhas {ANO} — Paratudo Parafusos e Ferramentas</title>
<style>{CSS}</style>
</head>
<body>
<div class="toolbar"><span class="t">Catálogo de Linhas {ANO} — Paratudo</span>
<button onclick="window.print()">Imprimir / Salvar PDF</button></div>
{''.join(paginas)}
<script>{JS}</script>
</body>
</html>'''
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, 'index.html')
    open(out, 'w', encoding='utf-8').write(html)
    print(f'gerado {out} ({len(html)//1024} KB, {num} paginas)')

if __name__ == '__main__':
    main()
