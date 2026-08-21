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

## Contato

**Paratudo Parafusos e Ferramentas**
(35) 3427-2450 — (35) 9.9758-0912
