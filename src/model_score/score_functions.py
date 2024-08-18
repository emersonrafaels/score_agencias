import pandas as pd
from loguru import logger

from src.model_score import normalization_functions


def group_dataframe(
    df,
    list_columns_group,
    aggregation_type="size",
    name_column_result="Quantidade",
    column_to_aggregate=None,
):
    """
    AGRUPA OS DADOS DO DATAFRAME POR COLUNAS ESPECIFICADAS E REALIZA OPERAÇÃO DE AGREGAÇÃO ESPECÍFICA.

    # Arguments
        df                   - Required: Dataframe a ser agrupado (pd.DataFrame)
        list_columns_group   - Required: Colunas usadas para agrupar os dados (List[str] | str)
        aggregation_type     - Optional: Tipo de agregação ('size', 'sum', 'mean') (str)
        name_column_result   - Optional: Nome da coluna de resultado que
                                         armazenará o resultado
                                         da agregação (str)
        column_to_aggregate  - Optional: Coluna sobre a qual a operação de
                                         agregação 'sum' ou 'mean'
                                         será realizada (str)

    # Returns:
        df_group             - Required: Dataframe agrupado com uma nova
                                         coluna indicando o
                                         resultado da agregação (pd.DataFrame)
    """

    # INICIANDO O VALIDATOR DA FUNÇÃO
    validator = False

    if isinstance(list_columns_group, str):
        list_columns_group = [list_columns_group]

    if aggregation_type == "size":
        df_group = (
            df.groupby(list_columns_group).size().reset_index(name=name_column_result)
        )

        validator = True

    elif aggregation_type in ["sum", "mean"] and column_to_aggregate is not None:
        if aggregation_type == "sum":
            df_group = (
                df.groupby(list_columns_group)
                .sum()[column_to_aggregate]
                .reset_index(name=name_column_result)
            )

            validator = True

        elif aggregation_type == "mean":
            df_group = (
                df.groupby(list_columns_group)
                .mean()[column_to_aggregate]
                .reset_index(name=name_column_result)
            )

            validator = True

    else:
        logger.error(
            "Invalid aggregation type or column_to_aggregate not provided for sum or mean aggregation."
        )

    if validator:
        logger.info(
            "AGRUPAMENTO REALIZADO COM SUCESSO: AGREGAÇÃO: {} - COLUNAS DE AGRUPAMENTO: {} - COLUNAS DE AGREGAÇÃO: {} - NOME DA COLUNA RESULTANTE: {}".format(
                aggregation_type,
                list_columns_group,
                column_to_aggregate,
                name_column_result,
            )
        )

    return df_group


def apply_weight(
    row, column_value=None, column_weight=None, weight_false=1, weight_true=1
):
    """
    APLICA UM PESO ESPECÍFICO A UM VALOR DE COLUNA
    BASEADO EM UMA CONDIÇÃO ESPECIFICADA POR OUTRA COLUNA.

    A FUNÇÃO VERIFICA SE AS COLUNAS ESPECIFICADAS
    EXISTEM E APLICA OS PESOS CORRESPONDENTES
    BASEADO NO VALOR BOOLEANO DA COLUNA DE PESO.

    # Arguments
        row                  - Required: A linha do DataFrame ou um
                                         dicionário contendo os dados (pd.Series | dict)
        column_value         - Optional: O nome da coluna cujo
                                         valor será ponderado (str)
        column_weight        - Optional: O nome da coluna que determina
                                         se o peso 'weight_true' ou 'weight_false'
                                         será aplicado (str)
        weight_false         - Optional: O peso a ser aplicado se o valor
                                         em 'column_weight' é falso ou
                                         corresponde a uma string que
                                         representa falso (1 por padrão)
                                         (int | float)
        weight_true          - Optional: O peso a ser aplicado se o valor
                                          em 'column_weight'
                                          é verdadeiro (1 por padrão)
                                          (int | float)

    # Returns:
        weighted_value       - Required: O valor ponderado resultante ou None
                                          se ocorrer um erro ou
                                          se as colunas especificadas
                                          não existirem (float | None)

    # Example:
        row = pd.Series({'Age': 25, 'Member': 'Yes'})
        result = apply_weight(row, column_value='Age',
                              column_weight='Member',
                              weight_false=0.8,
                              weight_true=1.2)
        print(result)  # Saída esperada: 30.0
    """

    # VERIFICANDO SE A COLUNA ESTÁ NAS COLUNAS DO ROW
    if isinstance(row, (pd.Series, dict)):
        # VERIFICANDO SE AS COLUNAS EXISTEM NO DATAFRAME
        for column in [column_value, column_weight]:
            if column not in row:
                logger.error(f"A coluna '{column}' não existe no DataFrame.")
                return None

        if row[column_weight] in [False, "Não", "NÃO", "Nao", "NAO"]:
            return row[column_value] * weight_false
        else:
            return row[column_value] * weight_true
    return column_value


def apply_weights(
    row,
    column_value=None,
    weights={},
):
    """
    APLICA UM PESO ESPECÍFICO A UM VALOR DE COLUNA
    BASEADO EM UMA CONDIÇÃO ESPECIFICADA POR OUTRA COLUNA.

    A FUNÇÃO VERIFICA SE AS COLUNAS ESPECIFICADAS
    EXISTEM E APLICA OS PESOS CORRESPONDENTES
    BASEADO NO VALOR BOOLEANO DA COLUNA DE PESO.

    # Arguments
        row                  - Required: A linha do DataFrame ou um
                                         dicionário contendo os dados (pd.Series | dict)
        column_value         - Optional: O nome da coluna cujo
                                         valor será ponderado (str)
        weights              - Optional: Dict contendo todos os pesos
                                         que serão aplicados.
                                         O padrão do dict é: (Dict)

    # Returns:
        weighted_value       - Required: O valor ponderado resultante ou None
                                          se ocorrer um erro ou
                                          se as colunas especificadas
                                          não existirem (float | None)

    # Example:

    """

    # INICIANDO A VARIÁVEL DE RETORNO
    result = 1

    # VERIFICANDO SE WEIGHTS É UM DICT
    if isinstance(weights, dict):
        # VERIFICANDO SE FOI PASSADO UMA ROW DO TIPO SERIES OU DICT
        if isinstance(row, (pd.Series, dict)):
            # VERIFICANDO SE AS COLUNAS DE VOLUME ESTÁ NO DATAFRAME
            if column_value in row:
                # PERCORRENDO CADA UMA DAS COLUNAS DO DICT WEIGHT
                for key, value in weights.items():
                    # VERIFICANDO SE A COLUNA CONSTA NA LINHA
                    if key in row:
                        # VERIFICANDO SE É UMA VARIÁVEL DE PESO POR TEMPO
                        if "TEMPO" in list(value.keys()):
                            pass
                        else:
                            # result = column_value*value_weight
                            result *= value.get(row[key], 0) * row.get(column_value, 0)

    return result


def get_score(
    df,
    normalize_to_high_score=False,
    name_column_value="Quantidade",
    name_column_result="Score_Normalizado",
    list_columns_group_result=None,
):
    """
    CALCULA O SCORE NORMALIZADO BASEADO EM UMA COLUNA DE VALORES DO DATAFRAME.

    # Arguments
        df                        - Required: Dataframe contendo os dados (pd.DataFrame)
        normalize_to_high_score   - Required: Define o padrão de normalização (Boolean)
        name_column_value         - Optional: Nome da coluna do dataframe de
                                                                      onde os valores serão utilizados
                                                                      para calcular o score (str)
        name_column_result        - Optional: Nome da coluna onde os
                                                                      resultados do score
                                                                      serão armazenados (str)
        list_columns_group_result - Optional: Se desejado,
                                              realiza o agrupamento das
                                              colunas mencionadas após a normalização.
                                              Se não for desejado agrupar,
                                              manter None (Tuple | List)

    # Returns:get_score
        df                         - Required: Dataframe com uma nova coluna de
                                               scores normalizados (pd.DataFrame)
    """

    # INICIANDO O DICT QUE ARMAZENA OS RESULTADOS
    dict_result = {}

    # ARMAZENANDO O DATAFRAME COM OS VALORES PONDERADOS
    dict_result["DATAFRAME_PONDERADO"] = df.copy()

    if list_columns_group_result:
        # AGRUPANDO OS DADOS
        df = group_dataframe(
            df=df,
            aggregation_type="mean",
            list_columns_group=list_columns_group_result,
            name_column_result=name_column_result,
            column_to_aggregate=name_column_value,
        )

    # ARMAZENANDO O DATAFRAME APÓS O GROUPBY
    dict_result["DATAFRAME_RESULT_GROUP"] = df.copy()

    if normalize_to_high_score:
        # VALORES MENOR -> MAIORES NOTAS
        df[name_column_result] = normalization_functions.normalize_to_high_score(
            df[name_column_result]
        )
    else:
        # VALORES MENOR -> MENORES NOTAS
        df[name_column_result] = normalization_functions.normalize_to_low_score(
            df[name_column_result]
        )

    # ARMAZENANDO O DATAFRAME COM OS VALORES DE PONDERAÇÃO NORMALIZADOS
    dict_result["DATAFRAME_SCORE"] = df.copy()

    return df
