"""Entidades e regras de negócio do RentSmart."""
from abc import ABC, abstractmethod
from decimal import Decimal

DINHEIRO = Decimal("0.01")


def reais(valor: Decimal) -> str:
    """Representação monetária brasileira."""
    numero = f"{valor.quantize(DINHEIRO):,.2f}"
    return "R$ " + numero.replace(",", "_").replace(".", ",").replace("_", ".")


class Imovel(ABC):
    """Interface abstrata compartilhada pelas categorias de imóveis."""

    @abstractmethod
    def detalhamento(self) -> list[tuple[str, Decimal]]:
        """Itens de custo; descontos negativos."""

    @property
    @abstractmethod
    def descricao(self) -> str:
        """Descrição do imóvel."""

    @property
    def aluguel_mensal(self) -> Decimal:
        return sum((v for _, v in self.detalhamento()), Decimal("0.00")).quantize(DINHEIRO)


class Apartamento(Imovel):
    BASE = Decimal("700.00")
    SEGUNDO_QUARTO = Decimal("200.00")
    GARAGEM = Decimal("300.00")
    DESCONTO_SEM_CRIANCAS = Decimal("0.05")

    def __init__(self, quartos: int, garagem: bool, possui_criancas: bool):
        if type(quartos) is not int or quartos not in (1, 2):
            raise ValueError("O apartamento deve ter um ou dois quartos.")
        if type(garagem) is not bool or type(possui_criancas) is not bool:
            raise ValueError("Garagem e presença de crianças devem ser sim ou não.")
        self.quartos = quartos
        self.garagem = garagem
        self.possui_criancas = possui_criancas

    @property
    def descricao(self) -> str:
        return f"Apartamento com {self.quartos} quarto(s)"

    def detalhamento(self) -> list[tuple[str, Decimal]]:
        itens = [("Aluguel-base do apartamento", self.BASE)]
        if self.quartos == 2:
            itens.append(("Adicional do segundo quarto", self.SEGUNDO_QUARTO))
        if self.garagem:
            itens.append(("Vaga de garagem", self.GARAGEM))
        subtotal = sum((v for _, v in itens), Decimal("0.00"))
        if not self.possui_criancas:
            desconto = (subtotal * self.DESCONTO_SEM_CRIANCAS).quantize(DINHEIRO)
            itens.append(("Desconto de 5% (sem crianças)", -desconto))
        return itens


class Casa(Imovel):
    BASE = Decimal("900.00")
    SEGUNDO_QUARTO = Decimal("250.00")
    GARAGEM = Decimal("300.00")

    def __init__(self, quartos: int, garagem: bool):
        if type(quartos) is not int or quartos not in (1, 2):
            raise ValueError("A casa deve ter um ou dois quartos.")
        if type(garagem) is not bool:
            raise ValueError("Garagem deve ser sim ou não.")
        self.quartos = quartos
        self.garagem = garagem

    @property
    def descricao(self) -> str:
        return f"Casa com {self.quartos} quarto(s)"

    def detalhamento(self) -> list[tuple[str, Decimal]]:
        itens = [("Aluguel-base da casa", self.BASE)]
        if self.quartos == 2:
            itens.append(("Adicional do segundo quarto", self.SEGUNDO_QUARTO))
        if self.garagem:
            itens.append(("Vaga de garagem", self.GARAGEM))
        return itens


class Estudio(Imovel):
    BASE = Decimal("1200.00")
    PACOTE_DUAS_VAGAS = Decimal("250.00")
    VAGA_ADICIONAL = Decimal("60.00")

    def __init__(self, vagas: int):
        if type(vagas) is not int or vagas < 0 or vagas == 1:
            raise ValueError("Estúdios permitem 0 vagas ou pacote inicial de 2 ou mais vagas.")
        self.vagas = vagas

    @property
    def descricao(self) -> str:
        return f"Estúdio com {self.vagas} vaga(s) de estacionamento"

    def detalhamento(self) -> list[tuple[str, Decimal]]:
        itens = [("Aluguel-base do estúdio", self.BASE)]
        if self.vagas >= 2:
            itens.append(("Pacote inicial de duas vagas", self.PACOTE_DUAS_VAGAS))
            if self.vagas > 2:
                itens.append((f"{self.vagas - 2} vaga(s) adicional(is)", (self.vagas - 2) * self.VAGA_ADICIONAL))
        return itens


class Orcamento:
    TAXA_CONTRATUAL = Decimal("2000.00")
    MESES = 12

    def __init__(self, imovel: Imovel, parcelas_taxa: int):
        if not isinstance(imovel, Imovel):
            raise TypeError("O orçamento requer um imóvel válido.")
        if type(parcelas_taxa) is not int or not 1 <= parcelas_taxa <= 5:
            raise ValueError("A taxa contratual pode ser paga em 1 a 5 parcelas.")
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa

    @property
    def aluguel_mensal(self) -> Decimal:
        return self.imovel.aluguel_mensal

    def parcela_da_taxa(self, mes: int) -> Decimal:
        if type(mes) is not int or not 1 <= mes <= self.MESES:
            raise ValueError("Mês da projeção deve estar entre 1 e 12.")
        if mes > self.parcelas_taxa:
            return Decimal("0.00")
        centavos = int(self.TAXA_CONTRATUAL * 100)
        base, resto = divmod(centavos, self.parcelas_taxa)
        return Decimal(base + (1 if mes <= resto else 0)) / Decimal(100)

    def projecao(self) -> list[dict]:
        resultado = []
        for mes in range(1, self.MESES + 1):
            taxa = self.parcela_da_taxa(mes)
            resultado.append({"mes": mes, "aluguel": self.aluguel_mensal,
                              "taxa": taxa, "total": self.aluguel_mensal + taxa})
        return resultado

    @property
    def total_primeiro_ano(self) -> Decimal:
        return sum((item["total"] for item in self.projecao()), Decimal("0.00"))
