# KPI Dashboard — Reservas de Rent-a-Car (SJO)

Análisis de indicadores clave de desempeño (KPIs) aplicado a un manifiesto real de **1,019 reservas** de una semana (02–09 de agosto 2026) en el Aeropuerto Internacional Juan Santamaría, Costa Rica.

**Temática: KPIs** — el proyecto explica qué es un KPI, la diferencia entre métrica y KPI, ejemplos por área de negocio y aplica **10 KPIs** con datos reales.

## 📊 Dashboard en vivo
👉 https://josean03.github.io/kpi-reservations-dashboard/

## 🔑 KPIs principales de la semana
| KPI | Valor |
|---|---|
| Reservas totales | 1,019 (127/día) |
| Tarifa promedio (ADR) | $51.66 |
| Revenue estimado | $453,718 |
| Duración promedio | 8.8 días |
| Anticipación (lead time) | 43.8 días |
| Clientes contactados | 0% ⚠️ |

**Insight clave:** el 100% de las reservas está sin contacto con el cliente → confirmarlas reduce no-shows y abre la puerta a upgrades (más revenue).

## 📁 Estructura
```
├── index.html              # Dashboard completo (autocontenido, sin conexión requerida)
├── analizar.py             # Análisis de KPIs en Python (pandas + matplotlib)
├── kpis.json               # Resultados del análisis
├── data/reservas.csv       # Datos anonimizados (sin nombres de clientes)
├── charts/                 # Gráficos generados
└── docs/KPI_Guia_Estudio.pdf  # Guía de estudio: qué es un KPI, métrica vs KPI, 10 KPIs
```

## 🛠️ Cómo reproducir
```bash
pip install pandas matplotlib
python analizar.py
```

## 🧠 Aprendizajes incluidos
- Qué es un KPI y cuándo una métrica se convierte en KPI
- Ejemplos por área: ventas, marketing, operaciones y RRHH
- 10 KPIs del día a día de un analista de datos en rent-a-car

---
*Proyecto de portafolio — José Andrés Sequeira · Datos anonimizados por privacidad*
