# ARCHITECTURE AUDIT REPORT

Project: code-smells-project
Stack:   Python + Flask 3.1.1
Files:   4 | ~784

## Summary
CRITICAL: 4 | HIGH: 2 | MEDIUM: 2 | LOW: 0 | Total: 8 findings

## Findings

### [CRITICAL] Spaghetti Code / SQL Injection
- **File:** [models.py](file:///G:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py):28, 48-50, 58-60, 68, 92, 109-111, 126-129, 140, 148-151, 155, 157-161, 163-166, 174, 188, 192, 220, 224, 279-281, 289-298
- **Description:** O projeto faz uso extensivo de consultas SQL puras construídas por meio de concatenação de strings com dados fornecidos pelo usuário. Por exemplo, na busca de produto por ID (`models.py:28`) e na validação de login (`models.py:109-111`), os parâmetros são injetados diretamente na query string.
- **Impact:** Vulnerável a SQL Injection de forma crítica. Um atacante pode burlar a autenticação de login (ex: inserindo `' OR '1'='1`), extrair dados sigilosos ou modificar a base de dados.
- **Recommendation:** Substituir todas as concatenações por Prepared Statements / consultas parametrizadas do SQLite, utilizando o caractere curinga `?` e passando os parâmetros como uma tupla/lista.

---

### [CRITICAL] Insecure Cryptography / Plain Text Passwords
- **File:** [models.py](file:///G:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py):109-111, 126-129 e [database.py](file:///G:/Projects/mba-ia-refactor-projects-skill/code-smells-project/database.py):75-83
- **Description:** O sistema armazena as senhas dos usuários em texto limpo (plain text). Tanto na inserção inicial de usuários de teste (`database.py`) quanto na criação de novos usuários (`models.py:126-129`) e login (`models.py:109-111`), as senhas não passam por nenhum processo de hashing.
- **Impact:** Se a base de dados SQLite (`loja.db`) for vazada ou acessada indevidamente, todas as credenciais de clientes e administradores serão expostas imediatamente.
- **Recommendation:** Refatorar o fluxo para criptografar as senhas usando algoritmos robustos e modernos de hash como PBKDF2 com Salt. Sugere-se utilizar `werkzeug.security.generate_password_hash` e `check_password_hash`, que já estão disponíveis no Flask/Werkzeug.

---

### [CRITICAL] Auth Illusion / SQL Backdoor
- **File:** [app.py](file:///G:/Projects/mba-ia-refactor-projects-skill/code-smells-project/app.py):59-79
- **Description:** A rota `/admin/query` permite que qualquer requisição HTTP POST execute comandos SQL arbitrários no banco de dados sem nenhuma validação, sanitização ou autenticação de token/sessão.
- **Impact:** Isso funciona como um backdoor administrativo completo exposto publicamente na internet. Qualquer pessoa pode apagar tabelas (`DROP TABLE`), extrair dados de usuários ou injetar registros arbitrários.
- **Recommendation:** Remover completamente a rota `/admin/query` da aplicação, pois ela viola os princípios fundamentais de segurança de software.

---

### [CRITICAL] Hardcoded Secrets & Info Leakage
- **File:** [app.py](file:///G:/Projects/mba-ia-refactor-projects-skill/code-smells-project/app.py):7 e [controllers.py](file:///G:/Projects/mba-ia-refactor-projects-skill/code-smells-project/controllers.py):289
- **Description:** A chave de criptografia do Flask (`SECRET_KEY`) está chumbada no código-fonte como `"minha-chave-super-secreta-123"`. Adicionalmente, no endpoint `/health` (`controllers.py:289`), essa chave secreta e o estado de debug são explicitamente retornados no payload JSON de resposta HTTP.
- **Impact:** Com a `SECRET_KEY` exposta publicamente via código ou pelo endpoint `/health`, um atacante pode forjar cookies de sessão do Flask, permitindo Personificação de Usuário e controle da aplicação.
- **Recommendation:** Carregar a `SECRET_KEY` a partir de variáveis de ambiente (`os.getenv("SECRET_KEY")`) e remover a chave secreta e informações internas de depuração do retorno JSON do endpoint `/health`.

---

### [HIGH] The Blob / God Class
- **File:** [app.py](file:///G:/Projects/mba-ia-refactor-projects-skill/code-smells-project/app.py):47-79
- **Description:** O arquivo `app.py` age como "God Class", concentrando a configuração de roteamento geral da API, inicialização de conexões e execução direta de comandos SQL administrativos e de backdoor (`/admin/reset-db` e `/admin/query`). Isso quebra a separação de responsabilidades.
- **Impact:** Acoplamento excessivo que impede testes unitários e dificulta a evolução de regras de autenticação/autorização de rotas administrativas.
- **Recommendation:** Segregar a lógica das rotas em controllers apropriados e views/routes organizadas. Centralizar o bootstrap e composition root em `app.py` apenas delegando para as camadas inferiores.

---

### [HIGH] Query N+1 Performance Bottleneck
- **File:** [models.py](file:///G:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py):171-201 e 203-233
- **Description:** As funções `get_pedidos_usuario` e `get_todos_pedidos` realizam consultas em laço (loops). Primeiro busca os pedidos; para cada pedido, faz uma consulta na tabela `itens_pedido`; e para cada item do pedido, faz outra consulta na tabela `produtos` para obter o nome do produto.
- **Impact:** Se houver 100 pedidos com média de 3 itens cada, a API executará 1 + 100 + 300 = 401 queries separadas no banco de dados. Isso causa lentidão extrema e sobrecarga de I/O do banco à medida que o histórico de vendas cresce.
- **Recommendation:** Reescrever a busca usando cláusulas `JOIN` do SQL para trazer todos os pedidos, itens e nomes dos produtos em uma única consulta otimizada, e estruturar o agrupamento no código Python.

---

### [MEDIUM] Cover Your Assets / Generic Exception Swallowing
- **File:** [controllers.py](file:///G:/Projects/mba-ia-refactor-projects-skill/code-smells-project/controllers.py):5-13, 14-22, 24-63, etc.
- **Description:** Praticamente todas as funções de controle usam blocos genéricos `try-except Exception as e` para capturar qualquer exceção e retornar a mensagem interna do erro diretamente no JSON de erro para o cliente (`return jsonify({"erro": str(e)}), 500`).
- **Impact:** Silencia logs estruturados internos do servidor e vaza detalhes estruturais do banco de dados (ex: erros de sintaxe SQL, nomes de colunas) para o cliente externo, facilitando ataques dirigidos.
- **Recommendation:** Implementar um middleware / decorador de tratamento de exceções global no Flask (`@app.errorhandler(Exception)`) para interceptar erros inesperados de forma genérica, logar o erro internamente com stack trace completo, e responder ao cliente com uma mensagem de erro genérica padrão e segura.

---

### [MEDIUM] Referential Integrity Failure / Cascade Delete Failure
- **File:** [database.py](file:///G:/Projects/mba-ia-refactor-projects-skill/code-smells-project/database.py):46-53 e [models.py](file:///G:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py):65-70
- **Description:** A tabela `itens_pedido` é relacionada aos pedidos e produtos por chaves lógicas, mas não declara restrições explícitas de chaves estrangeiras com `ON DELETE CASCADE`. Além disso, a remoção de produtos (`deletar_produto`) é executada por um `DELETE` direto, mantendo linhas órfãs em `itens_pedido`.
- **Impact:** Inconsistência relacional no banco de dados e acúmulo de dados lixo e registros órfãos que quebram relatórios futuros.
- **Recommendation:** Declarar explicitamente as chaves estrangeiras (`FOREIGN KEY`) com `ON DELETE CASCADE` na criação das tabelas e garantir que o SQLite execute com constraints habilitadas (`PRAGMA foreign_keys = ON;`).
