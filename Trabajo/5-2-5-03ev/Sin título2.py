import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

def analizar_bandas_paper(directorio):
    archivos = sorted(glob.glob(os.path.join(directorio, "*.txt")))
    
    if not archivos:
        print("No se encontraron archivos .txt en la ruta.")
        return


    # =====================================================
    # CONFIGURACIÓN ESTÉTICA (PAPER-READY)
    # =====================================================
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.linewidth': 1.2,
        'legend.fontsize': 10,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'xtick.top': True,
        'ytick.right': True,
        'figure.dpi': 300,
        'savefig.bbox': 'tight'
    })
    
    # Paleta de colores sobria
    colores = ['#000000', '#d62728', '#1f77b4', '#2ca02c', '#9467bd']

    # =====================================================
    # FIGURA 1: SUBPLOTS APILADOS (Evolución de Kronig-Penney)
    # =====================================================
    fig, axes = plt.subplots(len(archivos), 1, figsize=(7, 2 * len(archivos)), sharex=True)
    if len(archivos) == 1: axes = [axes]
    
    for i, (archivo, ax) in enumerate(zip(archivos, axes)):
        nombre = os.path.basename(archivo).replace('.txt', '')
        
        # Lectura de datos
        df = pd.read_csv(archivo, sep=r',\s*', engine='python', skiprows=3, names=['Transmission', 'Energy'])
        df = df.apply(pd.to_numeric, errors='coerce').dropna()
        df['Transmission'] = np.clip(df['Transmission'], 1e-15, 1)

        # Ploteo de la curva
        ax.semilogy(df['Energy'], df['Transmission'], color=colores[i % len(colores)], linewidth=1.5, label=nombre)
        
        # Sombreado de minibandas (Umbral T > 0.5)
        mask = df['Transmission'] > 0.5
        if mask.any():
            grupos = (mask != mask.shift()).cumsum()
            for _, banda in df[mask].groupby(grupos):
                ax.axvspan(banda['Energy'].min(), banda['Energy'].max(), color='gray', alpha=0.25, lw=0)

        # Formato de cada subplot
        ax.set_ylim(1e-6, 2)
        ax.grid(True, which='both', linestyle=':', alpha=0.4)
        ax.legend(loc='lower right', frameon=False)
        ax.set_ylabel("Transmission")
        
        # Solo poner la etiqueta X en el último gráfico
        if i == len(archivos) - 1:
            ax.set_xlabel("Energy (eV)")

    plt.subplots_adjust(hspace=0.05) # Juntar los gráficos para comparar mejor las bandas
    plt.savefig("Fig1_Subplots_Evolucion.png")
    plt.close()

    # =====================================================
    # FIGURA 2: OVERLAY COMBINADO
    # =====================================================
    plt.figure(figsize=(7, 5))
    
    for i, archivo in enumerate(archivos):
        nombre = os.path.basename(archivo).replace('.txt', '')
        
        df = pd.read_csv(archivo, sep=r',\s*', engine='python', skiprows=3, names=['Transmission', 'Energy'])
        df = df.apply(pd.to_numeric, errors='coerce').dropna()
        df['Transmission'] = np.clip(df['Transmission'], 1e-15, 1)

        plt.semilogy(df['Energy'], df['Transmission'], color=colores[i % len(colores)], linewidth=1.2, alpha=0.8, label=nombre)

    plt.xlabel("Energy (eV)")
    plt.ylabel("Transmission Coefficient")
    plt.ylim(1e-6, 2)
    plt.grid(True, which='both', linestyle=':', alpha=0.4)
    plt.legend(loc='lower right', frameon=False)
    
    plt.savefig("Fig2_Overlay_Combinado.png")
    plt.close()
    
    print("¡Listo! Imágenes 'Fig1_Subplots_Evolucion.png' y 'Fig2_Overlay_Combinado.png' generadas.")

# =========================================================
# EJECUCIÓN DIRECTA
# =========================================================
ruta = r"C:\Users\shara\Desktop\Electronica Fisica\Trabajo"
analizar_bandas_paper(ruta)