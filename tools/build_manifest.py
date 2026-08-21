# -*- coding: utf-8 -*-
"""Picks a curated sample of product photos per category and writes
../data/manifest.json (product name/brand/thumbnail as base64 JPEG).
Run tools/build_catalog.py afterwards to regenerate ../index.html.

Requires the full photo library from the Paratudo_Fotos project:
_progresso_fotos.csv plus one {codigo}.png per product. Point
SOURCE_PHOTOS_DIR below at that folder if it's not in the default spot."""
import csv, re, unicodedata, random, json, io, os
from PIL import Image
import base64

random.seed(11)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SOURCE_PHOTOS_DIR = r"C:\Users\User\Documents\Paratudo_Fotos"
os.chdir(SOURCE_PHOTOS_DIR)

def norm(t):
    t = t.upper()
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return t

STOPWORDS_LOWER = {'DE', 'DA', 'DO', 'DAS', 'DOS', 'COM', 'PARA', 'SEM', 'EM',
                    'NO', 'NA', 'NOS', 'NAS', 'POR', 'AO', 'AOS', 'E'}
KEEP_UPPER = {'CA', 'MM', 'CM', 'PVC', 'MM2', 'LED', 'SI', 'CG', 'LT', 'EPI',
              '2T', '4T', 'TIG', 'MMA', 'HVLP', 'PU', 'AC', 'USB'}

def clean_desc(d):
    d = re.sub(r'\*+\s*$', '', d).strip()
    d = re.sub(r'\s+', ' ', d)
    words = d.split(' ')
    out = []
    for w in words:
        wu = w.upper()
        if wu in STOPWORDS_LOWER:
            out.append(wu.lower())
        elif re.match(r'^\d', w) or wu in KEEP_UPPER or re.match(r'^[0-9./,%"\'\-]+$', w):
            out.append(w)
        elif len(w) <= 3 and wu == w and w.isalpha():
            out.append(w)
        else:
            out.append(w.capitalize())
    return ' '.join(out)

rows = [r for r in csv.DictReader(open('_progresso_fotos.csv', encoding='utf-8')) if r['status'] == 'done']

CATS = [
 ('Ferramentas Manuais', r'CHAVE (DE FENDA|PHILLIPS|COMBINADA|ESTRELA|ALLEN|FIXA|CATRACA|CANHAO|INGLESA|GRIFO)|ALICATE|MARTELO|MARRETA|SOQUETE|JOGO DE SOQUETE|TRENA|NIVEL|ESQUADRO|SERROTE|LIMA |FORMAO|SACA|EXTRATOR|MORSA|TORNO DE BANCADA|PE DE CABRA', 32),
 ('Ferramentas Elétricas', r'FURADEIRA|PARAFUSADEIRA|ESMERILHADEIRA|SERRA (CIRC|TICO|MARMORE|SABRE)|LIXADEIRA|MARTELETE|PLAINA ELET|SOPRADOR TERMICO|FRESADORA|POLITRIZ ELET|BATERIA \d+V|CARREGADOR DE BATERIA', 28),
 ('Fixadores e Ferragens', r'PARAFUS|PORCA|ARRUEL|BUCHA|CHUMBAD|REBITE|PRISIONEIR|PREGO|CUPILHA|DOBRADIC|FECHAD|FECHO|CADEAD|TRINCO|MAO FRANCESA|GONZO|DIN\d', 26),
 ('Abrasivos e Corte', r'DISCO DE CORTE|DISCO DE DESBASTE|DISCO FLAP|LIXA|REBOLO|ESCOVA DE ACO|BROCA |FLANGE|RODA DE LIXA|CINTA DE LIXA', 26),
 ('Material Elétrico', r'CABO FLEX|FIO CABO|TOMADA|PLUGUE|PINO (MACHO|FEMEA)|DISJUNTOR|LAMPADA|LUMINARIA|FITA ISOLANTE|BENJAMIM|INTERRUPTOR|EXTENSAO|FILTRO DE LINHA|CHUVEIRO', 22),
 ('Hidráulica', r'TUBO|CONEXAO|JOELHO|UNIAO|REGISTRO|TORNEIRA|MANGUEIRA|ENGATE RAPIDO|SIFAO|VALVULA|ADAPTADOR.*MANGUEIRA|ESGUICHO|BOMBA D|BOMBA SUBMERSA|MOTOBOMBA', 26),
 ('Pintura e Acabamento', r'TINTA|VERNIZ|PINCEL|ROLO DE PINTURA|MASSA (CORRIDA|PLASTICA|POLIESTER)|SOLVENTE|THINNER|LIXA D.AGUA|FUNDO|SELADOR|PRIMER|ESMALTE SINTETICO', 24),
 ('Jardim e Agropecuária', r'ROCADEIRA|MOTOSSERRA|CORTADOR DE GRAMA|ENXADA|ENXADAO|PA (QUADRADA|VANGA|DE BICO)|PICARETA|FOICE|MACHADO|MANGUEIRA.*JARDIM|PULVERIZADOR|ASPERSOR|ADUBO|CORDA|ARAME FARPADO|CAVADEIRA|TRITURADOR|TESOURA DE PODA', 26),
 ('Segurança e EPI', r'CAPACETE|LUVA |OCULOS|MASCARA|PROTETOR AURICULAR|COLETE|CINTURAO|TALABARTE|BOTA |BOTINA|SAPATO DE SEGURANCA|TAMANCO|AVENTAL|PROTETOR SOLAR|CREME DE PROTECAO', 28),
 ('Solda e Eletrodos', r'ELETRODO|MASCARA DE SOLDA|INVERSORA|TOCHA|ARAME.*SOLDA|VARETA|SOLDA|GOIVAGEM|PLASMA', 22),  # noqa: kept ascii "Eletrodos" to match CAT_ORDER key
 ('Automotivo', r'BATERIA AUTOMOTIVA|OLEO (2T|4T|PARA MOTOR)|GRAXA|MACACO |CAVALETE|CABO DE RE?BOQUE|CALIBRADOR|FILTRO DE OLEO|VELA DE IGNICAO|PASTILHA DE FREIO', 22),
 ('Limpeza e Organização', r'VASSOURA|RODO|PANO |ESCOVA DE ROUPA|CAIXA ORGANIZADORA|MALETA|GAVETEIRO|CAIXA BIN|BOMBONA|BALDE|CESTO', 20),
 ('Máquinas e Equipamentos', r'COMPRESSOR|GERADOR|BETONEIRA|LAVADORA DE ALTA PRESSAO|MOTOCULTIVADOR|COMPACTADOR', 18),
]

def classify(desc):
    d = norm(desc)
    for name, pat, _ in CATS:
        if re.search(pat, d):
            return name
    return None

buckets = {name: [] for name, _, _ in CATS}
for r in rows:
    c = classify(r['descricao'])
    if c:
        buckets[c].append(r)

OUTDIR = os.path.join(REPO, "data")
manifest = []

for name, pat, cap in CATS:
    items = buckets[name]
    seen_group = set()
    seen_desc_prefix = set()
    picked = []
    random.shuffle(items)
    items.sort(key=lambda r: (0 if (r['notes'] and 'fonte:' in r['notes']) else 1))
    for r in items:
        gk = r['group_key'] or r['codigo']
        if gk in seen_group:
            continue
        dp = norm(r['descricao'])[:14]
        if dp in seen_desc_prefix:
            continue
        path = r['codigo'] + '.png'
        if not os.path.exists(path):
            continue
        seen_group.add(gk); seen_desc_prefix.add(dp)
        picked.append(r)
        if len(picked) >= cap:
            break
    for r in picked:
        try:
            im = Image.open(r['codigo'] + '.png').convert('RGB')
        except Exception:
            continue
        im.thumbnail((260, 260), Image.LANCZOS)
        sq = Image.new('RGB', (260, 260), (255, 255, 255))
        sq.paste(im, ((260 - im.width) // 2, (260 - im.height) // 2))
        buf = io.BytesIO()
        sq.save(buf, 'JPEG', quality=74, optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode()
        manifest.append({
            'cat': name,
            'codigo': r['codigo'],
            'desc': clean_desc(r['descricao']),
            'marca': r['marca_nome'].strip(),
            'img': 'data:image/jpeg;base64,' + b64,
        })

print('total items:', len(manifest))
from collections import Counter
for k, v in Counter(m['cat'] for m in manifest).items():
    print(' ', k, v)
tot_kb = sum(len(m['img']) for m in manifest) / 1024
print('total b64 size KB:', round(tot_kb, 1))

os.makedirs(OUTDIR, exist_ok=True)
with open(os.path.join(OUTDIR, 'manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False)
print('saved manifest')
