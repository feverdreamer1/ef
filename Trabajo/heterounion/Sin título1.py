import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import re

def simular_simbiosis_rtd(directorio):
    archivos_crudos = glob.glob(os.path.join(directorio, "*.txt"))
    
    if not archivos_crudos:
        print("No se encontraron archivos .txt en la ruta.")
        return

    # =====================================================
    # ORDENAR ARCHIVOS DE MAYOR A MENOR DESALINEACIÓN
    # =====================================================
    def extraer_potencial(ruta_archivo):
        nombre = os.path.basename(ruta_archivo)
        # Extraer números que pueden tener decimales
        numeros = re.findall(r'\d+\.?\d*', nombre)
        return float(numeros[0]) if numeros else 0.0

    # Ordenamos de mayor a menor (0.1, 0.05, 0.01, 0)
    archivos = sorted(archivos_crudos, key=extraer_potencial, reverse=True)
    
    print(f"Archivos detectados y ordenados para la transición:")
    for arch in archivos:
        print(f" - {os.path.basename(arch)} ({extraer_potencial(arch)} eV)")

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

    plt.figure(figsize=(8, 5.5))
    
    # Paleta de degradado: de Rojo (mal) a Verde/Azul (perfecto)
    # Puedes ajustar los colores si prefieres otro estilo
    colores = ['#d62728', '#ff7f0e', '#bcbd22', '#1f77b4'] 
    
    for i, archivo in enumerate(archivos):
        potencial = extraer_potencial(archivo)
        
        # Lectura de datos nanoHUB
        df = pd.read_csv(archivo, sep=r',\s*', engine='python', skiprows=3, names=['Transmision', 'Energia'])
        df = df.apply(pd.to_numeric, errors='coerce').dropna()
        df['Transmision'] = np.clip(df['Transmision'], 1e-15, 1)

        # Destacar el estado de simbiosis (0 eV)
        if potencial == 0.0:
            etiqueta = f"Alineación Perfecta (V = {potencial} eV)"
            grosor = 2.0
            z_order = 10 # Para que se pinte por encima de las demás
            alfa = 1.0
        else:
            etiqueta = f"Desalineado (V = {potencial} eV)"
            grosor = 1.6
            z_order = 5
            alfa = 0.75

        plt.semilogy(
            df['Energia'], 
            df['Transmision'], 
            color=colores[i % len(colores)], 
            linewidth=grosor, 
            alpha=alfa, 
            label=etiqueta,
            zorder=z_order
        )

    # Formato del gráfico
    plt.xlabel("Energía (eV)")
    plt.ylabel("Coeficiente de Transmisión")
    plt.ylim(1e-6, 2)
    # Limitar el eje X ayuda a centrar la atención en los picos de resonancia
    plt.xlim(0.05, 0.45) 
    
    plt.grid(True, which='both', linestyle=':', alpha=0.4)
    plt.legend(loc='lower right', frameon=False, title="Potencial de la Cepa B")
    
    
    plt.savefig("Fig_Simbiosis_RTD.png")
    plt.show()
    
    print("¡Listo! Imagen 'Fig_Simbiosis_RTD.png' generada con éxito.")

# =========================================================
# EJECUCIÓN DIRECTA
# =========================================================
ruta = r"C:\Users\shara\Desktop\Electronica Fisica\Trabajo\heterounion" # <-- ¡Acuérdate de cambiar esto!
simular_simbiosis_rtd(ruta)