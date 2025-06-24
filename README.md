# CBot NovaEra - Sistema de Cobrança Automatizado

Solução completa para envio de mensagens de cobrança via WhatsApp, otimizada para Termux com autenticação por QR Code.

## Recursos Principais
- Autenticação via QR Code para WhatsApp pessoal
- Compatibilidade total com Termux (Android)
- Processamento eficiente de grandes bancos de dados (5GB+)
- Sistema anti-bloqueio inteligente
- Logs em tempo real
- Interface profissional

## Pré-requisitos
- Termux atualizado
- Python 3.10+
- Espaço em disco suficiente (recomendado 10GB+)

## Instalação no Termux

```bash
# Atualizar pacotes
pkg update -y && pkg upgrade -y

# Instalar dependências
pkg install python git wget -y

# Instalar Chrome para Termux
wget https://github.com/Hax4us/TermuxBlack/raw/master/storage/termuxblack/termuxblack.deb
dpkg -i termuxblack.deb

# Instalar WebDriver
pkg install chromium -y

# Clonar repositório
git clone https://github.com/seuusuario/CBot_NovaEra.git
cd CBot_NovaEra

# Instalar dependências Python
pip install -r requirements.txt

# Dar permissões de armazenamento
termux-setup-storage
