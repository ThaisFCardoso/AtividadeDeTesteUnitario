import unittest
from datetime import date

from emprestimos import EmprestimosMaker

# Os IDs CTxx remetem às linhas da matriz de rastreabilidade (matriz_vv_emprestimos.xlsx).
# Os resultados esperados vêm do enunciado (R1 a R4), não do comportamento do código.

VENCIMENTO = date(2026, 5, 7)  # data limite usada nos testes de R4


class TestEmprestimosMaker(unittest.TestCase):
    def setUp(self):
        self.emprestimos = EmprestimosMaker()

    # ------------------------------------------------------------------
    # R1 · Vencimento
    # ------------------------------------------------------------------

    # CT01 · R1
    def test_calcula_vencimento_em_dias_corridos(self):
        retirada = date(2026, 5, 4)

        vencimento = self.emprestimos.calcular_data_limite(retirada, 3)

        self.assertEqual(vencimento, date(2026, 5, 7))

    # CT02 · R1
    def test_vencimento_com_prazo_minimo_de_um_dia(self):
        self.assertEqual(
            self.emprestimos.calcular_data_limite(date(2026, 5, 4), 1),
            date(2026, 5, 5),
        )

    # CT03 · R1
    def test_prazo_zero_gera_value_error(self):
        with self.assertRaises(ValueError):
            self.emprestimos.calcular_data_limite(date(2026, 5, 4), 0)

    # CT04 · R1
    def test_prazo_negativo_gera_value_error(self):
        with self.assertRaises(ValueError):
            self.emprestimos.calcular_data_limite(date(2026, 5, 4), -3)

    # CT05 · R1
    def test_vencimento_atravessa_virada_de_ano(self):
        self.assertEqual(
            self.emprestimos.calcular_data_limite(date(2026, 12, 30), 3),
            date(2027, 1, 2),
        )

    # ------------------------------------------------------------------
    # R2 · Multa
    # ------------------------------------------------------------------

    # CT06 · R2
    def test_multa_de_zero_dias_e_zero(self):
        self.assertEqual(self.emprestimos.calcular_multa(0), 0)

    # CT07 · R2
    def test_multa_de_um_dia_e_500_centavos(self):
        self.assertEqual(self.emprestimos.calcular_multa(1), 500)

    # CT08 · R2
    def test_multa_de_cinco_dias_abaixo_do_teto(self):
        self.assertEqual(self.emprestimos.calcular_multa(5), 2500)

    # CT09 · R2
    def test_multa_de_seis_dias_atinge_o_teto_de_3000(self):
        self.assertEqual(self.emprestimos.calcular_multa(6), 3000)

    # CT10 · R2
    def test_multa_de_sete_dias_fica_limitada_ao_teto(self):
        self.assertEqual(self.emprestimos.calcular_multa(7), 3000)

    # CT11 · R2
    def test_multa_de_trinta_dias_fica_limitada_ao_teto(self):
        self.assertEqual(self.emprestimos.calcular_multa(30), 3000)

    # CT12 · R2
    def test_multa_com_atraso_negativo_gera_value_error(self):
        with self.assertRaises(ValueError):
            self.emprestimos.calcular_multa(-1)

    # ------------------------------------------------------------------
    # R3 · Renovação (um motivo de recusa por teste, exceto CT25 a CT27)
    # ------------------------------------------------------------------

    # CT13 · R3
    def test_renovacao_autorizada_quando_nenhuma_condicao_e_satisfeita(self):
        self.assertEqual(self.emprestimos.avaliar_renovacao(0, 0, False), "AUTORIZADO")

    # CT14 · R3
    def test_renovacao_com_atraso_negativo_gera_value_error(self):
        with self.assertRaises(ValueError):
            self.emprestimos.avaliar_renovacao(-1, 0, False)

    # CT15 · R3
    def test_renovacao_com_renovacoes_negativas_gera_value_error(self):
        with self.assertRaises(ValueError):
            self.emprestimos.avaliar_renovacao(0, -1, False)

    # CT16 · R3
    def test_renovacao_com_saldo_negativo_gera_value_error(self):
        with self.assertRaises(ValueError):
            self.emprestimos.avaliar_renovacao(0, 0, False, -1)

    # CT17 · R3
    def test_renovacao_recusada_com_um_dia_de_atraso(self):
        self.assertEqual(self.emprestimos.avaliar_renovacao(1, 0, False), "EM_ATRASO")

    # CT18 · R3
    def test_renovacao_recusada_com_reserva_de_outro_usuario(self):
        self.assertEqual(self.emprestimos.avaliar_renovacao(0, 0, True), "RESERVADO")

    # CT19 · R3
    def test_saldo_de_1499_centavos_nao_bloqueia_renovacao(self):
        self.assertEqual(
            self.emprestimos.avaliar_renovacao(0, 0, False, 1499), "AUTORIZADO"
        )

    # CT20 · R3
    def test_saldo_de_1500_centavos_nao_bloqueia_pois_o_limite_e_superior_a_1500(self):
        self.assertEqual(
            self.emprestimos.avaliar_renovacao(0, 0, False, 1500), "AUTORIZADO"
        )

    # CT21 · R3
    def test_saldo_de_1501_centavos_bloqueia_renovacao(self):
        self.assertEqual(
            self.emprestimos.avaliar_renovacao(0, 0, False, 1501), "SALDO_PENDENTE"
        )

    # CT22 · R3
    def test_uma_renovacao_anterior_ainda_permite_renovar(self):
        self.assertEqual(self.emprestimos.avaliar_renovacao(0, 1, False), "AUTORIZADO")

    # CT23 · R3
    def test_duas_renovacoes_anteriores_atingem_o_limite(self):
        self.assertEqual(
            self.emprestimos.avaliar_renovacao(0, 2, False), "LIMITE_ATINGIDO"
        )

    # CT24 · R3
    def test_tres_renovacoes_anteriores_atingem_o_limite(self):
        self.assertEqual(
            self.emprestimos.avaliar_renovacao(0, 3, False), "LIMITE_ATINGIDO"
        )

    # CT25 · R3 (prioridade 1 sobre 2, 3 e 4)
    def test_atraso_tem_prioridade_sobre_todos_os_outros_motivos(self):
        self.assertEqual(
            self.emprestimos.avaliar_renovacao(2, 3, True, 2000), "EM_ATRASO"
        )

    # CT26 · R3 (prioridade 2 sobre 3 e 4)
    def test_reserva_tem_prioridade_sobre_saldo_e_limite_de_renovacoes(self):
        self.assertEqual(
            self.emprestimos.avaliar_renovacao(0, 3, True, 2000), "RESERVADO"
        )

    # CT27 · R3 (prioridade 3 sobre 4)
    def test_saldo_pendente_tem_prioridade_sobre_limite_de_renovacoes(self):
        self.assertEqual(
            self.emprestimos.avaliar_renovacao(0, 3, False, 2000), "SALDO_PENDENTE"
        )

    # ------------------------------------------------------------------
    # R4 · Devolução com abono (confere os dois elementos da tupla; R2 na multa)
    # ------------------------------------------------------------------

    # CT28 · R4
    def test_devolucao_no_dia_do_vencimento_nao_cobra_dias_nem_multa(self):
        self.assertEqual(
            self.emprestimos.registrar_devolucao(VENCIMENTO, date(2026, 5, 7)),
            (0, 0),
        )

    # CT29 · R4
    def test_devolucao_antecipada_nao_cobra_dias_nem_multa(self):
        self.assertEqual(
            self.emprestimos.registrar_devolucao(VENCIMENTO, date(2026, 5, 5)),
            (0, 0),
        )

    # CT30 · R4 · R2
    def test_devolucao_com_um_dia_de_atraso_cobra_500_centavos(self):
        self.assertEqual(
            self.emprestimos.registrar_devolucao(VENCIMENTO, date(2026, 5, 8)),
            (1, 500),
        )

    # CT31 · R4 · R2
    def test_devolucao_com_cinco_dias_de_atraso_abaixo_do_teto(self):
        self.assertEqual(
            self.emprestimos.registrar_devolucao(VENCIMENTO, date(2026, 5, 12)),
            (5, 2500),
        )

    # CT32 · R4 · R2
    def test_devolucao_com_seis_dias_de_atraso_atinge_o_teto(self):
        self.assertEqual(
            self.emprestimos.registrar_devolucao(VENCIMENTO, date(2026, 5, 13)),
            (6, 3000),
        )

    # CT33 · R4 · R2
    def test_devolucao_com_dez_dias_de_atraso_informa_dias_integrais_e_multa_no_teto(self):
        self.assertEqual(
            self.emprestimos.registrar_devolucao(VENCIMENTO, date(2026, 5, 17)),
            (10, 3000),
        )

    # CT34 · R4 · R2
    def test_abono_parcial_desconta_dias_cobrados(self):
        self.assertEqual(
            self.emprestimos.registrar_devolucao(VENCIMENTO, date(2026, 5, 12), 2),
            (3, 1500),
        )

    # CT35 · R4
    def test_abono_igual_ao_atraso_zera_dias_cobrados_e_multa(self):
        self.assertEqual(
            self.emprestimos.registrar_devolucao(VENCIMENTO, date(2026, 5, 10), 3),
            (0, 0),
        )

    # CT36 · R4
    def test_abono_maior_que_o_atraso_limita_dias_cobrados_a_zero(self):
        self.assertEqual(
            self.emprestimos.registrar_devolucao(VENCIMENTO, date(2026, 5, 8), 5),
            (0, 0),
        )

    # CT37 · R4
    def test_abono_negativo_gera_value_error(self):
        with self.assertRaises(ValueError):
            self.emprestimos.registrar_devolucao(VENCIMENTO, date(2026, 5, 8), -1)

    # CT38 · R4 · R2
    def test_abono_com_atraso_ainda_acima_do_teto_mantem_multa_em_3000(self):
        self.assertEqual(
            self.emprestimos.registrar_devolucao(VENCIMENTO, date(2026, 5, 17), 2),
            (8, 3000),
        )

    # CT39 · R4 · R2
    def test_abono_que_deixa_exatamente_seis_dias_cobrados_atinge_o_teto(self):
        self.assertEqual(
            self.emprestimos.registrar_devolucao(VENCIMENTO, date(2026, 5, 15), 2),
            (6, 3000),
        )


if __name__ == "__main__":
    unittest.main()
