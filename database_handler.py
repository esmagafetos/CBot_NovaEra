import os
import sqlite3
import pandas as pd
import logging
from config import CONFIG

class DatabaseHandler:
    def __init__(self):
        self.setup_database()
    
    def setup_database(self):
        """Configura o banco de dados"""
        os.makedirs(os.path.dirname(CONFIG['SENT_DB_PATH']), exist_ok=True)
        self.conn = sqlite3.connect(CONFIG['SENT_DB_PATH'])
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sent_phones (
                phone TEXT PRIMARY KEY,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def is_sent(self, phone):
        """Verifica se o número já foi processado"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM sent_phones WHERE phone = ?", (phone,))
        return cursor.fetchone() is not None
    
    def mark_as_sent(self, phone):
        """Marca um número como enviado"""
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO sent_phones (phone) VALUES (?)", (phone,))
        self.conn.commit()
    
    def get_clients_to_message(self):
        """Obtém clientes do banco de dados principal"""
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(CONFIG['DATABASE_PATH']):
                logging.error(f"Arquivo de banco de dados não encontrado: {CONFIG['DATABASE_PATH']}")
                return []
            
            # Lê o arquivo em chunks para evitar sobrecarga de memória
            chunks = pd.read_csv(
                CONFIG['DATABASE_PATH'], 
                sep=';', 
                chunksize=1000,
                dtype=str,
                encoding='latin1',
                on_bad_lines='skip'
            )
            
            clients = []
            for chunk in chunks:
                # Processa apenas linhas com telefone válido
                if 'TELEFONE' not in chunk.columns:
                    logging.error("Coluna 'TELEFONE' não encontrada no banco de dados")
                    continue
                    
                chunk = chunk[chunk['TELEFONE'].notna()]
                
                # Remove espaços em branco e caracteres não numéricos
                chunk['TELEFONE'] = chunk['TELEFONE'].astype(str).str.replace(r'\D', '', regex=True)
                
                # Filtra números já enviados
                chunk = chunk[~chunk['TELEFONE'].apply(self.is_sent)]
                
                # Converte para lista de dicionários
                for _, row in chunk.iterrows():
                    clients.append(row.to_dict())
            
            return clients
        except Exception as e:
            logging.error(f"Erro ao ler banco de dados: {str(e)}")
            return []
