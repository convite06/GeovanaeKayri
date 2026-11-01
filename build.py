#!/usr/bin/env python3
"""Junta fontes, CSS, JS e a foto em UM único arquivo HTML.
Uso:  python3 build.py [caminho/da/foto.jpg]
Saída: dist/convite-geovana-kayri.html
"""
import base64, pathlib, sys, html as _h
import qrsvg

root = pathlib.Path(__file__).parent
src = root / 'src'
photo_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / 'assets' / 'foto.jpg'

def read(name):
    return (src / name).read_text(encoding='utf-8')

html = read('index.template.html')
photo = 'data:image/jpeg;base64,' + base64.b64encode(photo_path.read_bytes()).decode('ascii')

parts = {
    '/*{{FONTS}}*/': read('fonts.css'),
    '/*{{CSS}}*/':   read('style.css'),
    '/*{{ENGINE}}*/': read('ribbon-engine.js'),
    '/*{{POSES}}*/':  read('bowposes.js'),
    '/*{{VIEW}}*/':   read('bow-view.js'),
    '/*{{MOTION}}*/': read('bow-motion.js'),
    '/*{{MAIN}}*/':   read('main.js'),
}
for key, val in parts.items():
    assert key in html, key
    html = html.replace(key, val)
html = html.replace('{{PHOTO}}', photo)

# PIX: um único payload (src/pix.txt) alimenta o QR Code e o botão de copiar
pix = (src / 'pix.txt').read_text(encoding='utf-8')
qr, n = qrsvg.build(pix)
assert '{{QR}}' in html and '{{PIX}}' in html
html = html.replace('{{QR}}', qr).replace('{{PIX}}', _h.escape(pix, quote=False))
assert html.count(pix) == 1, 'o código PIX deve aparecer exatamente uma vez (no campo de cópia)'
print('PIX ok · QR', n, 'módulos (nível M) · decodificado = payload')

out = root / 'dist' / 'convite-geovana-kayri.html'
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding='utf-8')
(root / 'index.html').write_text(html, encoding='utf-8')   # cópia na raiz (GitHub Pages)
print(out, f'{out.stat().st_size/1024:.0f} KB')
