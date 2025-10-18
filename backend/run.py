"""
Arquivo principal para executar a aplicação Flask
"""
import os
from app import create_app

# Determinar ambiente
config_name = os.environ.get('FLASK_ENV', 'development')

# Criar aplicação
app = create_app(config_name)

if __name__ == '__main__':
    # Executar em modo de desenvolvimento
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )

