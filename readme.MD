# Documentação do Projeto Business Management

Bem-vindo ao projeto **Business Management**! Esta documentação fornecerá um guia completo para configurar, executar e gerenciar a aplicação utilizando o Docker Compose. O projeto consiste em um backend FastAPI, um frontend Next.js, um banco de dados PostgreSQL e um sistema de mensagens Kafka com Zookeeper.

---

## Índice

1. [Visão Geral do Projeto](#visão-geral-do-projeto)
2. [Pré-requisitos](#pré-requisitos)
3. [Configuração de Variáveis de Ambiente](#configuração-de-variáveis-de-ambiente)
    - [Arquivo `.env.example`](#arquivo-envexample)
4. [Configuração do Docker Compose](#configuração-do-docker-compose)
5. [Executando a Aplicação](#executando-a-aplicação)
6. [Acessando os Serviços](#acessando-os-serviços)
7. [Gerenciando a Aplicação](#gerenciando-a-aplicação)
    - [Visualizando Logs](#visualizando-logs)
    - [Parando os Serviços](#parando-os-serviços)
    - [Removendo Contêineres e Volumes](#removendo-contêineres-e-volumes)
8. [Solução de Problemas](#solução-de-problemas)
9. [Recursos Adicionais](#recursos-adicionais)
10. [Conclusão](#conclusão)

---

## Visão Geral do Projeto

O **Business Management** é uma aplicação full-stack composta por:

- **Backend:** Aplicação FastAPI que gerencia requisições de API, interações com o banco de dados e mensagens Kafka.
- **Frontend:** Aplicação Next.js que fornece a interface do usuário.
- **Banco de Dados:** PostgreSQL para armazenamento de dados.
- **Mensageria:** Kafka e Zookeeper para mensagens em tempo real e gerenciamento de eventos.

O Docker e o Docker Compose são utilizados para containerizar e orquestrar esses serviços, garantindo um ambiente consistente e isolado.

---

## Pré-requisitos

Antes de configurar o projeto, certifique-se de que seu ambiente de desenvolvimento atende aos seguintes requisitos:

- **Sistema Operacional:** Linux, macOS ou Windows com WSL2 (recomendado para Windows).
- **Docker:** Versão 27.2.0, Build 3ab4256
  - [Baixar Docker](https://www.docker.com/get-started)
- **Docker Compose:** Incluído no Docker Desktop. Verifique a compatibilidade com a versão do Docker instalada.
- **Node.js:** Versão 22.10.0
  - [Baixar Node.js](https://nodejs.org/en/download/)
- **Python 3:** Certifique-se de que o Python 3 está instalado. Verifique com:
  ```bash
  python3 --version
  ```
- **Git:** Para clonar o repositório.
  - [Baixar Git](https://git-scm.com/downloads)

> **Nota:** Assegure-se de que o Docker está em execução antes de prosseguir. Você pode verificar a instalação do Docker executando:
> ```bash
> docker --version
> ```

---

## Configuração de Variáveis de Ambiente

A configuração adequada das variáveis de ambiente é crucial para o funcionamento correto da aplicação. Todas as variáveis de ambiente estão definidas no arquivo `.env.example` na raiz do projeto.

### Arquivo `.env.example`

O arquivo `.env.example` contém todas as variáveis necessárias para a configuração inicial do ambiente. Para criar o arquivo `.env` a partir do `.env.example`, execute o seguinte comando na raiz do projeto:

```bash
cp .env.example .env
```

> **Importante:** Após copiar o arquivo, edite o `.env` para preencher os valores específicos de seu ambiente, como credenciais do banco de dados e chaves de segurança.

**Exemplo de `.env.example`:**

```dotenv
# Configuração do Banco de Dados
DATABASE_DRIVER=postgresql
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=postgres         # Nome do serviço no Docker
DATABASE_PORT=5432
DATABASE_NAME=your_db_name

# Credenciais do Super Admin
SUPER_ADMIN_NAME=Admin
SUPER_ADMIN_EMAIL=admin@example.com
SUPER_ADMIN_PASSWORD=your_secure_password

# Segurança
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuração do Kafka
KAFKA_URL=kafka:9092

# Configuração do Frontend

# URL da API (use o nome do serviço do backend no Docker)
NEXT_PUBLIC_API_URL=http://app:8000

# URLs dos WebSockets
NEXT_PUBLIC_WS_HISTORY_URL=ws://app:8000/chat/ws/history?token=
NEXT_PUBLIC_WS_SEND_URL=ws://app:8000/chat/ws/send?token=
```

> **Nota:** As credenciais do usuário inicial (Super Admin) estão nas chaves `SUPER_ADMIN_NAME`, `SUPER_ADMIN_EMAIL` e `SUPER_ADMIN_PASSWORD`. Esses valores devem ser definidos durante a configuração para criar automaticamente o usuário inicial da aplicação.

---

## Configuração do Docker Compose

> **Nota:** Assegure-se de que o arquivo `docker-compose.yml` está corretamente configurado conforme as necessidades do projeto. Este arquivo define os serviços, redes e volumes necessários para a aplicação.

---

## Executando a Aplicação

Siga os passos abaixo para construir e executar todos os serviços utilizando o Docker Compose.

### 1. Clonar o Repositório

Se ainda não o fez, clone o repositório para sua máquina local:

```bash
git clone git@github.com:hgo19/business-management.git
cd business-management
```

### 2. Configurar as Variáveis de Ambiente

Certifique-se de que o arquivo `.env` está corretamente configurado conforme descrito na seção [Configuração de Variáveis de Ambiente](#configuração-de-variáveis-de-ambiente).

### 3. Dar Permissões ao Script de Entrada

Assegure-se de que o script `entrypoint.sh` tenha permissões de execução:

```bash
chmod +x backend/entrypoint.sh
```

### 4. Construir e Iniciar os Contêineres

Execute o seguinte comando na raiz do projeto para construir e iniciar todos os serviços em modo destacado:

```bash
docker-compose up -d --build
```

- `-d`: Executa os contêineres em segundo plano (detached mode).
- `--build`: Força a reconstrução das imagens Docker, garantindo que as últimas alterações sejam incluídas.

### 5. Verificar o Status dos Serviços

Para verificar se todos os serviços estão em execução, utilize:

```bash
docker-compose ps
```

Você deverá ver todos os serviços (`zookeeper`, `kafka`, `postgres`, `app`, `frontend`) listados como `Up`.

---

## Acessando os Serviços

Após os contêineres estarem em execução, você pode acessar os serviços através do seu navegador ou clientes apropriados.

### Frontend (Next.js)

- **URL:** [http://localhost:3000](http://localhost:3000)
- **Descrição:** Interface do usuário da aplicação.

### Backend (FastAPI)

- **URL:** [http://localhost:8000](http://localhost:8000)
- **Descrição:** Gerencia requisições de API, autenticação e funcionalidades de backend.
- **Documentação da API:** Acessível em [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

### Banco de Dados PostgreSQL

- **Host:** `localhost`
- **Porta:** `5432`
- **Banco de Dados:** Conforme especificado no arquivo `.env` (`DATABASE_NAME`)
- **Usuário:** Conforme especificado no arquivo `.env` (`DATABASE_USER`)
- **Senha:** Conforme especificado no arquivo `.env` (`DATABASE_PASSWORD`)

> **Nota:** Utilize ferramentas como `pgAdmin`, `DBeaver` ou `psql` para interagir com o banco de dados PostgreSQL.

### Kafka

- **Host:** `localhost`
- **Porta:** `9092`
- **Descrição:** Gerencia mensagens em tempo real e streaming de eventos.

### Zookeeper

- **Host:** `localhost`
- **Porta:** `2181`
- **Descrição:** Gerencia metadados do cluster Kafka.

---

## Gerenciando a Aplicação

### Visualizando Logs

Para visualizar os logs de um serviço específico, utilize o comando `docker-compose logs` seguido do nome do serviço.

- **Visualizar Todos os Logs:**
  ```bash
  docker-compose logs -f
  ```

- **Visualizar Logs de um Serviço Específico:**
  ```bash
  docker-compose logs -f frontend
  docker-compose logs -f app
  docker-compose logs -f postgres
  docker-compose logs -f kafka
  docker-compose logs -f zookeeper
  ```

> **Dica:** A flag `-f` permite acompanhar os logs em tempo real.

### Parando os Serviços

Para parar todos os serviços sem removê-los, utilize:

```bash
docker-compose stop
```

### Iniciando os Serviços Novamente

Para iniciar os contêineres parados:

```bash
docker-compose start
```

### Reiniciando os Serviços

Para reiniciar todos os serviços:

```bash
docker-compose restart
```

### Removendo Contêineres e Redes

Para parar e remover todos os contêineres, redes e recursos definidos no `docker-compose.yml`, execute:

```bash
docker-compose down
```

- **Remover Volumes Nomeados:**
  Para também

 remover os volumes nomeados (por exemplo, `postgres_data`), adicione a flag `-v`:
  
  ```bash
  docker-compose down -v
  ```

> **Atenção:** Remover volumes deletará todos os dados persistidos, incluindo o banco de dados PostgreSQL.

---

## Solução de Problemas

### Problemas Comuns e Soluções

1. **Conflitos de Porta:**
   - **Problema:** Portas `3000`, `8000`, `5432`, `9092` ou `2181` já estão em uso.
   - **Solução:** Identifique o serviço que está ocupando a porta utilizando:
     ```bash
     lsof -i :NUMERO_DA_PORTA
     ```
     Substitua `NUMERO_DA_PORTA` pela porta conflitante. Pare ou reconfigure o serviço conforme necessário.

2. **Daemon do Docker Não Está Rodando:**
   - **Problema:** Comandos Docker falham com erros indicando que o daemon do Docker não está em execução.
   - **Solução:** Inicie o Docker Desktop ou certifique-se de que o daemon do Docker está ativo.

3. **Variáveis de Ambiente Não Carregadas:**
   - **Problema:** Serviços falham ao iniciar ou comportam-se de forma inesperada devido a variáveis de ambiente ausentes.
   - **Solução:** Verifique se o arquivo `.env` está corretamente configurado e referenciado no `docker-compose.yml`. Assegure-se de que não há erros de sintaxe.

4. **Backend Não Consegue Conectar ao Banco de Dados:**
   - **Problema:** O backend FastAPI não consegue estabelecer conexão com o PostgreSQL.
   - **Solução:**
     - Verifique se o serviço PostgreSQL está ativo.
     - Confirme se as variáveis `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USER`, `DATABASE_PASSWORD` e `DATABASE_NAME` no arquivo `.env` estão corretas.
     - Verifique os logs dos serviços `app` e `postgres`:
       ```bash
       docker-compose logs app
       docker-compose logs postgres
       ```

5. **Problemas de Conexão com Kafka:**
   - **Problema:** O backend falha ao conectar-se ao Kafka.
   - **Solução:**
     - Certifique-se de que os serviços Kafka e Zookeeper estão em execução.
     - Verifique a variável `KAFKA_URL` no arquivo `.env`.
     - Confira os logs dos serviços `kafka` e `app`.

6. **Frontend Não Constrói ou Inicia Corretamente:**
   - **Problema:** O frontend Next.js falha durante a construção ou inicialização.
   - **Solução:**
     - Verifique os logs do frontend para mensagens de erro específicas:
       ```bash
       docker-compose logs frontend
       ```
     - Assegure-se de que todas as dependências estão corretamente listadas no `package.json`.
     - Confirme se as variáveis de ambiente no `.env` estão corretas.

### Solução de Problemas Avançada

- **Inspecionar Detalhes do Contêiner:**
  ```bash
  docker inspect NOME_DO_CONTÊINER
  ```
  Substitua `NOME_DO_CONTÊINER` pelo nome do contêiner problemático.

- **Acessar o Shell do Contêiner:**
  ```bash
  docker exec -it NOME_DO_CONTÊINER sh
  ```
  Isso permite executar comandos dentro do contêiner para depuração.

- **Reconstruir Contêineres Sem Cache:**
  Às vezes, camadas em cache podem causar problemas. Reconstrua sem utilizar o cache:
  ```bash
  docker-compose build --no-cache
  docker-compose up -d
  ```

---

## Recursos Adicionais

- **Documentação do Docker:** [https://docs.docker.com/](https://docs.docker.com/)
- **Documentação do Docker Compose:** [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- **Documentação do FastAPI:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **Documentação do Next.js:** [https://nextjs.org/docs](https://nextjs.org/docs)
- **Documentação do PostgreSQL:** [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
- **Documentação do Kafka:** [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
- **Documentação do Zookeeper:** [https://zookeeper.apache.org/doc/](https://zookeeper.apache.org/doc/)

---

## Conclusão

Seguindo esta documentação, você conseguirá configurar, executar e gerenciar o projeto **Business Management** de maneira eficiente utilizando o Docker Compose. Esta configuração garante um ambiente consistente para desenvolvimento, testes e implantação, facilitando a colaboração e a escalabilidade da aplicação.

**Principais Pontos:**

- **Estrutura Modular:** Separação clara entre backend e frontend para melhor manutenção.
- **Redes Docker:** Utilização de redes internas para comunicação entre serviços, evitando conflitos de `localhost`.
- **Variáveis de Ambiente:** Configuração adequada para flexibilidade em diferentes ambientes.
- **Logs e Monitoramento:** Ferramentas integradas para monitoramento e depuração dos serviços.
- **Segurança:** Boas práticas para gerenciamento de informações sensíveis e acesso seguro aos serviços.

Caso encontre problemas ou tenha dúvidas adicionais, sinta-se à vontade para buscar ajuda nos recursos fornecidos ou entrar em contato comigo: [Hugo](https://www.linkedin.com/in/hugo-leop/)