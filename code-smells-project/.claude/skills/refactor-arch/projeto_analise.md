# Análise de Projeto — Heurísticas

Este documento define regras heurísticas para detectar a stack tecnológica e mapear a arquitetura atual do projeto sob análise.

## 1. Detecção de Stack Tecnológica

### Python / Flask
- **Presença de arquivos:** `app.py`, `wsgi.py`, `requirements.txt`.
- **Conteúdo de arquivos:**
  - Importação de `flask`, `Flask`, `Blueprint`, `jsonify`, `request` nos arquivos `.py`.
  - Dependências listadas no `requirements.txt` como `flask`, `Flask-SQLAlchemy`, `sqlite3`.

### Node.js / Express
- **Presença de arquivos:** `package.json`, `package-lock.json`, `app.js`, `server.js`, `index.js`.
- **Conteúdo de arquivos:**
  - `require('express')` ou `import express from 'express'`.
  - Scripts `npm start` ou `npm run dev` no `package.json`.

---

## 2. Detecção de Banco de Dados

- **SQLite:** Presença de arquivos `.db` ou `sqlite3` importado/requerido, conexões `:memory:`.
- **PostgreSQL / MySQL:** Presença de dependências como `pg`, `mysql2`, `psycopg2` ou strings de conexão contendo `postgresql://` ou `mysql://`.

---

## 3. Mapeamento de Arquitetura

Analise a estrutura de diretórios e o nível de separação de responsabilidades (camadas):

- **Monolito de Arquivo Único (God File):**
  - Todo o código de roteamento, lógica de negócio, manipulação de banco de dados e controle de respostas está em um único arquivo (ex: `app.py` ou `AppManager.js`).
- **Arquitetura Acoplada (Sem MVC):**
  - Roteamento direto acoplado a funções de consulta ao banco de dados no mesmo arquivo.
  - Mistura de lógica de domínio em métodos que deveriam apenas ler/escrever dados (Models).
  - Segredos misturados com código executável.
- **Arquitetura Parcialmente Separada:**
  - Divisão de arquivos baseada em camadas (ex: diretórios `models`, `routes`, `services`) mas sem aderência estrita a injeção de dependências, tratamento de erros centralizado ou isolamento de segredos.
