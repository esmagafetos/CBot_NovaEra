#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CBOT NOVAERA - Sistema de Cobrança Automatizado
Criado por Sanctos
"""

import os
import time
import random
import logging
from datetime import datetime
from database_handler import DatabaseHandler
from whatsapp_client import WhatsAppClient
from message_builder import MessageBuilder
from config import CONFIG

class CBotNovaEra:
    def __init__(self):
        self.show_banner()
        self.setup_logging()
        self.db_handler = DatabaseHandler()
        self.whatsapp_client = WhatsAppClient()
        self.message_builder = MessageBuilder()
        
    def show_banner(self):
        """Exibe o banner inicial do CBot NovaEra"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\033[1;36m")
        print("  ____ ____   ___  _  ______   _   _   _ ______ _____ ")
        print(" / ___/ ___| / _ \| |/ / ___| | | | | / |___  |___ / ")
        print("| |   \___ \| | | | ' /\___ \ | | | | | |  / /  |_ \ ")
        print("| |___ ___) | |_| | . \ ___) || |_| |_| | / /  ___) |")
        print(" \____|____/ \___/|_|\_\____/  \___/\___/_/_/  |____/ ")
        print("\033[1;33m\n            SISTEMA DE COBRANÇA AUTOMATIZADO")
        print("\033[1;35m                Versão 2.0 - Nova Era")
        print("\033[1;32m             Criado por Sanctos\033[0m")
        print("\033[1;34m" + "="*60 + "\033[0m")
    
    def setup_logging(self):
        """Configura o sistema de logs"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(CONFIG['LOG_FILE']),
                logging.StreamHandler()
            ]
        )
        logging.info("Sistema CBot NovaEra iniciado")
    
    def run(self):
        """Executa o fluxo principal do bot"""
        try:
            # Conectar ao WhatsApp
            self.whatsapp_client.connect()
            
            # Obter clientes para contato
            clients = self.db_handler.get_clients_to_message()
            total_clients = len(clients)
            logging.info(f"{total_clients} clientes encontrados para contato")
            
            messages_sent = 0
            
            for idx, client in enumerate(clients, 1):
                if messages_sent >= CONFIG['MAX_MESSAGES_PER_SESSION']:
                    logging.info(f"Limite de {CONFIG['MAX_MESSAGES_PER_SESSION']} mensagens atingido. Encerrando sessão.")
                    break
                
                # Mostrar progresso
                progress = f"[{idx}/{total_clients}]"
                logging.info(f"{progress} Processando cliente: {client['TELEFONE']}")
                
                # Construir mensagem
                message = self.message_builder.build_message(client)
                
                # Enviar mensagem
                if self.whatsapp_client.send_message(client['TELEFONE'], message):
                    messages_sent += 1
                    self.db_handler.mark_as_sent(client['TELEFONE'])
                    
                    # Aplicar delay anti-bloqueio
                    delay = random.randint(CONFIG['MIN_DELAY'], CONFIG['MAX_DELAY'])
                    logging.info(f"Aguardando {delay} segundos para próximo envio...")
                    time.sleep(delay)
                    
                    # Pausa estratégica a cada 5 envios
                    if messages_sent % 5 == 0:
                        logging.info(f"Pausa estratégica de {CONFIG['LONG_PAUSE']} segundos")
                        time.sleep(CONFIG['LONG_PAUSE'])
            
            logging.info(f"Processo concluído. {messages_sent} mensagens enviadas com sucesso.")
            self.show_footer()
            
        except Exception as e:
            logging.error(f"Erro crítico: {str(e)}")
    
    def show_footer(self):
        """Exibe o rodapé do sistema"""
        print("\033[1;34m" + "="*60 + "\033[0m")
        print("\033[1;32mCBot NovaEra - Sistema de Cobrança Automatizado")
        print("\033[1;35mCriado por Sanctos - Versão 2.0\033[0m")
        print("\033[1;33mProcesso concluído com sucesso!\033[0m")

if __name__ == "__main__":
    try:
        bot = CBotNovaEra()
        bot.run()
    except KeyboardInterrupt:
        print("\n\033[1;31mOperação interrompida pelo usuário.\033[0m")
    except Exception as e:
        print(f"\n\033[1;31mErro crítico: {str(e)}\033[0m")
