# Convite · Geovana & Kayri

Convite digital de casamento — um único arquivo HTML, sem dependências externas.

- **Abrir:** `index.html` (pronto para o GitHub Pages) ou `dist/convite-geovana-kayri.html`.
- **Capa:** laço de cetim em 3D (WebGL), feito de uma única fita contínua que se desata ao tocar em "Abrir convite".
- **Depois de aberto:** foto dos noivos, mensagem, data e horário, local (com mapa e calendário) e a seção "Presenteie os noivos" com QR Code PIX real e botão de copiar.

## Parâmetros de URL
- `?speed=0.4` — câmera lenta
- `?auto` — abre sozinho
- `?cor=dourado` (ou `rosa`, `champagne`, `salvia`) — cor da fita (padrão: branca)

## Estrutura
```
src/index.template.html   marcação
src/style.css             estilos (paleta em :root)
src/fonts.css             fontes embutidas (Lora, Inter)
src/ribbon-engine.js      motor WebGL da fita de cetim
src/bowposes.js           forma das alças
src/bow-motion.js         a fita contínua e o desatar (tempos em T)
src/bow-view.js           escala/posição do laço na tela
src/main.js               orquestração (tempos em TL), PIX, calendário
src/pix.txt               código PIX (fonte única do QR Code e do botão)
qrsvg.py                  gera o QR Code e confere CRC + leitura
build.py                  junta tudo em um único HTML
assets/foto.jpg           foto original
```

## Gerar de novo
Requer Python 3 com `opencv-python` (para gerar/validar o QR Code):
```
python3 build.py
```
Saída: `dist/convite-geovana-kayri.html` e `index.html`.
