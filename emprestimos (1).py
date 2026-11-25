"""Regras de empréstimo de equipamentos do laboratório maker."""


from datetime import timedelta


class EmprestimosMaker:
    def calcular_data_limite(self, data_retirada, dias):
        """Calcula o vencimento em dias corridos."""

        if dias < 1:
            raise ValueError("O prazo deve ser positivo")
        return data_retirada + timedelta(days=dias)

    def calcular_multa(self, dias_atraso):
        """Retorna a multa em centavos."""
        if dias_atraso < 0:
            raise ValueError("O atraso não pode ser negativo")
        return dias_atraso * 500

    def avaliar_renovacao(self, dias_atraso, renovacoes, tem_reserva, saldo_pendente=0):
        """Avalia a renovação e devolve o código de decisão."""
        if dias_atraso < 0 or renovacoes < 0 or saldo_pendente < 0:
            raise ValueError("Atraso, renovações e saldo não podem ser negativos")
        if dias_atraso > 0:
            return "EM_ATRASO"
        if tem_reserva:
            return "RESERVADO"
        if saldo_pendente >= 1500:
            return "SALDO_PENDENTE"
        if renovacoes > 2:
            return "LIMITE_ATINGIDO"
        return "AUTORIZADO"

    def registrar_devolucao(self, data_limite, data_devolucao, dias_abonados=0):
        """Retorna os dias de atraso cobrados e o valor da multa."""
        if dias_abonados < 0:
            raise ValueError("O abono não pode ser negativo")

        atraso = (data_devolucao - data_limite).days
        dias_cobrados = max(0, atraso - dias_abonados)
        return dias_cobrados, self.calcular_multa(dias_cobrados)
