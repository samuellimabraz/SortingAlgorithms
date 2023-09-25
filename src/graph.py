import pandas as pd
import matplotlib.pyplot as plt

# Carrega o arquivo CSV em um DataFrame do pandas
df = pd.read_csv(
    r"resource\sorting_times.csv"
)

# Cria um gráfico de linhas para cada algoritmo de ordenação
fig, ax = plt.subplots()
for method in df["Sorting Method"].unique():
    method_data = df[df["Sorting Method"] == method]
    ax.plot(method_data["Input Size"], method_data["Execution Time"], label=method)

ax.legend()
ax.set_xlabel("Tamanho do Vetor")
ax.set_ylabel("Tempo de Execução (ms)")
ax.set_title("Desempenho dos Algoritmos de Ordenação")
plt.show()
