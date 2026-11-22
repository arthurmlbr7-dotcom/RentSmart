"""Testes automatizados: python -m unittest discover -s testes -v"""
import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from modelos import Apartamento, Casa, Estudio, Orcamento
from exportacao import ExportadorCSV


class TesteRegrasNegocio(unittest.TestCase):
    def test_apartamento_com_desconto_depois_dos_adicionais(self):
        imovel = Apartamento(quartos=2, garagem=True, possui_criancas=False)
        self.assertEqual(imovel.aluguel_mensal, Decimal("1140.00"))
        self.assertEqual(imovel.detalhamento()[-1][1], Decimal("-60.00"))

    def test_apartamento_com_criancas_sem_desconto(self):
        self.assertEqual(Apartamento(2, True, True).aluguel_mensal, Decimal("1200.00"))

    def test_apartamento_sem_adicionais_com_desconto(self):
        self.assertEqual(Apartamento(1, False, False).aluguel_mensal, Decimal("665.00"))

    def test_casa_com_segundo_quarto_e_garagem(self):
        self.assertEqual(Casa(2, True).aluguel_mensal, Decimal("1450.00"))

    def test_casa_basica(self):
        self.assertEqual(Casa(1, False).aluguel_mensal, Decimal("900.00"))

    def test_estudio_sem_estacionamento(self):
        self.assertEqual(Estudio(0).aluguel_mensal, Decimal("1200.00"))

    def test_estudio_duas_vagas(self):
        self.assertEqual(Estudio(2).aluguel_mensal, Decimal("1450.00"))

    def test_estudio_quatro_vagas(self):
        self.assertEqual(Estudio(4).aluguel_mensal, Decimal("1570.00"))

    def test_validacao_de_imoveis(self):
        for construtor, args in [
            (Apartamento, (3, True, False)), (Apartamento, (1, 1, False)),
            (Casa, (0, False)), (Estudio, (1,)), (Estudio, (-1,)),
        ]:
            with self.subTest(construtor=construtor.__name__, args=args):
                with self.assertRaises(ValueError):
                    construtor(*args)

    def test_validacao_de_parcelas(self):
        for parcelas in (0, 6, -1, 2.5, True):
            with self.subTest(parcelas=parcelas):
                with self.assertRaises(ValueError):
                    Orcamento(Casa(1, False), parcelas)

    def test_cinco_parcelas_e_total_anual(self):
        o = Orcamento(Apartamento(2, True, False), 5)
        self.assertEqual(o.aluguel_mensal, Decimal("1140.00"))
        self.assertEqual(o.parcela_da_taxa(1), Decimal("400.00"))
        self.assertEqual(o.parcela_da_taxa(5), Decimal("400.00"))
        self.assertEqual(o.parcela_da_taxa(6), Decimal("0.00"))
        self.assertEqual(o.total_primeiro_ano, Decimal("15680.00"))
        self.assertEqual(len(o.projecao()), 12)

    def test_tres_parcelas_redistribuem_centavos(self):
        o = Orcamento(Casa(1, False), 3)
        self.assertEqual([o.parcela_da_taxa(m) for m in range(1, 4)], [
            Decimal("666.67"), Decimal("666.67"), Decimal("666.66")
        ])
        self.assertEqual(sum((o.parcela_da_taxa(m) for m in range(1, 13))), Decimal("2000.00"))

    def test_csv_tem_doze_meses_e_valores_corretos(self):
        o = Orcamento(Apartamento(2, True, False), 5)
        with tempfile.TemporaryDirectory() as pasta:
            caminho = ExportadorCSV.exportar(o, Path(pasta) / "saida.csv")
            with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
                linhas = list(csv.DictReader(arquivo, delimiter=";"))
            self.assertEqual(len(linhas), 12)
            self.assertEqual(linhas[0]["Aluguel mensal (R$)"], "1140,00")
            self.assertEqual(linhas[0]["Parcela da taxa (R$)"], "400,00")
            self.assertEqual(linhas[0]["Total do mês (R$)"], "1540,00")
            self.assertEqual(linhas[5]["Total do mês (R$)"], "1140,00")


if __name__ == "__main__":
    unittest.main()
