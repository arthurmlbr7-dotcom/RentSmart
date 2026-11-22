# RentSmart — Sistema de Orçamento de Locação

**Projeto acadêmico:** Arthur — UniFECAF — Ciência da Computação.

Aplicação em Python com Programação Orientada a Objetos para a imobiliária fictícia R.M Imóveis. Calcula o aluguel mensal de apartamentos, casas e estúdios, aplica adicionais e descontos, apresenta a taxa contratual separadamente e gera a projeção financeira dos 12 meses em CSV.

## Como executar

Requer **Python 3.10 ou superior**. Não precisa de bibliotecas externas.

Abra um terminal na pasta do projeto e execute:

    python main.py

Se necessário, substitua por `python3 main.py` ou `py main.py`.

O programa solicita o tipo de imóvel, suas características e o parcelamento da taxa contratual; ao final, exibe o detalhamento e cria `projecao_12_meses.csv` na pasta atual.

## Regras comerciais

| Característica | Valor |
| --- | ---: |
| Apartamento de 1 quarto | R$ 700,00/mês |
| Segundo quarto do apartamento | + R$ 200,00/mês |
| Casa de 1 quarto | R$ 900,00/mês |
| Segundo quarto da casa | + R$ 250,00/mês |
| Estúdio | R$ 1.200,00/mês |
| Garagem para casa ou apartamento | + R$ 300,00/mês |
| Pacote inicial de 2 vagas para estúdio | + R$ 250,00/mês |
| Cada vaga de estúdio além de 2 | + R$ 60,00/mês |
| Apartamento sem crianças | 5% de desconto depois dos adicionais |
| Taxa contratual | R$ 2.000,00, em até 5 parcelas |

Premissas: estúdios podem ter zero vagas ou o pacote inicial de duas ou mais vagas, porque o enunciado não fornece preço para uma vaga isolada. O parcelamento da taxa é cobrado nos primeiros N meses e não altera o aluguel mensal. Diferenças de centavos são distribuídas nas primeiras parcelas. A projeção não inclui reajustes e despesas não informadas.

## Estrutura do projeto

- `main.py`: interação com o usuário e validação das entradas.
- `modelos.py`: classes abstrata `Imovel`, `Apartamento`, `Casa`, `Estudio` e `Orcamento`.
- `exportacao.py`: classe `ExportadorCSV`.
- `testes/test_rentsmart.py`: 13 testes automatizados.
- `exemplos/projecao_12_meses_exemplo.csv`: simulação demonstrativa.
- `docs/relatorio_teorico.md`: documentação do sistema.

## Exemplo para demonstração

Entradas, nesta ordem: **1** (apartamento), **2** (quartos), **S** (garagem), **N** (crianças), **5** (parcelas).

Aluguel-base de R$ 700,00 + segundo quarto de R$ 200,00 + garagem de R$ 300,00 = subtotal de R$ 1.200,00. Desconto de 5% = R$ 60,00. **Aluguel mensal: R$ 1.140,00**.

Taxa contratual de R$ 2.000,00 em 5 parcelas de R$ 400,00. Pagamento mensal de R$ 1.540,00 nos meses 1 a 5 e R$ 1.140,00 nos meses 6 a 12. **Total do primeiro ano: R$ 15.680,00**.

## Testes

Execute na pasta principal:

    python -m unittest discover -s testes -v

O projeto implementa herança, abstração, polimorfismo e composição. O aluguel é calculado usando `Decimal` para preservar os centavos, e o CSV é gravado usando ponto e vírgula como separador.

## Entregáveis acadêmicos

- **Parte teórica (25%)**: relatório com análise, fluxograma e justificativa das classes. O PDF final também deve ser enviado ao professor.
- **Parte prática (50%)**: este repositório, código Python, README e CSV.
- **Vídeo pitch (25%)**: apresentação de até quatro minutos, a ser publicada separadamente.

**Fonte:** enunciado `TRABALHO - AT & IOOP.docx`. Documentação Python: https://docs.python.org/pt-br/3/
