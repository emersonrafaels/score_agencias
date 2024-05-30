from utils.generic_functions import check_none


@check_none
def normalize_to_high_score(values):
    """
    Normaliza uma lista de valores de modo que o menor valor receba a maior pontuação (10).
    Valores mais altos recebem pontuações mais baixas em uma escala de 0 a 10.

    # Arguments:
        values (list): Lista de valores numéricos a serem normalizados.

    # Returns:
        list: Lista de valores normalizados onde o menor valor recebe a pontuação máxima (10).

    Exemplo:
        >>> normalize_to_high_score([10, 20, 15, 5, 30])
        [8.0, 4.0, 6.0, 10.0, 0.0]
    """

    max_val = max(values)
    min_val = min(values)
    if max_val == min_val:
        return [10.0] * len(values)  # Todos os valores são iguais
    return [(1 - (val - min_val) / (max_val - min_val)) * 10 for val in values]


@check_none
def normalize_to_low_score(values):
    """
    Normaliza uma lista de valores de modo que o menor valor receba a menor pontuação (0).
    Valores mais altos recebem pontuações mais altas em uma escala de 0 a 10.

    # Arguments:
        values (list): Lista de valores numéricos a serem normalizados.

    # Returns:
        list: Lista de valores normalizados onde o menor valor recebe a pontuação mínima (0).

    Exemplo:
        >>> normalize_to_low_score([10, 20, 15, 5, 30])
        [2.0, 6.0, 4.0, 0.0, 10.0]
    """
    max_val = max(values)
    min_val = min(values)
    if max_val == min_val:
        return [0.0] * len(values)  # Todos os valores são iguais
    return [(val - min_val) / (max_val - min_val) * 10 for val in values]
