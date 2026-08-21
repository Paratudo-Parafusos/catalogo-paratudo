# -*- coding: utf-8 -*-
"""Regenerates ../index.html from ../data/manifest.json + catalog_head.html.
Run after build_manifest.py, or after editing catalog_head.html by hand."""
import json, html, re, base64, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

MANIFEST_PATH = os.path.join(REPO, "data", "manifest.json")
OUT_PATH = os.path.join(REPO, "index.html")
LOGO_FULL_PATH = os.path.join(HERE, "logo_full_q.png")
LOGO_MARK_PATH = os.path.join(HERE, "logo_mark_q.png")

def data_uri(path):
    b64 = base64.b64encode(open(path, 'rb').read()).decode()
    return 'data:image/png;base64,' + b64

manifest = json.load(open(MANIFEST_PATH, encoding='utf-8'))

CAT_ORDER = [
    "Ferramentas Manuais",
    "Ferramentas El\u00e9tricas",
    "Fixadores e Ferragens",
    "Abrasivos e Corte",
    "Material El\u00e9trico",
    "Hidr\u00e1ulica",
    "Pintura e Acabamento",
    "Jardim e Agropecu\u00e1ria",
    "Seguran\u00e7a e EPI",
    "Solda e Eletrodos",
    "Automotivo",
    "M\u00e1quinas e Equipamentos",
    "Limpeza e Organiza\u00e7\u00e3o",
]

CAT_META = {
    "Ferramentas Manuais": ("01", "Chaves, alicates, martelos, soquetes e trenas para o dia a dia da oficina."),
    "Ferramentas El\u00e9tricas": ("02", "Furadeiras, parafusadeiras, esmerilhadeiras e lixadeiras profissionais."),
    "Fixadores e Ferragens": ("03", "Fechaduras, cadeados, dobradi\u00e7as e ferragens para portas e port\u00f5es."),
    "Abrasivos e Corte": ("04", "Discos, lixas, rebolos e escovas de a\u00e7o para desbaste e acabamento."),
    "Material El\u00e9trico": ("05", "Cabos, tomadas, plugues, l\u00e2mpadas e prote\u00e7\u00f5es para instala\u00e7\u00f5es."),
    "Hidr\u00e1ulica": ("06", "Conex\u00f5es, registros, torneiras, mangueiras e bombas d'\u00e1gua."),
    "Pintura e Acabamento": ("07", "Tintas, vernizes, massas e solventes para pintura e reparo."),
    "Jardim e Agropecu\u00e1ria": ("08", "Ro\u00e7adeiras, enxadas, pulverizadores e ferramentas de cultivo."),
    "Seguran\u00e7a e EPI": ("09", "Capacetes, luvas, botinas e equipamentos de prote\u00e7\u00e3o individual."),
    "Solda e Eletrodos": ("10", "Eletrodos, m\u00e1scaras e consum\u00edveis para solda e corte a plasma."),
    "Automotivo": ("11", "Baterias, \u00f3leos, macacos e itens para manuten\u00e7\u00e3o de ve\u00edculos."),
    "M\u00e1quinas e Equipamentos": ("12", "Compressores, geradores, betoneiras e lavadoras de alta press\u00e3o."),
    "Limpeza e Organiza\u00e7\u00e3o": ("13", "Vassouras, caixas organizadoras e maletas para guardar tudo."),
}

buckets = {c: [] for c in CAT_ORDER}
for m in manifest:
    if m['cat'] in buckets:
        buckets[m['cat']].append(m)

def slug(s):
    s = s.lower()
    s = (s.replace('\u00e9', 'e').replace('\u00e1', 'a').replace('\u00e3', 'a')
           .replace('\u00e7', 'c').replace('\u00fa', 'u').replace('\u00ed', 'i')
           .replace('\u00f3', 'o'))
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s

def esc(s):
    return html.escape(s, quote=True)

LOGO_FULL_URI = data_uri(LOGO_FULL_PATH)   # full lockup + tagline + phone, for the letterhead
LOGO_MARK_URI = data_uri(LOGO_MARK_PATH)   # mark only (badge + screw + "UDO"), for the footer

def product_card(item):
    codigo = esc(item['codigo'])
    desc = esc(item['desc'])
    marca_raw = item['marca']
    marca = esc(marca_raw.title() if marca_raw.isupper() else marca_raw)
    img = item['img']
    return ('<figure class="card">'
            '<div class="card-photo"><img src="%s" alt="%s" loading="lazy" width="260" height="260"></div>'
            '<figcaption>'
            '<span class="card-brand">%s</span>'
            '<span class="card-name">%s</span>'
            '<span class="card-sku">Ref. %s</span>'
            '</figcaption>'
            '</figure>') % (img, desc, marca, desc, codigo)

nav_chips = []
sections = []
total_items = 0
for cat in CAT_ORDER:
    items = buckets[cat]
    if not items:
        continue
    total_items += len(items)
    cid = slug(cat)
    num, blurb = CAT_META[cat]
    nav_chips.append('<a class="chip" href="#%s">%s</a>' % (cid, esc(cat)))
    cards = "\n".join(product_card(i) for i in items)
    sections.append(
        '<section class="cat" id="%s">'
        '<div class="cat-head">'
        '<span class="cat-num">%s</span>'
        '<div class="cat-titles"><h2>%s</h2><p>%s</p></div>'
        '<span class="cat-count">%02d itens</span>'
        '</div>'
        '<div class="grid">\n%s\n</div>'
        '</section>' % (cid, num, esc(cat), esc(blurb), len(items), cards)
    )

NAV_HTML = "\n".join(nav_chips)
SECTIONS_HTML = "\n".join(sections)
CAT_COUNT = len(sections)

with open(os.path.join(HERE, "catalog_head.html"), "r", encoding="utf-8") as f:
    CSS_TEMPLATE = f.read()

html_out = CSS_TEMPLATE
html_out = html_out.replace("__LOGO_FULL__", LOGO_FULL_URI)
html_out = html_out.replace("__LOGO_MARK__", LOGO_MARK_URI)
html_out = html_out.replace("__TOTAL_ITEMS__", str(total_items))
html_out = html_out.replace("__CAT_COUNT__", str(CAT_COUNT))
html_out = html_out.replace("__NAV_HTML__", NAV_HTML)
html_out = html_out.replace("__SECTIONS_HTML__", SECTIONS_HTML)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(html_out)
print("wrote", OUT_PATH, len(html_out), "chars")
