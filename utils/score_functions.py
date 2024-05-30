import pandas as pd
from loguru import logger

from utils import normalization_functions

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

    if isinstance(list_columns_group, str):
        list_columns_group = [list_columns_group]

    if aggregation_type == "size":
        df_group = (
            df.groupby(list_columns_group).size().reset_index(name=name_column_result)
        )
    elif aggregation_type in ["sum", "mean"] and column_to_aggregate is not None:
        if aggregation_type == "sum":
            df_group = (
                df.groupby(list_columns_group)
                .sum()[column_to_aggregate]
                .reset_index(name=name_column_result)
            )
        elif aggregation_type == "mean":
            df_group = (
                df.groupby(list_columns_group)
                .mean()[column_to_aggregate]
                .reset_index(name=name_column_result)
            )
    else:
        logger.error(
            "Invalid aggregation type or column_to_aggregate not provided for sum or mean aggregation."
        )

    return df_group


def apply_weight(
    row, column_value=None, column_weight=None, weight_false=1, weight_true=1
):
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

    if normalize_to_high_score:
        # VALORES MENOR -> MAIORES NOTAS
        df[name_column_result] = normalization_functions.normalize_to_high_score(
            df[name_column_value]
        )
    else:
        # VALORES MENOR -> MENORES NOTAS
        df[name_column_result] = normalization_functions.normalize_to_low_score(
            df[name_column_value]
        )

    if list_columns_group_result:
        # AGRUPANDO OS DADOS
        df = group_dataframe(df=df,
                             aggregation_type="mean",
                             list_columns_group=list_columns_group_result,
                             name_column_result=name_column_result,
                             column_to_aggregate=name_column_result)

    return df