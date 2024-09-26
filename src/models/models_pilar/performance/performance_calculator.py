import pandas as pd
from .models import BaseScore, ScoreDetails
from .weights import Weights

class ScorePilarPerformance:
    """
    Classe para calcular o score pilar combinado a partir de várias categorias de scores.

    Attributes:
        details_list (list): Lista de objetos ScoreDetails contendo dados e metadata de cada categoria.
        dia (int): Dia associado aos dados.
        mes (int): Mês associado aos dados.
        ano (int): Ano associado aos dados.
        score_pilar (DataFrame): DataFrame contendo o score pilar calculado.
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
        self.score_pilar = self.calculate_score_pilar()

    def calculate_score_pilar(self):
        """
        Calcula o score pilar combinado de todas as categorias.

        Returns:
            DataFrame: DataFrame com as colunas 'CD_PONTO', 'DIA', 'MES', 'ANO', scores, pesos,
            faróis de cada categoria, e o score e farol pilar combinado.
        """
        df_final = pd.DataFrame()

        for detail in self.details_list:
            df = detail.dataframe.copy()
            category = detail.category

            # Nomeando as colunas conforme a categoria para clareza e prevenção de sobreposição
            score_col = f"{category}_SCORE"
            peso_col = f"{category}_PESO"
            farol_col = f"{category}_FAROL"

            df.rename(columns={detail.score_column: score_col}, inplace=True)
            df[peso_col] = detail.weight
            df[farol_col] = df[score_col].apply(self.definir_farol)

            # Primeira categoria inicializa o df_final, as subsequentes são mescladas
            if df_final.empty:
                df_final = df[['CD_PONTO', 'DIA', 'MES', 'ANO', score_col, peso_col, farol_col]]
            else:
                df_final = df_final.merge(df[['CD_PONTO', score_col, peso_col, farol_col]], on='CD_PONTO', how='outer')

        # Calcular o score pilar ponderado e o farol correspondente
        df_final['SCORE_PILAR'] = sum(
            df_final[col] * df_final[col.replace('_SCORE', '_PESO')] for col in df_final.columns if '_SCORE' in col
        ) / df_final[[col for col in df_final.columns if '_PESO' in col]].sum(axis=1)
        df_final['FAROL_PILAR'] = df_final['SCORE_PILAR'].apply(self.definir_farol)

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
            return 'VERMELHO'
        elif score <= 8:
            return 'AMARELO'
        else:
            return 'VERDE'
