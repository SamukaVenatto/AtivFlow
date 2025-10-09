#!/bin/bash

# Instalar dependências do Python
pip install -r requirements.txt

# Instalar Node.js e npm se não estiverem disponíveis
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Instalar pnpm
if ! command -v pnpm &> /dev/null; then
    npm install -g pnpm
fi

# Build do frontend
cd frontend
pnpm install
pnpm run build

# Copiar arquivos do frontend para o backend
mkdir -p ../backend/src/static
cp -r dist/* ../backend/src/static/

echo "Build concluído com sucesso!"
