from pathlib import Path
import csv,json
from decimal import Decimal
from collections import Counter
BASE=Path(__file__).resolve().parent
def read(n):
    with (BASE/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def main():
    pe=read("PE01_pestel.csv");fi=read("PE02_matriz_efi.csv");fe=read("PE02_matriz_efe.csv");st=read("PE03_foda_cruzado.csv");tr=read("PE05_trazabilidad.csv");rank=read("PE04_estrategias_priorizadas.csv")
    sources={r["id"] for r in read("PE00_fuentes.csv")};ev={r["id"] for r in read("PE00_evidencias_bcp.csv")}
    assert {r["Dimensión"] for r in pe}=={"Político","Económico","Social","Tecnológico","Ecológico/Ético","Legal"}
    assert all(r["Evidencia con cifra"] and r["Decisión que obliga"] and set(r["Fuentes"].split("; "))<=sources for r in pe)
    assert all(1<=int(r["Intensidad (1–5)"])<=5 for r in pe)
    for rows in [fi,fe]:
        assert sum(Decimal(r["peso"]) for r in rows)==1
        assert len({r["id"] for r in rows})==len(rows)
        for r in rows:
            assert 1<=int(r["calificacion"])<=4
            assert Decimal(r["peso"])*int(r["calificacion"])==Decimal(r["ponderado"])
            assert r["justificacion_peso"] and r["justificacion_calificacion"]
    assert all(set(r["evidencia_id"].split("; "))<=ev for r in fi)
    assert all(set(r["evidencia_respuesta"].split("; "))<=ev for r in fe)
    factors={r["id"]:r for r in fi+fe};links={(r["Estrategia"],r["Factor F/D/O/A"]) for r in tr}
    assert len(links)==len(tr) and len(tr)>=12
    counts=Counter(r["Tipo"] for r in st)
    assert len(st)>=12 and all(counts[t]>=3 for t in ["FO","FA","DO","DA"])
    assert {r["id"] for r in st}=={r["id"] for r in rank}=={r["Estrategia"] for r in tr}
    bonus={"FO":Decimal("1"),"FA":Decimal("1.2"),"DO":Decimal("1.1"),"DA":Decimal("1.35")}
    for s in st:
        ids=s["Factores cruzados"].split(" + ")
        assert len(ids)==len(set(ids)) and all(i in factors for i in ids)
        assert all(any(i.startswith(t) for i in ids) for t in s["Tipo"])
        assert all(i in s["Estrategia"] and (s["id"],i) in links for i in ids)
        row=next(r for r in rank if r["id"]==s["id"])
        weight=sum(Decimal(factors[i]["peso"]) for i in ids)
        assert Decimal(row["peso_factores"])==weight
        assert Decimal(row["puntaje"])==(weight*bonus[s["Tipo"]]).quantize(Decimal(".001"))
        for t in [t for t in tr if t["Estrategia"]==s["id"]]:
            assert t["Objetivo (Sección 6.2)"].startswith(s["Objetivo_id"]+" ")
            assert t["Proyecto (Sección 7.1)"].startswith(s["Proyecto_id"]+" ")
    scores=[Decimal(r["puntaje"]) for r in rank];assert scores==sorted(scores,reverse=True)
    result={"organizacion":"BCP Perú","pestel_factores":len(pe),"dimensiones":6,"efi_total":str(sum(Decimal(r["ponderado"]) for r in fi)),"efe_total":str(sum(Decimal(r["ponderado"]) for r in fe)),"estrategias":len(st),"por_tipo":dict(counts),"trazabilidad_filas":len(tr),"estado_calculos":"Validado","estado_evidencia":"Respuesta documentada en cada EFE; pesos/calificaciones son juicio académico; cuatro debilidades candidatas inferidas; no auditoría."}
    (BASE.parent/"docs/evidencias/S07/salidas/PE06_validacion.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
