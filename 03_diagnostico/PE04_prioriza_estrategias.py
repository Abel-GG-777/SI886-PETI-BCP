"""Prioridad preliminar según la fórmula de la guía del taller 07."""
from pathlib import Path
import csv
from decimal import Decimal
from collections import Counter

BASE = Path(__file__).resolve().parent
OUT = BASE.parent / "docs" / "evidencias" / "S07" / "salidas"
BONO = {"DA": Decimal("1.35"), "FA": Decimal("1.20"), "DO": Decimal("1.10"), "FO": Decimal("1.00")}

def read(name):
    with (BASE/name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def main():
    factors = read("PE02_matriz_efi.csv") + read("PE02_matriz_efe.csv")
    assert len({f["id"] for f in factors}) == len(factors), "Factores duplicados"
    weights = {f["id"]: Decimal(f["peso"]) for f in factors}
    rows = read("PE03_foda_cruzado.csv")
    assert len({r["id"] for r in rows}) == len(rows), "Estrategias duplicadas"
    counts = Counter(r["Tipo"] for r in rows)
    assert len(rows) >= 12 and all(counts[t] >= 3 for t in BONO)
    for r in rows:
        ids = [x.strip() for x in r["Factores cruzados"].split("+")]
        assert len(ids) == len(set(ids)), "Factor repetido en estrategia"
        assert all(x in weights for x in ids), "Factor desconocido"
        assert all(any(x.startswith(p) for x in ids) for p in r["Tipo"]), "Cruce incompatible"
        w = sum(weights[x] for x in ids)
        r["peso_factores"] = str(w.quantize(Decimal("0.000")))
        r["bono_tipo"] = str(BONO[r["Tipo"]])
        r["puntaje"] = str((w * BONO[r["Tipo"]]).quantize(Decimal("0.001")))
    rows.sort(key=lambda r: (-Decimal(r["puntaje"]), r["id"]))
    for i,r in enumerate(rows,1):
        r["orden"] = i
        r["Prioridad preliminar"] = f"Orden {i} según puntaje"
    with (BASE/"PE04_estrategias_priorizadas.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    report="Método: suma de pesos EFI/EFE de factores únicos x bono del tipo.\n"
    report+="Bonos de la guía: DA=1.35; FA=1.20; DO=1.10; FO=1.00.\n"
    report+="Desempate por ID; orden no sustituye dependencias ni presupuesto.\n"
    report+="\n".join(f"{r['orden']:02}. {r['id']} {r['Tipo']} {r['puntaje']} {r['Proyecto candidato']}" for r in rows)
    report+=f"\nDistribución diseñada: {dict(sorted(counts.items()))}.\n"
    top=Counter(r["Tipo"] for r in rows[:4])
    report+=f"Primeras cuatro: {dict(sorted(top.items()))}.\n"
    report+="Tres estrategias por cuadrante es un requisito, no evidencia de predominio defensivo.\n"
    report+="La secuencia debe atender controles y continuidad antes de expandir servicios.\n"
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"PE04_resultados.txt").write_text(report,encoding="utf-8")
    print(report)

if __name__ == "__main__":
    main()
