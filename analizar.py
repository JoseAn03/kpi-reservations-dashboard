# -*- coding: utf-8 -*-
"""Análisis de KPIs del manifiesto de reservas (semana 02-09 ago 2026)."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

df = pd.read_csv('reservas.csv')
# limpiar columnas
df = df.loc[:, ~df.columns.str.startswith('Unnamed')]
df = df[[c for c in df.columns if str(c).strip() != '']]
df.columns = [str(c).strip() for c in df.columns]
df = df.rename(columns={
    'N.º reserva': 'reserva',
    'Fact.': 'facturacion',
    'Clase': 'clase',
    'N.º unidad': 'unidad',
    'Fecha recogida': 'fecha_recogida',
    'Fecha entrega': 'fecha_entrega',
    'Ubic. rec.': 'ubic_rec',
    'Ubic. ent.': 'ubic_ent',
    'Código de tarifa': 'tarifa_codigo',
    'Tarifa diaria': 'tarifa_diaria',
    'Nº de vuelo': 'vuelo',
    'Fecha de reserva': 'fecha_reserva',
    'Reservado por': 'canal',
    'Agencia de recom.': 'agencia',
    'Notas': 'notas',
    'Cliente Contactado': 'contactado',
})
df = df.drop(columns=[c for c in df.columns if c.startswith('col') or c == ''], errors='ignore')

def parse_fecha(s):
    try:
        return pd.to_datetime(s, format='%d/%m/%Y %H:%M')
    except Exception:
        try:
            return pd.to_datetime(s, format='%d/%m/%Y')
        except Exception:
            return pd.NaT

df['recogida'] = df['fecha_recogida'].apply(parse_fecha)
df['entrega'] = df['fecha_entrega'].apply(parse_fecha)
df['fecha_res'] = df['fecha_reserva'].apply(parse_fecha)
df['tarifa_diaria'] = pd.to_numeric(df['tarifa_diaria'], errors='coerce')
df['duracion_dias'] = (df['entrega'] - df['recogida']).dt.total_seconds() / 86400
df['lead_time_dias'] = (df['recogida'] - df['fecha_res']).dt.total_seconds() / 86400
df['revenue_est'] = df['tarifa_diaria'] * df['duracion_dias']

kpis = {}
kpis['total_reservas'] = int(len(df))
kpis['rango'] = f"{df['recogida'].min().strftime('%d/%m/%Y')} - {df['recogida'].max().strftime('%d/%m/%Y')}"
kpis['dias'] = int(df['recogida'].dt.date.nunique())
kpis['reservas_por_dia'] = round(len(df) / df['recogida'].dt.date.nunique(), 1)
kpis['tarifa_promedio'] = round(df['tarifa_diaria'].mean(), 2)
kpis['tarifa_mediana'] = round(df['tarifa_diaria'].median(), 2)
kpis['revenue_estimado'] = round(df['revenue_est'].sum(), 2)
kpis['duracion_promedio'] = round(df['duracion_dias'].mean(), 2)
kpis['lead_time_promedio'] = round(df['lead_time_dias'].mean(), 1)
kpis['contactado_pct'] = round((df['contactado'].str.strip() != 'NC').mean() * 100, 1)
kpis['top_clase'] = df['clase'].value_counts().index[0]
kpis['top_canal'] = df['canal'].value_counts().index[0]
kpis['pct_nc'] = round((df['contactado'].str.strip() == 'NC').mean() * 100, 1)
print(json.dumps(kpis, indent=1))

# ---- graficos ----
plt.rcParams['font.family'] = 'DejaVu Sans'

# 1. Reservas por dia
por_dia = df.groupby(df['recogida'].dt.date).size()
fig, ax = plt.subplots(figsize=(8,4.2), dpi=150)
ax.bar([d.strftime('%d/%m') for d in por_dia.index], por_dia.values, color='#4472C4', edgecolor='black', linewidth=0.6)
for x, v in zip(range(len(por_dia)), por_dia.values):
    ax.text(x, v+3, str(v), ha='center', fontsize=9)
ax.set_title('Reservas por día de recogida', fontsize=11)
ax.set_ylabel('N.º de reservas')
ax.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout(); plt.savefig('chart_reservas_dia.png', dpi=150); plt.close()

# 2. Revenue estimado por dia
rev_dia = df.groupby(df['recogida'].dt.date)['revenue_est'].sum()
fig, ax = plt.subplots(figsize=(8,4.2), dpi=150)
ax.bar([d.strftime('%d/%m') for d in rev_dia.index], rev_dia.values, color='#70AD47', edgecolor='black', linewidth=0.6)
for x, v in zip(range(len(rev_dia)), rev_dia.values):
    ax.text(x, v+80, f'${v:,.0f}'.replace(',', ' '), ha='center', fontsize=8.5)
ax.set_title('Revenue estimado por día de recogida (USD)', fontsize=11)
ax.set_ylabel('USD')
ax.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout(); plt.savefig('chart_revenue_dia.png', dpi=150); plt.close()

# 3. Tarifa promedio por clase
tar_clase = df.groupby('clase')['tarifa_diaria'].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8,4.2), dpi=150)
ax.bar(tar_clase.index, tar_clase.values, color='#ED7D31', edgecolor='black', linewidth=0.6)
for x, v in zip(range(len(tar_clase)), tar_clase.values):
    ax.text(x, v+0.8, f'${v:.2f}'.replace('.', ','), ha='center', fontsize=8)
ax.set_title('Tarifa diaria promedio por clase de vehículo', fontsize=11)
ax.set_ylabel('USD / día')
ax.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout(); plt.savefig('chart_tarifa_clase.png', dpi=150); plt.close()

# 4. Mix de flota (top 8 clases)
mix = df['clase'].value_counts().head(8)
fig, ax = plt.subplots(figsize=(8,4.2), dpi=150)
ax.barh(mix.index[::-1], mix.values[::-1], color='#FFC000', edgecolor='black', linewidth=0.6)
for y, v in zip(range(len(mix)), mix.values[::-1]):
    ax.text(v+5, y, str(v), va='center', fontsize=9)
ax.set_title('Mix de flota: reservas por clase (top 8)', fontsize=11)
ax.set_xlabel('N.º de reservas')
ax.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout(); plt.savefig('chart_mix_flota.png', dpi=150); plt.close()

# 5. Reservas por canal
canal = df['canal'].value_counts().head(6)
fig, ax = plt.subplots(figsize=(8,4.2), dpi=150)
ax.bar(canal.index, canal.values, color='#A5A5A5', edgecolor='black', linewidth=0.6)
for x, v in zip(range(len(canal)), canal.values):
    ax.text(x, v+8, str(v), ha='center', fontsize=9)
ax.set_title('Reservas por canal de reserva', fontsize=11)
ax.set_ylabel('N.º de reservas')
ax.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout(); plt.savefig('chart_canal.png', dpi=150); plt.close()

# 6. Histograma duracion de renta
fig, ax = plt.subplots(figsize=(8,4.2), dpi=150)
ax.hist(df['duracion_dias'], bins=15, color='#5B9BD5', edgecolor='black', linewidth=0.6)
ax.set_title('Distribución de la duración de renta (días)', fontsize=11)
ax.set_xlabel('Días'); ax.set_ylabel('Frecuencia')
ax.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout(); plt.savefig('chart_duracion.png', dpi=150); plt.close()

# 7. Lead time
fig, ax = plt.subplots(figsize=(8,4.2), dpi=150)
ax.hist(df['lead_time_dias'].clip(0, 90), bins=20, color='#9B5DE5', edgecolor='black', linewidth=0.6)
ax.set_title('Anticipación de la reserva (lead time en días)', fontsize=11)
ax.set_xlabel('Días entre reserva y recogida'); ax.set_ylabel('Frecuencia')
ax.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout(); plt.savefig('chart_leadtime.png', dpi=150); plt.close()

json.dump(kpis, open('kpis.json', 'w'))
print('GRAFICOS + KPIS OK')
