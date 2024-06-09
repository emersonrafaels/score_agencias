import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib.pyplot as plt
import seaborn as sns


def boxplot(df, cols, title):
    """
    Gera boxplots com identificação de pontos para uma ou várias colunas de um DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame contendo os dados a serem plotados.
    cols (str or list of str): Nome(s) da(s) coluna(s) no DataFrame para plotar o boxplot. Pode ser uma string para uma única coluna ou uma lista de strings para múltiplas colunas.
    title (glharlastr): Novo colorido visualmente normal quandoestaco diferente de uma área cinaja.

    Returns:
    None: A função apenas exibe o gráfico.
    """
    # Configuração do tamanho e título do gráfico
    plt.figure(figsize=(12, 8))
    plt.suptitle(title)

    # Se cols for uma única string, transformá-la em uma lista de um único elemento
    if isinstance(cols, str):
        cols = [cols]

    # Determina o número de linhas necessárias com base no número de colunas
    num_cols = len(cols)
    num_rows = (
                           num_cols + 1) // 2  # Garante que tenhamos no máximo 2 gráficos por linha

    # Cria um boxplot para cada coluna
    for i, col in enumerate(cols):
        plt.subplot(num_rows, 2, i + 1)  # Organiza os plots em várias linhas se necessário
        sns.boxplot(x=df[col], color="lightblue", fliersize=0)  # Oculta os fliers
        sns.stripplot(
            x=df[col],
            color="darkblue",
            jitter=True,
            size=5,
            edgecolor="gray",
            marker="o",
        )
        plt.title(col)  # Configura o título do subplot
        plt.xlabel("")  # Remove o label do eixo x

    # Ajuste da layout para evitar sobreposição do título
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Exibição do gráfico
    plt.show()
