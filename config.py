# Configurações do CBot NovaEra

CONFIG = {
    # Caminhos de arquivos
    'DATABASE_PATH': 'database/database.txt',
    'SENT_DB_PATH': 'database/sent_phones.db',
    'LOG_FILE': 'logs/operation.log',
    'SESSION_DIR': 'session/',
    
    # Configurações de envio
    'MAX_MESSAGES_PER_SESSION': 15,  # Mensagens por execução
    'MIN_DELAY': 120,                # 2 minutos (em segundos)
    'MAX_DELAY': 300,                # 5 minutos (em segundos)
    'LONG_PAUSE': 900,               # 15 minutos (em segundos)
}
