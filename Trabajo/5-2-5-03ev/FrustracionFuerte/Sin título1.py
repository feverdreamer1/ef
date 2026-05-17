import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

def comparar_frustracion(directorio):
    archivos = sorted(glob.glob(os.path.join(directorio, "*.txt")))
    
    if len(archivos) != 2:
        print(f"Error: Se necesitan exactamente 2 archivos en la carpeta. Se encontraron {len(archivos)}.")
        return

    print("Generando comparativa de frustración del sistema...")

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

    plt.figure(figsize=(8, 5))
    
    # Colores estratégicos: Negro para el ideal, Rojo para el frustrado
    estilos = [
        {'color': '#333333', 'alpha': 0.8, 'lw': 1.5, 'label': 'Estado Ideal (Simétrico)'},
        {'color': '#d62728', 'alpha': 0.9, 'lw': 1.8, 'label': 'Estado Frustrado (Asimétrico)'}
    ]

    for i, archivo in enumerate(archivos):
        df = pd.read_csv(archivo, sep=r',\s*', engine='python', skiprows=3, names=['Transmision', 'Energia'])
        df = df.apply(pd.to_numeric, errors='coerce').dropna()
        df['Transmision'] = np.clip(df['Transmision'], 1e-15, 1)

        plt.semilogy(
            df['Energia'], 
            df['Transmision'], 
            color=estilos[i]['color'], 
            linewidth=estilos[i]['lw'], 
            alpha=estilos[i]['alpha'], 
            label=estilos[i]['label']
        )
        
        # Sombrear la banda del estado ideal para ver lo que se pierde
        if i == 0:
            mask = df['Transmision'] > 0.5
            if mask.any():
                grupos = (mask != mask.shift()).cumsum()
                for _, banda in df[mask].groupby(grupos):
                    plt.axvspan(banda['Energia'].min(), banda['Energia'].max(), color='gray', alpha=0.15, lw=0)

    # Formato del gráfico
    plt.xlabel("Energía (eV)")
    plt.ylabel("Coeficiente de Transmisión")
    plt.ylim(1e-6, 2)
    plt.xlim(0, 0.5) # Ajusta este límite si tus picos están más a la derecha
    
    plt.grid(True, which='both', linestyle=':', alpha=0.4)
    plt.legend(loc='lower right', frameon=False)
    
    # Anotación para 
    plt.savefig("Fig_Frustracion_Sistema.png")
    plt.show()
    
    print("¡Listo! Imagen 'Fig_Frustracion_Sistema.png' generada.")

# =========================================================
# EJECUCIÓN DIRECTA
# =========================================================
ruta = r"C:\Users\shara\Desktop\Electronica Fisica\Trabajo\5-2-5-03ev\FrustracionFuerte" # Cambia esto a tu carpeta con los 2 txt
comparar_frustracion(ruta)