"""Adaptación de la herramienta oficial: datos del BCP y justificación en CSV."""
from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parent
def main():
    report=[]
    EFI=pd.read_csv(BASE/"PE02_matriz_efi.csv",encoding="utf-8-sig",keep_default_na=False)
    EFE=pd.read_csv(BASE/"PE02_matriz_efe.csv",encoding="utf-8-sig",keep_default_na=False)
    for nombre,m in [("EFI",EFI),("EFE",EFE)]:
        assert m.id.is_unique and abs(m.peso.sum()-1)<1e-9
        assert m.peso.between(0,1,inclusive="right").all() and m.calificacion.isin([1,2,3,4]).all()
        assert m.justificacion_peso.str.len().gt(0).all() and m.justificacion_calificacion.str.len().gt(0).all()
        if nombre=="EFI":
            assert (((m.tipo=="F") & m.calificacion.ge(3))|((m.tipo=="D") & m.calificacion.le(2))).all()
        m["ponderado"]=(m.peso*m.calificacion).round(3)
        total=m.ponderado.sum()
        report.append(f"{nombre}: pesos={m.peso.sum():.3f}; total={total:.3f}; referencia=2.500")
        report.append(m[["id","factor","peso","calificacion","ponderado"]].to_string(index=False))
        report.append("Valoración académica, no auditoría ni comparación estadística sectorial.")
        m.to_csv(BASE/f"PE02_matriz_{nombre.lower()}.csv",index=False,encoding="utf-8-sig")
    out=BASE.parent/"docs/evidencias/S07/salidas";out.mkdir(parents=True,exist_ok=True)
    text="\n\n".join(report)+"\n";(out/"PE02_resultados.txt").write_text(text,encoding="utf-8");print(text)
if __name__=="__main__":main()
