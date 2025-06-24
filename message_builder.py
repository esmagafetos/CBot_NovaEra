from datetime import datetime
import random

class MessageBuilder:
    @staticmethod
    def build_message(client_data):
        """Constrói a mensagem no formato WhatsApp"""
        telefone = client_data.get('TELEFONE', '')
        nome = client_data.get('NOME_ASSINANTE', 'Cliente')
        protocolo = client_data.get('ID_UF', '') + str(random.randint(1000, 9999))
        
        return (
            f"Esperamos que você esteja bem, {nome}!\n\n"
            f"Gostaríamos de lembrar que a fatura da sua linha móvel *{telefone}*, "
            f"contrato *{protocolo}*, está com vencimento em *{datetime.now().strftime('%d/%m/%Y')}*.\n\n"
            "Para sua comodidade, se você efetuar o pagamento nas próximas 24 horas, "
            "poderá aproveitar *30% OFF*!\n\n"
            "Não deixe essa chance passar. Por favor, escolha uma das opções abaixo para continuar:\n\n"
            "Digite: *Sim* para pagar via Pix\n"
            "Digite: *Não* se você já realizou o pagamento\n\n"
            "Valor total em aberto: R$ 39,80\n"
            "Valor com 30% OFF via Pix: *R$ 31.84*\n\n"
            "Atenciosamente,\n"
            "Claro Agradece\n"
            "CLARO MOVEL"
        )
