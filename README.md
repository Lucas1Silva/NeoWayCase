# NeoWayCase

Repositório: https://github.com/Lucas1Silva/NeoWayCase
## Descrição

O NeoWayCase é uma aplicação REST desenvolvida em Python com FastAPI que permite o cadastro e consulta de clientes. A aplicação suporta autenticação via JWT utilizando um esquema Bearer Token, protegendo endpoints que realizam operações com clientes. Além disso, a aplicação disponibiliza um endpoint de status que informa o up-time do servidor e a quantidade de requisições processadas, armazenando essas métricas no Redis.
Arquitetura e Tecnologias Utilizadas

    Linguagem e Framework: Python + FastAPI
    Banco de Dados: PostgreSQL (acessado via SQLAlchemy)
    Cache/Métricas: Redis (para contagem de requisições)
    Autenticação: JWT com esquema HTTP Bearer (usando HTTPBearer)
    Testes: Testes unitários e de integração com Pytest, FastAPI TestClient e curl
    Conteinerização: Docker e Docker Compose
    Outras Dependências: pydantic, pydantic-settings, passlib, PyJWT, etc.

## A aplicação está estruturada em uma arquitetura modular, com camadas para:

    Configurações e Inicialização: (em app/core/)
    Modelos (Domínio): (em app/models/)
    Repositórios: (em app/repositories/)
    Serviços (Lógica de Negócio): (em app/services/)
    Utilitários: (em app/utils/)
    Rotas e Autenticação: (em app/api/ e app/dependencies.py)

## Funcionalidades

    Cadastro de Clientes: Cadastro de clientes (pessoas físicas e jurídicas) utilizando o documento único (CPF/CNPJ) como chave.
    Consulta de Clientes: Busca de clientes, com filtros por nome/razão social e ordenação alfabética.
    Autenticação de Usuários: Registro e login de usuários, gerando um token JWT para acesso aos endpoints protegidos.
    Endpoints Protegidos: Endpoints de clientes que só podem ser acessados com um token JWT válido.
    Status do Servidor: Endpoint /status que retorna o tempo de atividade do servidor e o número de requisições realizadas (armazenadas no Redis).

## Como Executar
## Pré-requisitos

    Docker e Docker Compose instalados.
    (Opcional) Acesso ao repositório Git para clonar o projeto.

Passo a Passo

    Clone o Repositório:

git clone https://github.com/Lucas1Silva/NeoWayCase.git
cd NeoWayCase

Inicie os Containers com Docker Compose:

No diretório raiz do projeto, execute:

    docker-compose up --build

    Isso iniciará os containers para:
        PostgreSQL (na porta mapeada 5433 do host),
        Redis (na porta 6379),
        Aplicação FastAPI (na porta 8000).

    Acessando a API:

    A aplicação ficará disponível em http://localhost:8000.

# Como Testar a Aplicação
# Usando a Documentação Interativa (Swagger UI)

    Acesse a Documentação:

    Abra o navegador e acesse http://localhost:8000/docs. Lá você encontrará todos os endpoints documentados.

    Registro de Usuário:
        Localize o endpoint POST /auth/register.
        Clique em Try it out.
        Insira o seguinte JSON no corpo da requisição:

{
  "username": "usuario123",
  "password": "senha123"
}

Clique em Execute.
Resultado Esperado: Um JSON com o token JWT, similar a:

    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3VhcmlvMTIzIiwiZXhwIjoxNzM5NTQ1NjU0fQ.w0XXiGjVHS9wXjNDuB6QHCwq1nWn_PoBxzCRMTD52KY",
      "token_type": "bearer"
    }

Autorização com Bearer Token:

    Copie o valor do access_token retornado.
    Clique no botão Authorize no canto superior direito da documentação.
    Será exibido apenas um campo para inserir o token. Insira o token no formato:

    Bearer <seu_token_aqui>

    Clique em Authorize e depois em Close.

Testar Endpoints Protegidos (Clientes):

    Cadastrar Cliente:
        Acesse o endpoint POST /clients/.
        Clique em Try it out.
        Insira o seguinte JSON:

            {
              "document": "12345678901",
              "name": "Cliente Teste",
              "is_blocked": false
            }

            Clique em Execute.
            Resultado Esperado: Os dados do cliente cadastrado serão retornados.
        Consultar Clientes:
            Use o endpoint GET /clients/ para listar clientes.
            Clique em Try it out e, se necessário, informe um parâmetro de busca (por exemplo, name).
            Clique em Execute para ver os clientes cadastrados.

Usando cURL

Para testar via cURL, você pode usar o seguinte comando (certifique-se de substituir <seu_token_aqui> pelo token obtido):

curl -X 'POST' \
  'http://0.0.0.0:8000/clients/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <seu_token_aqui>' \
  -H 'Content-Type: application/json' \
  -d '{
  "document": "12345678901",
  "name": "Cliente Teste",
  "is_blocked": false
}'

# Observação: Certifique-se de que o cabeçalho Content-Type está definido como application/json e que o token JWT está inserido corretamente sem duplicar o prefixo "Bearer".
Conclusão

Neste projeto, implementamos uma API REST com autenticação JWT, protegendo os endpoints com um Bearer token. Utilizamos Docker para conteinerizar a aplicação, PostgreSQL para persistência de dados, Redis para contagem de requisições e FastAPI para criação dos endpoints. Siga os passos acima para executar e testar a aplicação.

Se houver dúvidas ou sugestões, sinta-se à vontade para abrir issues ou enviar pull requests!