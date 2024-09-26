from pathlib import Path

import pandas as pd
import numpy as np


# Função para definir o farol baseado no score
def definir_farol(score):
    if score <= 4:
        return "VERMELHO"
    elif score <= 8:
        return "AMARELO"
    else:
        return "VERDE"


# Função para gerar Score com base nas ocorrências
def calcular_score(ocorrencias, max_ocorrencias):
    return max(0, 10 - (ocorrencias / max_ocorrencias) * 10)


def generate_dataframe_score_view():
    # Parâmetros de geração de dados
    n = 9999  # número de pontos
    max_ocorrencias = 100  # máximo de ocorrências para normalização
    max_recorrencias = 50  # máximo de recorrência
    max_mttr = 48  # máximo de MTTR (em horas)

    # Gerando dados aleatórios
    cd_ponto = np.arange(1, n + 1)
    ocorrencias = np.random.randint(0, max_ocorrencias + 1, n)
    recorrencias = np.random.randint(0, max_recorrencias + 1, n)
    mttr = np.random.uniform(0, max_mttr, n)

    # Calculando scores
    score_ocorrencias = [calcular_score(o, max_ocorrencias) for o in ocorrencias]
    score_recorrencias = [calcular_score(r, max_recorrencias) for r in recorrencias]
    score_mttr = [calcular_score(m, max_mttr) for m in mttr]

    # Definindo os faróis com base nos scores
    farol_ocorrencias = [definir_farol(s) for s in score_ocorrencias]
    farol_recorrencias = [definir_farol(s) for s in score_recorrencias]
    farol_mttr = [definir_farol(s) for s in score_mttr]

    # DEFININDO DATA
    dia = 1
    mes = 9
    ano = 2024

    # Definindo pesos
    peso_ocorrencias = 0.2
    peso_recorrencias = 0.7
    peso_mttr = 0.1

    # DEFININDO O SCORE DO TEMA
    score_tema = score_tema = np.average(
        [score_ocorrencias, score_recorrencias, score_mttr],
        axis=0,
        weights=[peso_ocorrencias, peso_recorrencias, peso_mttr],
    )
    farol_tema = [definir_farol(s) for s in score_tema]

    # Criando o DataFrame
    df = pd.DataFrame(
        {
            "CD_PONTO": cd_ponto,
            "DIA": [dia] * len(cd_ponto),
            "MES": [mes] * len(cd_ponto),
            "ANO": [ano] * len(cd_ponto),
            "VOLUME_OCORRENCIAS": ocorrencias,
            "SCORE_OCORRENCIAS": score_ocorrencias,
            "FAROL_OCORRENCIAS": farol_ocorrencias,
            "PESO_OCORRENCIAS": peso_ocorrencias,
            "VOLUME_RECORRENCIA": recorrencias,
            "SCORE_RECORRENCIA": score_recorrencias,
            "FAROL_RECORRENCIA": farol_recorrencias,
            "PESO_RECORRENCIA": peso_recorrencias,
            "MTTR": mttr,
            "SCORE_MTTR": score_mttr,
            "FAROL_MTTR": farol_mttr,
            "PESO_MTTR": peso_mttr,
            "SCORE_TEMA": score_tema,
            "FAROL_TEMA": farol_tema,
        }
    )

    # GERANDO O DATAFRAME RESULTADO
    df.to_excel(
        str(
            Path(
                Path(__file__).parent.parent.parent.parent,
                r"data\result\PERFORMANCE\AB\BASE_SCORE_AB.xlsx",
            )
        ),
        index=None,
    )


if __name__ == "__main__":
    generate_dataframe_score_view()
