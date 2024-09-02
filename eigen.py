import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Configurazione per l'uso di LaTeX nei grafici
rcParams['text.usetex'] = True
rcParams["text.latex.preamble"] = r"\usepackage{amsmath}\usepackage{amsfonts}"

class Eigenfish:
    def __init__(self, matrix, indices_of_ts):
        # Inizializzazione della classe con la matrice e gli indici delle variabili
        self.matrix = matrix
        self.indices_of_ts = indices_of_ts
        self.mdim = matrix.shape[0]
        self.n_t = len(self.indices_of_ts[0])
        self.is_matrix_of_phases = np.all(np.abs(self.matrix) == 1.0)

    def eigvals_random_ts_torus(self, n_ts, radius=1.0):
        # Calcolo degli autovalori per n_ts configurazioni casuali sul toro
        eigenvalues = np.zeros(n_ts * self.mdim, dtype=np.complex64)
        for i in range(n_ts):
            ts = tuple([radius * np.exp(1.j * np.random.uniform(0., 2 * np.pi)) for _ in range(self.n_t)])
            self.matrix[self.indices_of_ts] = ts
            eigenvalues[i * self.mdim:(i + 1) * self.mdim] = np.linalg.eigvals(self.matrix)
        return eigenvalues

    def latex_matrix(self, max_real="1"):
        # Genera una rappresentazione LaTeX della matrice
        def clean(val):
            real, imag = np.real(val), np.imag(val)
            if imag != 0:
                return "i" if imag > 0 else "-i"
            real = str(real).replace(".0", "")
            return real if real in ["0", "0.5", max_real] else "tT"

        template = r" \\ ".join([" & ".join(["{}"] * self.mdim)] * self.mdim)
        filled = template.format(*map(clean, self.matrix.flatten()))
        final = filled.replace("T", "{}").format(*range(1, self.n_t + 1))
        return r"\begin{pmatrix} " + final + r" \end{pmatrix}"

    def create_latex_title_torus(self):
        # Crea un titolo LaTeX per il grafico
        title = (r"\lambda \in \mathbb{C} | \det(A-\lambda I)=0, \quad A="
                 + self.latex_matrix(max_real="0.2")
                 + r", \quad "
                 + ",".join([f"t{n + 1}" for n in range(self.n_t)])
                 + r" \in S^{1} \times S^{1}")
        return f"$ {title} $"

# Codice principale per la creazione del grafico
population = np.array([0., 0., -1.j, 1.j, 0.2])
mdim = 6
n_frames = 100
n_initial_frames = 10
n_matrix = 100000

# Creazione della matrice casuale e selezione degli indici variabili
matrix = np.random.choice(population, (mdim, mdim)) + 0.j
var_indices = np.unravel_index(np.random.choice(np.arange(0, mdim ** 2), 2, replace=False), (mdim, mdim))
eigenfish = Eigenfish(matrix, var_indices)

# Configurazione del grafico
fig, ax = plt.subplots(figsize=(6, 6))  # Grafico quadrato e più piccolo
fig.set_facecolor("#f4f0e8")
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)

# Calcolo e visualizzazione degli autovalori
eigenvalues = eigenfish.eigvals_random_ts_torus(n_matrix)
ax.scatter(np.real(eigenvalues), np.imag(eigenvalues), c="#383b3e", s=0.05, linewidths=0.0001, alpha=1.)

# Impostazione del titolo e delle proprietà del grafico
ax.set_title(eigenfish.create_latex_title_torus(), fontsize=12)
ax.set_aspect('equal', 'box')
ax.set_axis_off()
plt.tight_layout()
plt.show()
