"""QR Code PIX: gera o SVG a partir do payload EXATO e confere tudo.
   · CRC16 do payload (campo 63) precisa bater;
   · o QR gerado é decodificado de volta e comparado caractere a caractere."""
import cv2, numpy as np

def crc16(s):
    c = 0xFFFF
    for b in s.encode('utf-8'):
        c ^= b << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x1021) & 0xFFFF if c & 0x8000 else (c << 1) & 0xFFFF
    return c

def matrix(payload):
    p = cv2.QRCodeEncoder_Params()
    p.correction_level = cv2.QRCodeEncoder_CORRECT_LEVEL_M   # nível M: o padrão dos apps bancários
    p.mode = cv2.QRCodeEncoder_MODE_BYTE
    img = cv2.QRCodeEncoder.create(p).encode(payload)
    m = (img[2:-2, 2:-2] == 0)                                 # o OpenCV devolve 2 módulos de borda
    return m

def decode_all(m, scale=10, quiet=4):
    n = m.shape[0]
    big = np.full(((n + 2 * quiet) * scale,) * 2, 255, np.uint8)
    for y, x in zip(*np.nonzero(m)):
        big[(y + quiet) * scale:(y + quiet + 1) * scale, (x + quiet) * scale:(x + quiet + 1) * scale] = 0
    out = []
    d = cv2.QRCodeDetector()
    out.append(d.detectAndDecode(big)[0])
    try:
        out.append(cv2.QRCodeDetectorAruco().detectAndDecode(big)[0])
    except Exception as e:
        out.append('aruco-indisponível')
    return out

def build(payload, color='#2B231D'):
    assert payload == payload.strip() and '\n' not in payload
    assert payload[-8:-4] == '6304' and '%04X' % crc16(payload[:-4]) == payload[-4:], 'CRC do PIX não confere'
    m = matrix(payload)
    n = m.shape[0]
    for r in decode_all(m):
        assert r == payload, ('QR não decodifica igual', r)
    q = 4
    d = []
    for y in range(n):
        x = 0
        while x < n:
            if m[y, x]:
                x0 = x
                while x < n and m[y, x]: x += 1
                d.append(f'M{x0 + q} {y + q}h{x - x0}v1h-{x - x0}z')
            else:
                x += 1
    N = n + 2 * q
    svg = (f'<svg class="qr-svg" viewBox="0 0 {N} {N}" role="img" aria-labelledby="qr-t" shape-rendering="crispEdges" xmlns="http://www.w3.org/2000/svg">'
           f'<title id="qr-t">QR Code PIX para presentear Geovana e Kayri</title>'
           f'<rect width="{N}" height="{N}" fill="#FFFFFF"/><path fill="{color}" d="{"".join(d)}"/></svg>')
    return svg, n

if __name__ == '__main__':
    import sys
    pl = open(sys.argv[1], encoding='utf-8').read()
    svg, n = build(pl)
    print('ok', n, 'módulos', len(svg), 'bytes')
