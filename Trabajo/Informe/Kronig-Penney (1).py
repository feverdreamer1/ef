import numpy as np
import matplotlib.pyplot as plt

# 1. Constantes físicas Universales
m_e = 9.109e-31      # Masa del electrón libre (kg)
hbar = 1.054e-34     # Constante reducida de Planck (J*s)
eV = 1.602e-19       # Factor de conversión eV a Julios

# 2. Parámetros de vuestra simulación
m_star = 0.067 * m_e # Masa efectiva del GaAs
L = 5e-9             # Anchura del pozo (5 nm)
b = 2e-9             # Anchura de la barrera (2 nm)
V0 = 0.4 * eV        # Altura de la barrera (0.4 eV pasados a Julios)

# 3. Vector de energía
# Evitamos el 0 exacto y el 0.4 exacto para evitar divisiones por cero en kappa o k
energia_eV = np.linspace(0.001, 0.399, 2000)
energia_J = energia_eV * eV

# 4. Cálculo de k y kappa
k = np.sqrt(2 * m_star * energia_J) / hbar
kappa = np.sqrt(2 * m_star * (V0 - energia_J)) / hbar

# 5. La función trascendental f(E) de Kronig-Penney
termino1 = np.cos(k * L) * np.cosh(kappa * b)
termino2 = ((kappa**2 - k**2) / (2 * k * kappa)) * np.sin(k * L) * np.sinh(kappa * b)
f_E = termino1 + termino2

# 6. Representación Gráfica
plt.figure(figsize=(10, 5))
plt.plot(energia_eV, f_E, color='black', label=r'$f(E)$ de Kronig-Penney')

# Dibujar las franjas de condición |f(E)| <= 1
plt.axhline(y=1, color='red', linestyle='--', label=r'Límite $+1$')
plt.axhline(y=-1, color='red', linestyle='--')
plt.fill_between(energia_eV, -1, 1, color='green', alpha=0.1, label='Bandas Permitidas')

# Formato
plt.ylim(-3, 3) # Recortamos el eje Y para ver bien la intersección
plt.xlim(0, 0.4)
plt.xlabel('Energía (eV)', fontsize=12)
plt.ylabel(r'$f(E)$', fontsize=12)
plt.title('Solución Gráfica del Modelo de Kronig-Penney', fontsize=14)
plt.grid(True, alpha=0.5)
plt.legend(loc='upper right')

plt.tight_layout()
plt.savefig('Solucion_Kronig_Penney.png', dpi=300)
plt.show()

# --- EXTRACCIÓN NUMÉRICA DE LAS BANDAS ---

# 1. Creamos una máscara booleana: True donde está en la zona verde, False donde no
dentro_de_banda = np.abs(f_E) <= 1

# 2. Buscamos los índices donde la curva "cruza" la frontera (cambia de True a False o viceversa)
cruces = np.where(dentro_de_banda[:-1] != dentro_de_banda[1:])[0]

print("\n--- VALORES NUMÉRICOS DE KRONIG-PENNEY ---")
print("Las bandas de conducción permitidas están en los rangos:")

# 3. Emparejamos los cruces para definir el inicio y fin de cada banda
for i in range(0, len(cruces), 2):
    E_inicio = energia_eV[cruces[i]]
    
    # Si hay un cruce de salida, lo cogemos. Si no, la banda llega hasta el límite de 0.4 eV
    if i + 1 < len(cruces):
        E_fin = energia_eV[cruces[i+1]]
        print(f"- Banda {i//2 + 1}: de {E_inicio:.4f} eV a {E_fin:.4f} eV")
    else:
        print(f"- Banda {i//2 + 1}: de {E_inicio:.4f} eV hasta 0.4000 eV (Límite de barrera)")