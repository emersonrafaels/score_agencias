from utils.generic_functions import check_none


@check_none
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

    max_val = max(values)
    min_val = min(values)
    if max_val == min_val:
        return [10.0] * len(values)  # Todos os valores são iguais
    return [(1 - (val - min_val) / (max_val - min_val)) * 10 for val in values]


@check_none
def normalize_to_low_score(values):
    """
    NORMALIZA UMA LISTA DE VALORES DE MODO
    QUE O MENOR VALOR RECEBA A MENOR PONTUAÇÃO (0).

    VALORES MAIS ALTOS RECEBEM PONTUAÇÕES
    MAIS ALTAS EM UMA ESCALA DE 0 A 10.

    # Arguments
        values              - Required: Lista de valores numéricos a serem normalizados (List[int | float])

    # Returns:
        normalized_values   - Required: Lista de valores normalizados onde o menor valor recebe a pontuação mínima (0) (List[float])

    # Example:
        >>> normalize_to_low_score([10, 20, 15, 5, 30])
        [2.0, 6.0, 4.0, 0.0, 10.0]
    """

    max_val = max(values)
    min_val = min(values)
    if max_val == min_val:
        return [0.0] * len(values)  # Todos os valores são iguais
    return [(val - min_val) / (max_val - min_val) * 10 for val in values]
