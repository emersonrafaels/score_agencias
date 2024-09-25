from pathlib import Path

import pandas as pd
import numpy as np

# Função para definir o farol baseado no score
def definir_farol(score):
    if score <= 4:
        return 'VERMELHO'
    elif score <= 8:
        return 'AMARELO'
    else:
        return 'VERDE'

# Função para gerar Score com base nos consumos e limites estabelecidos
def calcular_score(consumo, max_consumo):
    return max(0, 10 - (consumo / max_consumo) * 10)

def generate_dataframe_esg_score_view():
    # Parâmetros de geração de dados
    n = 9999  # número de pontos
    max_agua = 5000  # máximo de consumo de água para normalização (em m³)
    max_energia = 10000  # máximo de consumo de energia para normalização (em kWh)
    max_fluidos = 100  # máximo de emissão de fluidos refrigerantes (em kg)

    # Gerando dados aleatórios
    cd_ponto = np.arange(1, n + 1)
    consumo_agua = np.random.uniform(0, max_agua, n)
    consumo_energia = np.random.uniform(0, max_energia, n)
    emissao_fluidos = np.random.uniform(0, max_fluidos, n)

    # Calculando scores
    score_agua = [calcular_score(a, max_agua) for a in consumo_agua]
    score_energia = [calcular_score(e, max_energia) for e in consumo_energia]
    score_fluidos = [calcular_score(f, max_fluidos) for f in emissao_fluidos]

    # Definindo os faróis com base nos scores
    farol_agua = [definir_farol(s) for s in score_agua]
    farol_energia = [definir_farol(s) for s in score_energia]
    farol_fluidos = [definir_farol(s) for s in score_fluidos]

    # DEFININDO DATA
    dia = 1
    mes = 9
    ano = 2024

    # Definindo pesos (ajustáveis conforme a relevância de cada indicador)
    peso_agua = 0.2
    peso_energia = 0.2
    peso_fluidos = 0.6

    # DEFININDO O SCORE DO TEMA
    score_tema = np.average([score_agua, score_energia, score_fluidos],
                            axis=0,
                            weights=[peso_agua, peso_energia, peso_fluidos])
    farol_tema = [definir_farol(s) for s in score_tema]

    # Criando o DataFrame
    df = pd.DataFrame({
        'CD_PONTO': cd_ponto,
        'DIA': [dia]*len(cd_ponto),
        'MES': [mes]*len(cd_ponto),
        'ANO': [ano]*len(cd_ponto),
        'CONSUMO_AGUA': consumo_agua,
        'SCORE_AGUA': score_agua,
        'FAROL_AGUA': farol_agua,
        'PESO_AGUA': peso_agua,
        'CONSUMO_ENERGIA': consumo_energia,
        'SCORE_ENERGIA': score_energia,
        'FAROL_ENERGIA': farol_energia,
        'PESO_ENERGIA': peso_energia,
        'EMISSAO_FLUIDOS': emissao_fluidos,
        'SCORE_FLUIDOS': score_fluidos,
        'FAROL_FLUIDOS': farol_fluidos,
        'PESO_FLUIDOS': peso_fluidos,
        'SCORE_TEMA': score_tema,
        'FAROL_TEMA': farol_tema
    })

    # GERANDO O DATAFRAME RESULTADO
    df.to_excel(str(Path(Path(__file__).parent.parent.parent.parent,
                r"data\result\ESG\ESG\BASE_SCORE_ESG.xlsx")),
                index=None)

if __name__ == '__main__':
    generate_dataframe_esg_score_view()
