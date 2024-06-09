import numpy as np

from utils.generic_functions import check_none


def calculate_outliers(data, method="IQR"):
    """
    Calcula os outliers em um conjunto de dados.

    Métodos disponíveis:
        - Intervalo Interquartil (IQR).

        O método IQR define outliers como aqueles
        elementos que estão:
            Lim inferior: Abaixo de Q1 - 1.5*IQR
            Lim superior: Acima de Q3 + 1.5*IQR

    # Arguments
        data            - Required: Lista ou array de dados numéricos onde
                                    os outliers serão calculados. (Array)

        method          - Optional: Método utilizado para calcular os outliers.
                                    Por padrão, é "IQR". (str)

    # Returns
        lower_outliers  - Required: Array booleano que indica quais valores
                                    estão abaixo do limite inferior de outliers. (Array)
        upper_outliers  - Required: Array booleano que indica quais valores
                                    estão acima do limite superior de outliers. (Array)

    Examples
    --------
    >>> data = [1, 2, 3, 4, 100, 101, 102]
    >>> lower_outliers, upper_outliers = calculate_outliers(data)
    >>> print(lower_outliers)
    [False False False False False False False]
    >>> print(upper_outliers)
    [False False False False  True  True  True]
    """

    lower_outliers = np.min(data)
    upper_outliers = np.max(data)

    if method in ["IQR"]:
        # CALCULANDO Q1, Q3 E IQR
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1
        outlier_step = 1.5 * IQR

        # IDENTIFICANDO OUTLIERS
        lower_bound = Q1 - outlier_step
        upper_bound = Q3 + outlier_step

        # MARCANDO OS OUTLIERS
        lower_outliers = data < lower_bound
        upper_outliers = data > upper_bound

    return lower_outliers, upper_outliers


def normalize_to_high_score(values):
    """
    NORMALIZA UMA LISTA DE VALORES DE MODO
    QUE O MENOR VALOR RECEBA A MAIOR PONTUAÇÃO (10).

    VALORES MAIS ALTOS RECEBEM PONTUAÇÕES
    MAIS BAIXAS EM UMA ESCALA DE 0 A 10.

    # Arguments
        values              - Required: Lista de valores numéricos a serem normalizados (List[int | float])

    # Returns:
        normalized_values   - Required: Lista de valores normalizados onde o menor valor recebe a pontuação máxima (10) (List[float])

    # Example:
        >>> normalize_to_high_score([10, 20, 15, 5, 30])
        [8.0, 4.0, 6.0, 10.0, 0.0]
    """

    if isinstance(values, np.ndarray):
        return 10 - values
    else:
        return [10 - val for val in values]


def robust_normalizaton(values, option_normalize_to_high_score=False):
    # CONVERTENDO OS DADOS PARA ARRAY NUMPY
    data = np.array(values)

    # CÁLCULO DA MEDIANA E IQR
    median_val = np.median(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    # UTILIZANDO A NORMALIZAÇÃO ROBUSTA
    valores_normalizados = ((data - median_val) / iqr) * 10

    # GARANTINDO DADOS NO INTERVALO 0 A 1
    valores_normalizados_clipped = np.clip(valores_normalizados, 0, 10)

    # NORMALIZA OS VALORES NA ESCALA DE 0 A 10
    if option_normalize_to_high_score:
        return normalize_to_high_score(valores_normalizados_clipped)
    else:
        return valores_normalizados_clipped


def normalize_values(values, option_normalize_to_high_score=False):
    # CONVERTENDO OS DADOS PARA ARRAY NUMPY
    data = np.array(values)

    # OBTENDO MAX E MIN
    max_val = data.max()
    min_val = data.min()

    # VERIFICANDO SE TODOS OS VALORES SÃO IGUAIS
    if max_val == min_val:
        # TODOS SÃO IGUAIS, RETORNA 10 PARA TODOS
        return np.full_like(data, 10.0)

    # NORMALIZA OS VALORES NA ESCALA DE 0 A 10
    if option_normalize_to_high_score:
        return normalize_to_high_score(((data - min_val) / (max_val - min_val)) * 10)
    else:
        return (data - min_val) / (max_val - min_val) * 10


def normalize_data_with_outliers(values, option_normalize_to_high_score=False):
    # CONVERTENDO OS DADOS PARA ARRAY NUMPY
    data = np.array(values)

    # CALCULANDO OUTLIERS
    lower_outliers, upper_outliers = calculate_outliers(data=data)

    # Substituindo outliers
    normalized_data = np.copy(data)

    if option_normalize_to_high_score:
        normalized_data[lower_outliers] = 10  # Outlier inferior para 10
        normalized_data[upper_outliers] = 0  # Outlier superior para 0
    else:
        normalized_data[lower_outliers] = 0  # Outlier inferior para 0
        normalized_data[upper_outliers] = 10  # Outlier superior para 10

    # Normalizando os dados não outliers
    non_outliers = ~lower_outliers & ~upper_outliers

    # Normalizar dados não outlier entre 0 e 10
    normalized_data[non_outliers] = normalize_values(
        normalized_data[non_outliers],
        option_normalize_to_high_score=option_normalize_to_high_score,
    )

    return normalized_data
