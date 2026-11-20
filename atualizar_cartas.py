"""Copia as cartas da planilha para o index.html.

Uso:  python atualizar_cartas.py [planilha.xlsx]
Planilha: coluna A = título, coluna B = 5 palavras proibidas separadas por vírgula.
A primeira linha é o cabeçalho. Só usa a biblioteca padrão do Python.
"""
import json, re, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

AQUI = Path(__file__).parent
XLSX = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "cartas.xlsx"
HTML = AQUI / "index.html"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def ler_planilha(caminho):
    z = zipfile.ZipFile(caminho)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(NS + "si"):
            shared.append("".join(t.text or "" for t in si.iter(NS + "t")))
    linhas = []
    for row in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(NS + "row"):
        cel = {}
        for c in row.iter(NS + "c"):
            col = re.match(r"[A-Z]+", c.get("r")).group()
            v = c.find(NS + "v")
            if c.get("t") == "s":
                cel[col] = shared[int(v.text)]
            elif c.get("t") == "inlineStr":
                cel[col] = "".join(t.text or "" for t in c.iter(NS + "t"))
            else:
                cel[col] = v.text if v is not None else ""
        linhas.append(cel)
    return linhas[1:]  # pula cabeçalho


def cap(s):
    return s[:1].upper() + s[1:]


def main():
    cartas, erros, vistos = [], [], set()
    for n, l in enumerate(ler_planilha(XLSX), start=2):
        titulo = (l.get("A") or "").strip()
        palavras = [cap(p.strip()) for p in (l.get("B") or "").split(",") if p.strip()]
        if not titulo and not palavras:
            continue
        if not titulo or len(palavras) != 5:
            erros.append(f"linha {n}: '{titulo}' tem {len(palavras)} palavras proibidas (esperado 5)")
        elif titulo.lower() in vistos:
            erros.append(f"linha {n}: título repetido '{titulo}'")
        vistos.add(titulo.lower())
        cartas.append([titulo] + palavras)
    if erros:
        print("Corrija a planilha:\n  " + "\n  ".join(erros))
        sys.exit(1)

    corpo = ",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in cartas)
    bloco = f"/*CARTAS-INICIO*/\nconst CARDS = [\n{corpo}\n];\n/*CARTAS-FIM*/"
    html = HTML.read_text(encoding="utf-8")
    novo, qtd = re.subn(r"/\*CARTAS-INICIO\*/.*?/\*CARTAS-FIM\*/", lambda _: bloco, html, flags=re.S)
    if qtd != 1:
        sys.exit("Marcadores /*CARTAS-INICIO*/ e /*CARTAS-FIM*/ não encontrados no index.html")
    HTML.write_bytes(novo.encode("utf-8"))  # mantém LF; write_text no Windows trocaria por CRLF
    print(f"{len(cartas)} cartas gravadas em {HTML.name}")


if __name__ == "__main__":
    main()
