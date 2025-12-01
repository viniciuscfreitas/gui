# Gui Magellane | Portfolio

Portfolio profissional de direção criativa high-ticket.

## 🚀 Deploy Rápido

### Docker Compose (Recomendado)

```bash
# Build e iniciar
docker-compose up -d --build

# Ver logs
docker-compose logs -f web

# Parar
docker-compose down
```

### Docker Manual

```bash
# Build
docker build -t guimagellane .

# Run
docker run -d -p 80:80 --name guimagellane-web guimagellane
```

## 📋 Pré-requisitos

- Docker & Docker Compose
- Porta 80 disponível (ou ajustar no docker-compose.yml)

## 🔧 Configuração

### Variáveis de Ambiente
Nenhuma necessária para deploy básico.

### Portas
- **80**: HTTP (ajustar no docker-compose.yml se necessário)

## 📁 Estrutura

```
.
├── index.html      # HTML principal
├── app.js          # JavaScript
├── styles.css      # Estilos
├── manifest.json   # PWA manifest
├── robots.txt      # SEO
├── sitemap.xml     # SEO
├── Dockerfile      # Container
├── docker-compose.yml
└── nginx.conf      # Configuração Nginx
```

## 🔍 Healthcheck

```bash
curl http://localhost/health
```

## 📝 Notas

- Site estático servido via Nginx
- Gzip compression ativado
- Security headers configurados
- Cache otimizado para assets

## ⚠️ Antes de Produção

Ver `ANALISE_PRODUCAO.md` para checklist completo.

