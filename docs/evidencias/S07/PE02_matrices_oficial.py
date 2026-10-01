# 03_diagnostico/PE02_matrices.py
import pandas as pd

# ---------- EFI: Evaluación de Factores Internos ----------
# calificación: 1 = debilidad mayor · 2 = debilidad menor · 3 = fortaleza menor · 4 = fortaleza mayor
EFI = pd.DataFrame([
 ("F1","Red de distribución propia con cobertura en 3 regiones",              .11, 4),
 ("F2","Base histórica de 15 años de compras de 8 400 clientes",              .10, 4),
 ("F3","Relación directa y de confianza con el pequeño comerciante",          .08, 4),
 ("F4","ERP integrado en compras, ventas, inventarios y contabilidad",        .07, 3),
 ("F5","Equipo de almacén con proceso estandarizado y escáner",               .06, 3),
 ("D1","Ausencia de capacidad de analítica de datos",                         .12, 1),
 ("D2","Dependencia de un único desarrollador para el canal digital",         .11, 1),
 ("D3","Portal B2B con 4 % de adopción",                                      .09, 1),
 ("D4","Ruteo y despacho gestionados en hoja de cálculo (22 % del costo)",    .10, 1),
 ("D5","Sin inventario de datos personales ni programa de cumplimiento",      .09, 1),
 ("D6","Servidor único sin redundancia ni prueba de restauración",            .07, 2),
], columns=["id","factor","peso","calificacion"])

# ---------- EFE: Evaluación de Factores Externos ----------
# calificación: mide QUÉ TAN BIEN RESPONDE la organización al factor
# 1 = respuesta deficiente · 2 = por debajo del promedio · 3 = por encima · 4 = superior
EFE = pd.DataFrame([
 ("O1","Adopción de smartphone en el segmento minorista",                     .14, 1),
 ("O2","Herramientas de analítica de bajo costo disponibles",                 .10, 1),
 ("O3","Talento técnico local disponible en la región",                       .08, 2),
 ("O4","Crecimiento del consumo en la macrorregión sur",                      .09, 3),
 ("O5","Interoperabilidad del Estado abre nuevos canales de venta institucional", .07, 1),
 ("A1","Entrada de mayoristas con canal digital consolidado",                 .13, 1),
 ("A2","Fin de soporte de la plataforma del ERP",                     .12, 1),
 ("A3","Nuevo Reglamento de Protección de Datos Personales",                  .11, 1),
 ("A4","Volatilidad cambiaria sobre contratos de TI en dólares",              .09, 2),
 ("A5","Rotación y escasez de personal técnico",                              .07, 2),
], columns=["id","factor","peso","calificacion"])

for nombre, m in [("EFI", EFI), ("EFE", EFE)]:
    assert abs(m.peso.sum() - 1) < 1e-9, f"Los pesos de {nombre} deben sumar 1 (suman {m.peso.sum()})"
    m["ponderado"] = (m.peso * m.calificacion).round(3)
    total = m.ponderado.sum()
    print(f"\n{'='*80}\nMATRIZ {nombre}")
    print(m.to_string(index=False))
    print(f"TOTAL PONDERADO {nombre}: {total:.2f}   (promedio de referencia: 2.50)")
    if nombre == "EFI":
        print("→ " + ("Posición interna FUERTE" if total > 2.5 else
              "Posición interna DÉBIL: las debilidades pesan más que las fortalezas"))
    else:
        print("→ " + ("La organización RESPONDE BIEN a su entorno" if total > 2.5 else
              "La organización RESPONDE MAL a su entorno: hay oportunidades no capturadas "
              "y amenazas no atendidas"))
    m.to_csv(f"PE02_matriz_{nombre.lower()}.csv", index=False)
