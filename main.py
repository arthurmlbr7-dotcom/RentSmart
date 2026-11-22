"""RentSmart - sistema de orçamento de locação (interface de terminal).

Execute: python main.py
"""
from pathlib import Path
from exportacao import ExportadorCSV
from modelos import Apartamento, Casa, Estudio, Orcamento, reais


def ler_opcao(mensagem: str, opcoes: set[str]) -> str:
    while True:
        resposta = input(mensagem).strip()
        if resposta in opcoes:
            return resposta
        print("Opção inválida. Escolha uma das opções apresentadas.\n")


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        resposta = input(mensagem).strip().casefold()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "não", "nao"):
            return False
        print("Resposta inválida. Digite S para sim ou N para não.\n")


def ler_inteiro(mensagem: str, minimo: int, maximo: int | None = None) -> int:
    while True:
        resposta = input(mensagem).strip()
        try:
            numero = int(resposta)
        except ValueError:
            print("Digite um número inteiro válido.\n")
            continue
        if numero < minimo or (maximo is not None and numero > maximo):
            intervalo = f"entre {minimo} e {maximo}" if maximo is not None else f"a partir de {minimo}"
            print(f"Digite um número {intervalo}.\n")
            continue
        return numero


def selecionar_imovel():
    print("\nSelecione o tipo de imóvel:")
    print("  1 - Apartamento")
    print("  2 - Casa")
    print("  3 - Estúdio")
    escolha = ler_opcao("Sua escolha (1, 2 ou 3): ", {"1", "2", "3"})
    if escolha == "1":
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja uma vaga de garagem? (S/N): ")
        criancas = ler_sim_nao("O cliente possui crianças? (S/N): ")
        return Apartamento(quartos, garagem, criancas)
    if escolha == "2":
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja uma vaga de garagem? (S/N): ")
        return Casa(quartos, garagem)
    deseja = ler_sim_nao("Deseja estacionamento no estúdio? (S/N): ")
    vagas = ler_inteiro("Total de vagas (mínimo 2): ", 2) if deseja else 0
    return Estudio(vagas)


def exibir_orcamento(orcamento: Orcamento) -> None:
    print("\n" + "=" * 60)
    print("             RENTSMART | ORÇAMENTO DE LOCAÇÃO")
    print("=" * 60)
    print("Imóvel:", orcamento.imovel.descricao)
    print("-" * 60)
    for item, valor in orcamento.imovel.detalhamento():
        print(f"  {item:<42}{reais(valor):>16}")
    print("-" * 60)
    print(f"  {'ALUGUEL MENSAL':<42}{reais(orcamento.aluguel_mensal):>16}")
    print("\nTaxa contratual (custo distinto do aluguel):", reais(orcamento.TAXA_CONTRATUAL))
    print("Parcelamento escolhido:", orcamento.parcelas_taxa, "vez(es)")
    print("\nPROJEÇÃO DOS PAGAMENTOS")
    print(f"{'Mês':>4} | {'Aluguel':>14} | {'Taxa':>14} | {'Total':>14}")
    print("-" * 60)
    for linha in orcamento.projecao():
        print(f"{linha['mes']:>4} | {reais(linha['aluguel']):>14} | {reais(linha['taxa']):>14} | {reais(linha['total']):>14}")
    print("-" * 60)
    print("TOTAL PREVISTO NO PRIMEIRO ANO:", reais(orcamento.total_primeiro_ano))
    print("Observação: valores nominais, sem reajustes ou outras despesas não previstas.")


def main() -> None:
    print("=" * 60)
    print("   RENTSMART - SISTEMA DE ORÇAMENTO DE LOCAÇÃO")
    print("=" * 60)
    print("Informe os dados para simular um orçamento de 12 meses.")
    imovel = selecionar_imovel()
    parcelas = ler_inteiro("\nEm quantas parcelas deseja pagar a taxa de R$ 2.000,00 (1 a 5)? ", 1, 5)
    orcamento = Orcamento(imovel, parcelas)
    exibir_orcamento(orcamento)
    arquivo = ExportadorCSV.exportar(orcamento, Path.cwd() / "projecao_12_meses.csv")
    print(f"\nCSV de 12 meses criado em: {arquivo.resolve()}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nOperação encerrada pelo usuário.")
    except OSError as erro:
        print(f"\nNão foi possível salvar o CSV: {erro}")
