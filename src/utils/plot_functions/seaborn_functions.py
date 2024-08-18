from functools import wraps

import matplotlib.pyplot as plt
import seaborn as sns


def save_plot(file_path="plot.png"):
    """
    Decorator that saves a matplotlib plot to a specified file path.

    Parameters:
    file_path (str): Path where the plot will be saved.

    Returns:
    Decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute the plotting function and retrieve the plt object
            plt = func(*args, **kwargs)

            # Save the figure
            plt.savefig(file_path)
            plt.close()  # Close the figure to free up memory

            return plt

        return wrapper

    return decorator


# Applying the decorator to the boxplot function
@save_plot(file_path="my_boxplot.png")
def boxplot(df, cols, title, color_points=False):
    """
    Gera boxplots com identificação de pontos para uma ou várias colunas de um DataFrame,
    com a opção de colorir os pontos individualmente.

    Parameters:
    df (pd.DataFrame): DataFrame contendo os dados a serem plotados.
    cols (str or list of str): Nome(s) da(s) coluna(s) no DataFrame para plotar o boxplot.
                               Pode ser uma string para uma única coluna ou uma lista de strings para múltiplas colunas.
    title (str): Título do gráfico.
    color_points (bool): Se True, cada ponto é colorido individualmente. Se False, todos os pontos são da mesma cor.

    Returns:
    None: A função apenas exibe o gráfico.
    """
    # Configuração do tamanho e título do gráfico
    plt.figure(figsize=(12, 8))
    plt.suptitle(title)

    # Convertendo cols para uma lista se for uma única string
    if isinstance(cols, str):
        cols = [cols]

    # Determina o número de linhas necessárias com base no número de colunas
    num_cols = len(cols)
    num_rows = (
        num_cols + 1
    ) // 2  # Garante que tenhamos no máximo 2 gráficos por linha

    # Criação de uma paleta de cores para cada ponto, se necessário
    if color_points:
        palette = sns.color_palette("hsv", len(df))
    else:
        palette = "deep"  # Usando uma cor padrão se color_points é False

    # Criando um boxplot para cada coluna
    for i, col in enumerate(cols):
        ax = plt.subplot(
            num_rows, 2, i + 1
        )  # Organiza os plots em várias linhas se necessário
        sns.boxplot(x=df[col], color="lightblue", fliersize=0)  # Oculta os fliers
        sns.stripplot(
            x=df[col],
            palette=palette,
            jitter=True,
            size=5,
            edgecolor="gray",
            marker="o",
            ax=ax,
        )
        plt.title(col)  # Configura o título do subplot
        plt.xlabel("")  # Remove o label do eixo x

    # Ajuste da layout para evitar sobreposição do título
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Retorno do gráfico
    return plt
