import pandas as pd
from .weights import Weights

class ScoreGlobalCalculator:
    """
    Classe para calcular o score global combinado a partir de várias categorias de scores de pilares.

    Attributes:
        details_list (list): Lista de objetos ScoreDetails contendo dados e metadata de cada categoria.
        dia (int): Dia associado aos dados.
        mes (int): Mês associado aos dados.
        ano (int): Ano associado aos dados.
        score_global (DataFrame): DataFrame contendo o score global calculado.
    """

    def __init__(self, details_list, dia, mes, ano):
        """
        Inicializa a classe com detalhes das categorias e a data dos dados.

        Args:
            details_list (list): Lista de objetos ScoreDetails.
            dia (int): Dia da data referente aos dados.
            mes (int): Mês da data referente aos dados.
            ano (int): Ano da data referente aos dados.
        """
        Weights(weights=[details.weight for details in details_list])  # Valida os pesos
        self.details_list = details_list
        self.dia = dia
        self.mes = mes
        self.ano = ano
        self.score_pilar = self.calculate_score_global()

    def calculate_score_global(self):
        """
        Calcula o score global combinado de todas os pilares.

        Returns:
            DataFrame: DataFrame com as colunas 'CD_PONTO', 'DIA', 'MES', 'ANO', scores, pesos,
            faróis de cada categoria, e o score e farol global.
        """
        df_final = pd.DataFrame()

        for detail in self.details_list:
            df = detail.dataframe.copy()
            category = detail.category

            # Nomeando as colunas conforme a categoria para clareza e prevenção de sobreposição
            score_col = f"{category}_SCORE"
            peso_col = f"{category}_PESO"
            farol_col = f"{category}_FAROL"

            # Renomeando a coluna de score e farol
            df.rename(columns={detail.score_column: score_col,
                               detail.farol_column: farol_col}, inplace=True)

            # Obtendo o peso do pilar
            df[peso_col] = detail.weight

            # Primeira categoria inicializa o df_final, as subsequentes são mescladas
            if df_final.empty:
                df_final = df[
                    ["CD_PONTO", "DIA", "MES", "ANO", score_col, peso_col, farol_col]
                ]
            else:
                df_final = df_final.merge(
                    df[["CD_PONTO", score_col, peso_col, farol_col]],
                    on="CD_PONTO",
                    how="outer",
                )

        # Calcular o score global ponderado e o farol correspondente
        """
        1)
        Iteração: A expressão itera sobre todas as colunas do DataFrame 
        df_final que contêm a substring "_SCORE" no nome. 
        Cada col nesse loop é o nome de uma coluna de score de um pilar específico.
        
        2)
        Ponderação: Para cada coluna de score identificada, 
        a expressão col.replace("_SCORE", "_PESO") gera o nome 
        correspondente da coluna de peso. 
        Por exemplo, se col é "ESG_SCORE", a expressão gerará "ESG_PESO".
        
        3)
        Multiplicação: Cada score individual em df_final[col] é 
        multiplicado pelo seu peso correspondente em 
        df_final[col.replace("_SCORE", "_PESO")]. 
        Isso pondera cada score pelo seu respectivo peso.
        
        4)
        Soma: A função sum() agrega todos esses scores ponderados 
        para cada linha, resultando na soma dos 
        scores ponderados para cada agência.
        """

        df_final["SCORE_GLOBAL"] = sum(
            df_final[col] * df_final[col.replace("_SCORE", "_PESO")]
            for col in df_final.columns
            if "_SCORE" in col
        ) / df_final[[col for col in df_final.columns if "_PESO" in col]].sum(axis=1)

        df_final["FAROL_GLOBAL"] = df_final["SCORE_GLOBAL"].apply(self.definir_farol)

        return df_final

    @staticmethod
    def definir_farol(score):
        """
        Define o farol com base no score calculado.

        Args:
            score (float): Score calculado para uma categoria ou para o pilar.

        Returns:
            str: Retorna 'VERMELHO', 'AMARELO' ou 'VERDE' com base no valor do score.
        """
        if score <= 4:
            return "VERMELHO"
        elif score <= 8:
            return "AMARELO"
        else:
            return "VERDE"
