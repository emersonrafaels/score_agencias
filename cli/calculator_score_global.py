import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import typer

from src.models.models_global.score_global.global_calculator import (
    ScoreGlobalCalculator,
)
from src.models.models_global.score_global.models import ScoreDetails
from src.utils.pandas_functions import load_data_auto, save_data_auto

app = typer.Typer()

@app.command()
def main(
    input_dir: Path = typer.Option(
        ...,
        exists=True,
        file_okay=False,
        help="Caminho para o diretório com os arquivos de score dos pilares.",
    ),
    output_dir: Path = typer.Option(
        ..., file_okay=False, help="Caminho para salvar o arquivo de resultados do score global."
    ),
    output_file: str = typer.Option(
        "BASE_SCORE_GLOBAL.xlsx", help="Nome do arquivo de saída para o score global."
    ),
    include_esg: bool = typer.Option(True, help="Incluir scores do pilar ESG"),
    include_performance: bool = typer.Option(True, help="Incluir scores do pilar Performance"),
    weight_esg: float = typer.Option(0.2, help="Peso para scores do pilar ESG"),
    weight_performance: float = typer.Option(0.8, help="Peso para scores do pilar Performance"),
):
    details_list = []

    if include_esg:
        df_esg = load_data_auto(Path(input_dir, "ESG", "BASE_SCORE_TEMA_ESG.xlsx"))
        details_list.append(
            ScoreDetails(
                dataframe=df_esg,
                score_column="SCORE_PILAR",
                farol_column="FAROL_PILAR",
                weight=weight_esg,
                category="ESG",
            )
        )

    if include_performance:
        df_performance = load_data_auto(Path(input_dir, "PERFORMANCE", "BASE_SCORE_TEMA_PERFORMANCE.xlsx"))
        details_list.append(
            ScoreDetails(
                dataframe=df_performance,
                score_column="SCORE_PILAR",
                farol_column="FAROL_PILAR",
                weight=weight_performance,
                category="PERFORMANCE",
            )
        )

    if not details_list:
        typer.echo("Nenhuma categoria de score foi selecionada. Encerrando execução.")
        raise typer.Exit()

    # Assumindo uniformidade nas datas entre os pilares
    dia = details_list[0].dataframe["DIA"].iloc[0]
    mes = details_list[0].dataframe["MES"].iloc[0]
    ano = details_list[0].dataframe["ANO"].iloc[0]

    # Calculando o score pilar
    score_calculator = ScoreGlobalCalculator(
        details_list=details_list, dia=dia, mes=mes, ano=ano
    )
    df_score_global = score_calculator.score_global

    output_path = output_dir / output_file
    output_dir.mkdir(parents=True, exist_ok=True)

    save_data_auto(dataframe=df_score_global, file_path=output_path)

    typer.echo(f"Score global calculado e salvo com sucesso em {output_path}")

if __name__ == "__main__":
    app()
