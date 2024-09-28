# Projeto de Cálculo de Score de Pilares e Global

Este projeto implementa uma solução para calcular scores de pilares específicos e um score global combinado, baseando-se em pesos configuráveis para cada pilar. O sistema é projetado para ser executado via linha de comando, oferecendo flexibilidade na seleção dos pilares e na especificação dos pesos.

## Estrutura do Projeto

O projeto inclui os seguintes diretórios e arquivos principais:

- `src/`: Contém o código-fonte do projeto.
  - `models/`: Contém os modelos de dados usados para o cálculo dos scores.
    - `models_global/`: Modelos para cálculo do score global.
    - `models_pilar/`: Modelos para cálculo dos scores de pilares.
  - `utils/`: Funções úteis, como carregamento e salvamento de dados.
- `data/`: Diretório para armazenar os datasets de entrada e saída.
- `scripts/`: Scripts de linha de comando para executar os cálculos.

## Configuração

Para configurar o ambiente necessário para executar este projeto, siga os passos abaixo:

1. Clone o repositório:
git clone https://github.com/emersonrafaels/score_agencias.git
   
2. Navegue até o diretório do projeto:
- cd score_agencias

3. Instale as dependências usando pip (é recomendado usar um ambiente virtual):


## Uso

Para calcular os scores, você pode utilizar os scripts de linha de comando disponibilizados. Aqui estão os comandos básicos para executar os cálculos de score dos pilares e do score global:

**Cálculo de Score dos Pilares**:


Opções adicionais:
- `--include_aa`: Incluir scores de AA (default `True`).
- `--include_ab`: Incluir scores de AB (default `True`).
- `--include_infra`: Incluir scores de Infra Civil (default `True`).
- `--weight_aa`: Peso para scores de AA (default `0.3`).
- `--weight_ab`: Peso para scores de AB (default `0.3`).
- `--weight_infra`: Peso para scores de Infra Civil (default `0.3`).

**Cálculo de Score Global**:

Opções adicionais:
- `--include_esg`: Incluir scores do pilar ESG (default `True`).
- `--include_performance`: Incluir scores do pilar Performance (default `True`).
- `--weight_esg`: Peso para scores do pilar ESG (default `0.7`).
- `--weight_performance`: Peso para scores do pilar Performance (default `0.3`).

## Contribuições

Contribuições são sempre bem-vindas! Para contribuir com o projeto, por favor, crie um fork do repositório, faça suas alterações e submeta um pull request.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.



