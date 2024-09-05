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
```

Agora, você pode acessar a aplicação no navegador através do endereço [http://localhost:8080](http://localhost:8080).

Será necessário realizar o port-forward do serviço do Backend para permitir a conexão com o Frontend

```bash
kubectl port-forward service/backend-service 5000:5000 -n controle-agua-prod
```
Agora, você pode acessar o Backend no navegador através do endereço [http://localhost:5000](http://localhost:5000).

# Comandos Úteis para Docker, Kind e Kubectl

**Listar containers:**
   ```
   docker ps
   ```

Adicione -a para listar todos os containers, incluindo os que estão parados:
    ```
    docker ps -a
    ```

**Iniciar/parar/reiniciar containers:**
```
docker start <container_id>
docker stop <container_id>
docker restart <container_id>
```

**Remover containers:**
```
docker rm <container_id>
```

**Listar imagens:**
```
docker images
```

**Remover imagens:**
```
docker rmi <image_id>
```

**Fazer pull de uma imagem do Docker Hub:**
```
docker pull <image_name>:<tag>
```

**Construir uma imagem a partir de um Dockerfile:**
```
docker build -t <image_name>:<tag> .
```

**Executar um container em modo interativo:**
```
docker run -it <image_name> /bin/bash
```

### Comandos Úteis do Kind

**Criar um cluster:**
```
kind create cluster --name <cluster_name>
```

**Listar clusters:**
```
kind get clusters
```

**Excluir um cluster:**
```
kind delete cluster --name <cluster_name>
```

**Carregar uma imagem Docker no cluster:**
```
kind load docker-image <image_name>:<tag> --name <cluster_name>
```

**Conectar ao container do control-plane:**
```
docker exec -it <control_plane_container_id> /bin/bash
```

## Comandos Úteis do Kubectl

**Listar todos os pods em todos os namespaces:**
```
kubectl get pods --all-namespaces
```

**Listar todos os serviços:**
```
kubectl get services
```

**Listar todos os nodes:**
```
kubectl get nodes
```

**Obter detalhes de um pod específico:**
```
kubectl describe pod <pod_name>
```

**Aplicar uma configuração YAML (criar/atualizar recursos):**
```
kubectl apply -f <file.yaml>
```

**Deletar um recurso (pod, service, deployment, etc.):**
```
kubectl delete <resource_type> <resource_name>
```

**Executar um comando em um pod:**
```
kubectl exec -it <pod_name> -- <command>
```

**Ver logs de um pod:**
```
kubectl logs <pod_name>
```

**Para acompanhar os logs em tempo real, adicione -f:**
```
kubectl logs -f <pod_name>
```

**Fazer port-forward de um serviço para sua máquina local:**
```
kubectl port-forward svc/<service_name> <local_port>:<service_port>
```

**Verificar os recursos de um deployment:**
```
kubectl get deployment <deployment_name>
```

**Realizar rollout de um deployment (atualização controlada):**

***Ver o status do rollout:***
```
kubectl rollout status deployment/<deployment_name>
```

**Fazer rollback para a versão anterior:**
```
kubectl rollout undo deployment/<deployment_name>
```

**Escalar réplicas de um deployment:**

***Escalar para um número específico de réplicas:***
```
kubectl scale deployment/<deployment_name> --replicas=<number_of_replicas>
```

## Licença

Este projeto é licenciado sob os termos da licença MIT. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.