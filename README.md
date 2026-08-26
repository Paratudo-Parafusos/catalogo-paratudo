# Catálogo Paratudo

Catálogo de produtos da **Paratudo Parafusos e Ferramentas**, em uma única
página estática (`index.html`) — sem servidor, sem dependências, pronta pra
abrir no navegador ou publicar no GitHub Pages.

- 316 produtos reais (foto, marca, nome e código de referência)
- Organizados em 13 categorias, com menu de navegação
- Logo oficial da loja no cabeçalho e rodapé
- Funciona em tema claro e escuro

## Ver localmente

Abra `index.html` direto no navegador — é um arquivo só, com tudo embutido
(imagens inclusas). Não precisa instalar nada.

## Publicar

### GitHub Pages (automático)

Este repositório já vem com um workflow (`.github/workflows/pages.yml`) que
publica `index.html` no GitHub Pages a cada `push` na branch `main`.

Pra ativar (só na primeira vez):

1. No GitHub, vá em **Settings → Pages**.
2. Em **Source**, escolha **GitHub Actions**.
3. Dê um `push` na `main` — o workflow builda e publica sozinho.
4. O link fica em **Settings → Pages** (algo como
   `https://paratudo-parafusos.github.io/catalogo-paratudo/`).

### Manual

`index.html` também pode ser hospedado em qualquer lugar que sirva arquivos
estáticos (Netlify, Vercel, um servidor próprio, etc.) — é só copiar o
arquivo.

## Atualizar o catálogo

O `index.html` é **gerado**, não editado à mão. O conteúdo (fotos, categorias,
quantidade de itens por categoria) vem de dois passos em `tools/`:

1. **`tools/build_manifest.py`** — escolhe uma amostra de produtos por
   categoria a partir da base de fotos completa do projeto Paratudo_Fotos
   (`_progresso_fotos.csv` + um `{código}.png` por produto) e grava
   `data/manifest.json` (nome, marca, categoria e a foto já em miniatura).
   - Pra trocar quais categorias existem, quantos itens cada uma mostra, ou
     as palavras-chave que classificam um produto numa categoria, edite a
     lista `CATS` no topo do arquivo.
   - Por padrão lê as fotos de `C:\Users\User\Documents\Paratudo_Fotos`
     (constante `SOURCE_PHOTOS_DIR` no topo do arquivo) — ajuste esse
     caminho se a pasta de fotos mudar de lugar.
2. **`tools/build_catalog.py`** — lê `data/manifest.json` +
   `tools/catalog_head.html` (o layout/design) e monta o `index.html` final.

Rodar os dois, nessa ordem, depois de qualquer mudança:

```bash
python tools/build_manifest.py
python tools/build_catalog.py
```

Requer Python 3 com Pillow (`pip install pillow`).

### Trocar só o design (cores, categorias, textos fixos)

Edite `tools/catalog_head.html` (CSS + estrutura da página) e rode só
`python tools/build_catalog.py` — não precisa refazer o `manifest.json`.

### Trocar a logo

A arte da logo entra como imagem de verdade (não é desenhada em CSS/SVG).
Pra trocar:

1. Salve o novo arquivo da logo em algum lugar do computador.
2. Aponte `SOURCE_LOGO` no topo de `tools/crop_logo.py` pra esse arquivo.
3. Rode `python tools/crop_logo.py` — ele recorta o fundo branco em excesso,
   separa a versão completa (com "Parafusos e Ferramentas" e telefone) da
   versão só da marca (pro rodapé), e gera as duas em tamanho otimizado pra
   web (`logo_full_q.png`, `logo_mark_q.png`).
4. Rode `python tools/build_catalog.py` de novo.

## Estrutura

```
index.html                  ← o catálogo (gerado, não editar à mão)
data/manifest.json          ← produtos selecionados (gerado)
tools/build_manifest.py     ← passo 1: escolhe os produtos e as fotos
tools/build_catalog.py      ← passo 2: monta o index.html
tools/catalog_head.html     ← layout, CSS e textos fixos do catálogo
tools/crop_logo.py          ← prepara os arquivos da logo
tools/logo_full*.png        ← logo completa (cabeçalho)
tools/logo_mark*.png        ← logo compacta (rodapé)
.github/workflows/pages.yml ← publica no GitHub Pages a cada push
```


## Catálogo de Linhas (simplificado)

Além do catálogo completo, o repositório gera o **Catálogo de Linhas**
(`simplificado/index.html`): 19 páginas A4 mostrando as ~230 linhas que a
loja trabalha, por seção, sem preço — pro cliente folhear impresso ou online.
No GitHub Pages ele fica em `/simplificado/`.

- O conteúdo vem de `tools/dados_simplificado.py` (seções, linhas e qual foto
  de `tools/fotos_docx/` cada linha usa). Pra mudar qualquer coisa do
  catálogo, edite esse arquivo.
- As fotos em `tools/fotos_docx/` foram extraídas do Word
  "CATALOGO PARATUDO.docx" (numeração `{N}.jpg` segue a ordem do documento).
- Depois de editar, gere de novo:

```bash
python tools/build_simplificado.py
```

- Pra gerar o PDF de impressão: abra `simplificado/index.html` no Chrome e
  use o botão **Imprimir / Salvar PDF** (ou Ctrl+P, destino PDF, margens
  nenhuma).

### Logos das marcas

Os logos ficam em `tools/logos_marcas/{Marca}.jpg` (29 arquivos, coletados dos
sites oficiais e do Wikimedia Commons). O gerador usa o logo quando o arquivo
existe e cai pro nome em texto quando não existe — então pra incluir uma marca
nova é só salvar o arquivo com o mesmo nome que está em `MARCAS_PARCEIRAS`
(nomes com espaço/acento têm um de-para no dicionário `LOGO_ARQ` do gerador).

São 51 logos, de 4 fontes: sites oficiais das marcas, Wikimedia Commons,
repositórios de logos (seeklogo e o CDN da freebiesupply) e sites de grupos
donos de várias marcas (ex.: ccmdobrasil.com.br traz Nakashi, Kawashima e CCM
em qualidade oficial — o site é feito em JavaScript, então só aparece se você
renderizar com `chrome --headless --dump-dom`).

Marcas ainda sem logo, que aparecem como chip de texto na página 3: Western,
Ribeiro, H7, Pinheiro, Real, Botafogo, Servente, Estival, Hard, PDR e Xadrez.
São marcas pequenas de nome genérico — a busca automática devolve coisa errada
(Real Madrid, banda KISS, Sherwin-Williams) em vez do logo certo. Pra essas,
o caminho é pedir o arquivo ao fornecedor.

Pendência: foto da fachada na página de apresentação.

## Contato

**Paratudo Parafusos e Ferramentas**
(35) 3427-2450 — (35) 9.9758-0912
