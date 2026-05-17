import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# =========================================================
# DETECCIÓN DE AUTOPISTA GLOBAL
# =========================================================
def detectar_autopista_global(archivos, excluir="1barrera"):
    E_comun = np.linspace(0, 0.5, 2000)

    datos_interp = []

    for archivo in archivos:
        nombre = os.path.basename(archivo)

        if excluir in nombre.lower():
            print(f"Excluyendo {nombre}")
            continue

        df = pd.read_csv(
            archivo,
            sep=r'\s*,\s*',
            engine='python',
            skiprows=3,
            names=['Transmission', 'Energy']
        )

        df = df.apply(pd.to_numeric, errors='coerce').dropna()

        T_interp = np.interp(E_comun, df['Energy'], df['Transmission'])
        datos_interp.append(T_interp)

    datos_interp = np.array(datos_interp)

    umbral = 0.1
    mask_global = np.all(datos_interp > umbral, axis=0)

    autopistas = []

    if mask_global.any():
        grupos = (mask_global != np.roll(mask_global, 1)).cumsum()

        for g in np.unique(grupos):
            region = (grupos == g) & mask_global

            if np.sum(region) > 10:
                e_ini = E_comun[region].min()
                e_fin = E_comun[region].max()
                autopistas.append((e_ini, e_fin))

    return E_comun, autopistas


# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================
def analizar_memristor_fungico(directorio_txt):

    archivos = sorted(glob.glob(os.path.join(directorio_txt, "*.[ct][sx][vt]")))

    if not archivos:
        print("No se encontraron archivos")
        return

    print(f"\n--- Analizando {len(archivos)} archivos ---\n")

    plt.style.use('seaborn-v0_8-whitegrid')

    resultados = []

    # =====================================================
    # FIGURAS INDIVIDUALES (TIPO PAPER)
    # =====================================================
    for archivo in archivos:
        try:
            df = pd.read_csv(
                archivo,
                sep=r'\s*,\s*',
                engine='python',
                skiprows=3,
                names=['Transmission', 'Energy']
            )

            df = df.apply(pd.to_numeric, errors='coerce').dropna()

            nombre = os.path.basename(archivo)

            # -------- detectar minibandas ----------
            umbral = 0.1
            mask = df['Transmission'] > umbral

            minibandas = []

            if mask.any():
                grupos = (mask != mask.shift()).cumsum()

                for g in df[mask].groupby(grupos):
                    banda = g[1]
                    e_ini = banda['Energy'].min()
                    e_fin = banda['Energy'].max()
                    t_max = banda['Transmission'].max()

                    minibandas.append((e_ini, e_fin, t_max))

                    resultados.append({
                        "archivo": nombre,
                        "E_inicio": e_ini,
                        "E_fin": e_fin,
                        "T_max": t_max
                    })

            # -------- gráfica ----------
            fig, ax = plt.subplots(figsize=(8, 5))

            ax.semilogy(df['Energy'], df['Transmission'], color='black', linewidth=2)

            for (e_ini, e_fin, _) in minibandas:
                ax.axvspan(e_ini, e_fin, alpha=0.25)

            ax.axhline(umbral, linestyle='--')

            ax.set_title(f"Quantum Transport\n{nombre}", fontsize=12)
            ax.set_xlabel("Energy (eV)")
            ax.set_ylabel("Transmission (log)")

            ax.set_xlim(0, 0.5)
            ax.set_ylim(1e-12, 1)

            ax.grid(True, which='both', alpha=0.2)

            plt.tight_layout()

            plt.savefig(nombre.replace(".txt", ".png"), dpi=300)
            plt.close()

            print(f"OK: {nombre}")

        except Exception as e:
            print(f"Error en {archivo}: {e}")

    # =====================================================
    # COMPARATIVA NORMALIZADA
    # =====================================================
    plt.figure(figsize=(10, 6))

    for archivo in archivos:
        df = pd.read_csv(
            archivo,
            sep=r'\s*,\s*',
            engine='python',
            skiprows=3,
            names=['Transmission', 'Energy']
        )

        df = df.apply(pd.to_numeric, errors='coerce').dropna()

        nombre = os.path.basename(archivo)

        T_norm = df['Transmission'] / df['Transmission'].max()

        plt.plot(df['Energy'], T_norm, label=nombre)

    plt.title("Comparativa Normalizada")
    plt.xlabel("Energy (eV)")
    plt.ylabel("Transmission (normalizada)")
    plt.legend(fontsize=8)

    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("comparativa.png", dpi=300)
    plt.show()

    # =====================================================
    # AUTOPISTA GLOBAL
    # =====================================================
    E_comun, autopistas = detectar_autopista_global(archivos)

    plt.figure(figsize=(10, 6))

    for archivo in archivos:
        nombre = os.path.basename(archivo)

        if "1barrera" in nombre.lower():
            continue

        df = pd.read_csv(
            archivo,
            sep=r'\s*,\s*',
            engine='python',
            skiprows=3,
            names=['Transmission', 'Energy']
        )

        df = df.apply(pd.to_numeric, errors='coerce').dropna()

        plt.semilogy(df['Energy'], df['Transmission'], alpha=0.5)

    for (e_ini, e_fin) in autopistas:
        plt.axvspan(e_ini, e_fin, alpha=0.3)

    plt.title("Autopista Cuántica Global")
    plt.xlabel("Energy (eV)")
    plt.ylabel("Transmission (log)")

    plt.xlim(0, 0.5)
    plt.ylim(1e-12, 1)

    plt.grid(True, which='both', alpha=0.2)

    plt.tight_layout()
    plt.savefig("autopista_global.png", dpi=300)
    plt.show()

    # =====================================================
    # EXPORTAR RESULTADOS
    # =====================================================
    if resultados:
        df_res = pd.DataFrame(resultados)
        df_res.to_csv("minibandas.csv", index=False)
        print("\nArchivo generado: minibandas.csv")


# =========================================================
# EJECUCIÓN DIRECTA (TU RUTA)
# =========================================================
ruta = r"C:\Users\shara\Desktop\Electronica Fisica\Trabajo"

analizar_memristor_fungico(ruta)