# Controle de Ingestão de Água - README

## Visão Geral

Este projeto é uma aplicação para controle de ingestão de água, composta por três componentes principais:

1. **Frontend**: Responsável pela interface de usuário, utilizando Nginx como servidor.
2. **Backend**: Implementado em Python utilizando Flask, é responsável pela lógica de negócios.
3. **Banco de Dados PostgreSQL**: Utilizado para persistência de dados.

Esses componentes são executados em containers Docker e são orquestrados em um cluster Kubernetes usando `kind`.

## Estrutura do Projeto

```plaintext
CONTROLE-HSO-KUBERNETES/
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── Dockerfile.backend
│   ├── models.py
│   ├── requirements.txt
│   └── routes.py
├── frontend/
│   ├── assets/
│   ├── Dockerfile.frontend
│   ├── index.html
│   ├── script.js
│   └── style.css
├── Dockerfile.postgres
├── README.md
├── backend-deployment.yml
├── backend-service.yml
├── frontend-deployment.yml
├── frontend-service.yml
├── postgres-deployment.yml
└── postgres-service.yml
```
## Pré-requisitos

- Docker
- Kind (Kubernetes in Docker)
- kubectl

## Passo a Passo para Configuração

### 1. Build das Imagens Docker

Primeiro, você deve criar as imagens Docker para cada componente.

#### Backend

Navegue até a pasta `backend` e execute:

```bash
docker build -t controle-agua-backend:v1.0.0 -f Dockerfile.backend .
```

#### Frontend

Navegue até a pasta `frontend` e execute:

```bash
docker build -t controle-agua-frontend:v1.0.0 -f Dockerfile.frontend .
```

#### Banco de Dados - PostgreSQL

Navegue até a pasta `raiz` e execute:

```bash
docker build -t controle-agua-db:v1.0.0 -f Dockerfile.postgres .
```

### 2. Criar um Cluster no Kind

Crie um cluster Kubernetes utilizando `kind`:

```bash
kind create cluster --name controle-agua-prod
```

### 3. Criar o Namespace

Crie um namespace para a aplicação:

```bash
kubectl create namespace controle-agua-prod
```

### 4. Carregar as Imagens no Cluster

Para carregar as imagens Docker que você acabou de buildar no cluster `kind`, utilize:

```bash
kind load docker-image controle-agua-backend:v1.0.0 --name controle-agua-prod
kind load docker-image controle-agua-frontend:v1.0.0 --name controle-agua-prod
kind load docker-image controle-agua-db:v1.0.0 --name controle-agua-prod
```

### 5. Aplicar os Deployments e Services

Aplique os arquivos de configuração:

```bash
kubectl apply -f backend-deployment.yml -n controle-agua-prod
kubectl apply -f backend-service.yml -n controle-agua-prod

kubectl apply -f frontend-deployment.yml -n controle-agua-prod
kubectl apply -f frontend-service.yml -n controle-agua-prod

kubectl apply -f postgres-deployment.yml -n controle-agua-prod
kubectl apply -f postgres-service.yml -n controle-agua-prod

Poderia ser utilizado apenas um arquivo de deployment e incluido o service dentro dele mais preferi separar para deixar mais fácil de entendimento.
```

### 6. Configurar o Port-Forward

Por fim, você pode acessar a aplicação através do serviço frontend utilizando o comando:

```bash
kubectl port-forward service/frontend-service 8080:80 -n controle-agua-prod

Agora, você pode acessar a aplicação no navegador através do endereço [http://localhost:8080](http://localhost:8080).

```

## Licença

Este projeto é licenciado sob os termos da licença MIT. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.

## Contato

- **Nome:** Arimateía Júnior
- **E-mail:** arimateiajunior.tic@gmail.com
- **WhatsApp:** +55 85 98776-4006