import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import typer

from src.models.models_pilar.performance.performance_calculator import ScorePilarPerformance
from src.models.models_pilar.performance.models import ScoreDetails
from src.utils.pandas_functions import load_data_auto, save_data_auto

app = typer.Typer()

@app.command()
def main(
    input_dir: Path = typer.Option(...,
                                   exists=True,
                                   file_okay=False,
                                   help="Caminho para o diretório com os arquivos de score."),
    output_dir: Path = typer.Option(...,
                                    file_okay=False,
                                    help="Caminho para salvar o arquivo de resultados."),
    output_file: str = typer.Option("BASE_SCORE_PILAR_PERFORMANCE.xlsx",
                                    help="Nome do arquivo de saída.")
):

    # Carregando os dataframes
    df_aa = load_data_auto(Path(input_dir,
                                "AA",
                                "BASE_SCORE_AA.xlsx"))
    df_ab = load_data_auto(Path(input_dir,
                                "AB",
                                "BASE_SCORE_AB.xlsx"))
    df_infra_civil = load_data_auto(Path(input_dir,
                                         "INFRA_CIVIL",
                                         "BASE_SCORE_INFRA_CIVIL.xlsx"))

    details_list = [
        ScoreDetails(
            dataframe=df_aa,
            score_column="SCORE_TEMA",
            weight=0.3,
            category="AA",
        ),
        ScoreDetails(
            dataframe=df_ab,
            score_column="SCORE_TEMA",
            weight=0.5,
            category="AB",
        ),
        ScoreDetails(
            dataframe=df_infra_civil,
            score_column="SCORE_TEMA",
            weight=0.2,
            category="INFRA_CIVIL",
        ),
    ]

    # Extraindo uma data comum dos dados, assumindo uniformidade
    dia = df_aa['DIA'].iloc[0]
    mes = df_aa['MES'].iloc[0]
    ano = df_aa['ANO'].iloc[0]

    # Calculando o score pilar
    score_calculator = ScorePilarPerformance(details_list=details_list,
                                             dia=dia,
                                             mes=mes,
                                             ano=ano)
    score_pilar_df = score_calculator.score_pilar

    # Criando o diretório de output
    output_path = output_dir / output_file
    output_dir.mkdir(parents=True, exist_ok=True)

    save_data_auto(dataframe=score_pilar_df, file_path=output_path)

    typer.echo(f"Scores calculados e salvos com sucesso em {output_path}")

if __name__ == "__main__":
    app()
