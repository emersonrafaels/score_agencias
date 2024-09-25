import pandas as pd

class ScorePilarPerformance:
    def __init__(self, peso_aa, peso_ab, peso_infra_civil, file_paths):
        self.peso_aa = peso_aa
        self.peso_ab = peso_ab
        self.peso_infra_civil = peso_infra_civil
        self.file_paths = file_paths
        self.dataframes = self.load_data()
        self.score_pilar = self.calculate_score_pilar()

    def load_data(self):
        # Carregando os DataFrames a partir dos caminhos de arquivo fornecidos
        data = {}
        for key, path in self.file_paths.items():
            data[key] = pd.read_excel(path, engine='openpyxl')
        return data

    def definir_farol(self, score):
        # Define o farol com base no score
        if score <= 4:
            return 'VERMELHO'
        elif score <= 8:
            return 'AMARELO'
        else:
            return 'VERDE'

    def calculate_score_pilar(self):
        # Calcula o Score Pilar ponderado para cada agência
        df_combined = pd.DataFrame()
        scores = []

        for category, df in self.dataframes.items():
            # Normaliza o peso para cada categoria de dados
            if category == 'AA':
                weight = self.peso_aa
            elif category == 'AB':
                weight = self.peso_ab
            elif category == 'Infra_Civil':
                weight = self.peso_infra_civil
            df['Weighted_Score'] = df['SCORE_TEMA'] * weight
            scores.append(df[['CD_PONTO', 'Weighted_Score']])

        # Combina os scores
        df_combined = pd.concat(scores)
        score_pilar = df_combined.groupby('CD_PONTO')['Weighted_Score'].sum().reset_index()
        score_pilar['Farol_Pilar'] = score_pilar['Weighted_Score'].apply(self.definir_farol)

        return score_pilar
