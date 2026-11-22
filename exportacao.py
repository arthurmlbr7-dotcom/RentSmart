"""Exportação da projeção de pagamentos para CSV."""
import csv
from pathlib import Path
from modelos import Orcamento


class ExportadorCSV:
    CABECALHO = [
        "Mês", "Aluguel mensal (R$)", "Parcela da taxa (R$)", "Total do mês (R$)"
    ]

    @staticmethod
    def valor_csv(valor) -> str:
        """Formata números para planilhas em português: decimal com vírgula."""
        return f"{valor:.2f}".replace(".", ",")

    @classmethod
    def exportar(cls, orcamento: Orcamento, caminho: str | Path) -> Path:
        destino = Path(caminho)
        destino.parent.mkdir(parents=True, exist_ok=True)
        with destino.open("w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(cls.CABECALHO)
            for linha in orcamento.projecao():
                escritor.writerow([
                    linha["mes"], cls.valor_csv(linha["aluguel"]),
                    cls.valor_csv(linha["taxa"]), cls.valor_csv(linha["total"]),
                ])
        return destino
