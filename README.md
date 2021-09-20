# Neoway API

O repositório disponibiliza uma API REST que permite carregar um arquivo texto contendo dados no modelo encaminhado pelo e-mail.

## Tecnologias

Neste projeto foram utilizadas as tecnologias abaixo:

- Python
- Flask (micro-framework)
- Postgres
- Redis
- Husky (GIT Commits - DEV)
- Docker

## Requerimentos

- Ter docker instalado na máquina
- Ter as portas ***5000*** e ***5432*** liberadas para acesso

## Instalação

1. Baixar código-fonte do repositório (Pode-se usar `git clone`)
2. Copiar arquivo `/app/.env.example` para `/app/.env` para setar as variáveis de ambiente
2. Acessar a raiz do repositório baixado e executar `make` para instalar os containers necessários para a aplicação.
3. Executar o comando `make generate-key` para gerar a key que sera informada no arquivo `/app/.env` na tag SECRET KEY
3. Executar `make create-db` para iniciar a criação da estrutura do banco de dados (Estrutura Banco de dados)

## Como utilizar a API

Após a instalação a API ficará disponível através do endereço [http://127.0.0.1:5000][PlGh], onde terá os recursos abaixo.


### Recursos disponíveis para acesso via API

| Método | Recurso | Endpoint |
| ------ | ------ | ------ |
| GET | Status Importação | [/api/sales/import/<in:**ID_ARQUIVO**>/status][PlGh] |
| POST | Importar arquivo | [/api/sales/import/file][PlGh] |

### Recurso [Importar Arquivo]:

#### Request
`POST /api/sales/import/file`
    
    curl -i -X POST -H "Accept: text/plain" -H "Content-Type: text/plain" --data-binary "@ARQUIVO" http://127.0.0.1:5000/api/sales/import/file

#### Response

    HTTP/1.1 200 OK
    Date: Mon, 20 Sep 2021 03:36:28 GMT
    Connection: close
    Content-Type: application/json
    Content-Length: 133
    Body:
    {
        "message":"Arquivo enviado com sucesso! Logo iremos processá-lo. Por favor, verique seu status em /api/sales/import/ID_ARQUIVO/status"
    }

### Recurso [Status Importação]:

#### Request
`GET /api/sales/import/ID_ARQUIVO/status`

    curl -i -X GET -H "Accept: application/json" -H "Content-Type: application/json"  http://127.0.0.1:5000/api/sales/import/2/status
    
#### Response
    
    HTTP/1.1 200 OK
    Date: Mon, 20 Sep 2021 03:38:07 GMT
    Connection: close
    Content-Type: application/json
    Content-Length: 203
    
    {
        "job_status":"started",
        "logs":[
            "2021-09-20 00:36:29 - Foo",
            "2021-09-20 00:36:29 - Foo",
            "2021-09-20 00:36:31 - Foo"
        ],
        "status":"processing"
    }

# Banco de dados

Utilizado banco Postgres na versão 12.

## Tabelas

- Customer
- Store
- Sale
- Log
- SaleFile

## DDL (Data Definition Language)
````
-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION neoway;

-- DROP TYPE statusenum;

CREATE TYPE statusenum AS ENUM (
	'processing',
	'completed',
	'canceled',
	'failed',
	'error');

-- DROP SEQUENCE public.log_id_seq;

CREATE SEQUENCE public.log_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.sale_file_id_seq;

CREATE SEQUENCE public.sale_file_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.sale_id_seq;

CREATE SEQUENCE public.sale_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- public.alembic_version definition

-- Drop table

-- DROP TABLE public.alembic_version;

CREATE TABLE public.alembic_version (
	version_num varchar(32) NOT NULL,
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);


-- public.customer definition

-- Drop table

-- DROP TABLE public.customer;

CREATE TABLE public.customer (
	cpf varchar(11) NOT NULL,
	CONSTRAINT customer_pkey PRIMARY KEY (cpf)
);


-- public.sale_file definition

-- Drop table

-- DROP TABLE public.sale_file;

CREATE TABLE public.sale_file (
	id serial4 NOT NULL,
	status statusenum NULL,
	job_id varchar(100) NULL,
	CONSTRAINT sale_file_pkey PRIMARY KEY (id)
);


-- public.store definition

-- Drop table

-- DROP TABLE public.store;

CREATE TABLE public.store (
	cnpj varchar(14) NOT NULL,
	CONSTRAINT store_pkey PRIMARY KEY (cnpj)
);


-- public.log definition

-- Drop table

-- DROP TABLE public.log;

CREATE TABLE public.log (
	id serial4 NOT NULL,
	message text NULL,
	created_at timestamptz NULL,
	sale_file_id int4 NULL,
	CONSTRAINT log_pkey PRIMARY KEY (id),
	CONSTRAINT log_sale_file_id_fkey FOREIGN KEY (sale_file_id) REFERENCES public.sale_file(id)
);


-- public.sale definition

-- Drop table

-- DROP TABLE public.sale;

CREATE TABLE public.sale (
	id serial4 NOT NULL,
	private int4 NOT NULL,
	unfinished int4 NOT NULL,
	last_purchase date NULL,
	average_ticket_price numeric(10, 2) NULL,
	ticket_price_last_purchase numeric(10, 2) NULL,
	customer_id varchar(11) NULL,
	most_visited_store varchar(14) NULL,
	last_purchase_store varchar(14) NULL,
	CONSTRAINT sale_pkey PRIMARY KEY (id),
	CONSTRAINT sale_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customer(cpf),
	CONSTRAINT sale_last_purchase_store_fkey FOREIGN KEY (last_purchase_store) REFERENCES public.store(cnpj),
	CONSTRAINT sale_most_visited_store_fkey FOREIGN KEY (most_visited_store) REFERENCES public.store(cnpj)
);
````