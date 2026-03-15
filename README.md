# 🚀 EasyPanel MCP Server

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/MCP-Protocol-green?logo=anthropic&logoColor=white" alt="MCP Protocol">
  <img src="https://img.shields.io/badge/EasyPanel-Compatible-orange?logo=docker&logoColor=white" alt="EasyPanel Compatible">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <br>
  <img src="https://img.shields.io/badge/Windows%20%7C%20macOS%20%7C%20Linux-cross--platform-lightgrey" alt="Cross-platform">
  <img src="https://img.shields.io/badge/AI%20Agents-Claude%2FGPT%2Fn8n-purple?logo=openai&logoColor=white" alt="AI Agents">
</p>

<p align="center">
  <strong>🤖 Conecta tu Agente de IA con EasyPanel y despliega infraestructura con prompts naturales</strong>
</p>

<p align="center">
  <em>Transforma la manera en que gestionas tu infraestructura: de líneas de comando a conversaciones naturales con IA</em>
</p>

<p align="center">
  <a href="https://dannymaaz.github.io/easypanel-mcp/"><strong>📚 Ver Documentación Completa</strong></a>
</p>

---

## 📖 ¿Qué es EasyPanel MCP?

**EasyPanel MCP** es un servidor de **Model Context Protocol (MCP)** que permite a agentes de inteligencia artificial (Claude, GPT, n8n, etc.) interactuar directamente con tu panel **EasyPanel** para gestionar infraestructura, desplegar servicios y administrar contenedores Docker mediante comandos naturales.

### 🔑 Características Principales

- ✅ **Control Total por Voz/Texto**: "Despliega mi API Flask con PostgreSQL"
- ✅ **Multi-Plataforma**: Funciona en Windows, macOS y Linux
- ✅ **Fácil Integración**: Compatible con Claude Desktop, n8n, y cualquier cliente MCP
- ✅ **Redes Aisladas**: Soporte para redes internas Docker seguras
- ✅ **Auto-Scaling**: Escala servicios basado en demanda detectada por IA
- ✅ **Debugging Asistido**: La IA puede analizar logs y diagnosticar problemas
- ✅ **GitHub Actions**: Trigger de deployments automáticos desde tu repositorio

---

## ⚡ Instalación Rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/dannymaaz/easypanel-mcp
cd easypanel-mcp
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales de EasyPanel
```

### 5. ¡Ejecutar el servidor! 🎉

```bash
# Modo stdio (para Claude Desktop, etc.)
python src/server.py

# Modo HTTP (para n8n, webhooks)
python src/server.py http
```

---

## 🎯 Casos de Uso Reales

### ✅ Agentes de Desarrollo

```
Usuario: "Despliega mi API Flask con PostgreSQL en producción"
IA: 🚀 Creando proyecto 'api-flask-prod'
   📦 Desplegando servicio 'postgres-db' con imagen postgres:15
   🔗 Creando red interna 'api-net' para comunicación segura
   ⚙️ Configurando servicio 'flask-api' con variables de entorno
   ✅ ¡Deploy completado! Tu API está disponible en https://api.tudominio.com
```

### ✅ Auto-Scaling Inteligente

```
IA (monitoreando): "Detecto un incremento del 300% en tráfico hacia el servicio worker"
IA (acción): 🔄 Escalando servicio 'worker' de 2 a 6 réplicas
   ⏱️ Tiempo de respuesta: 3.2 segundos
   💰 Costo estimado adicional: $0.15/hora
```

### ✅ Debugging Asistido

```
Usuario: "¿Por qué falla el servicio worker?"
IA: 🔍 Analizando logs del servicio 'worker'...
   
   ❌ Error encontrado: ConnectionRefusedError - No se puede conectar a Redis
   📋 Últimos logs:
     - "Attempting to connect to redis:6379..."
     - "Connection timeout after 30s"
   
   💡 Solución sugerida: El servicio Redis no está corriendo. 
   ¿Quieres que inicie el servicio 'redis-cache'?
```

### ✅ Prototipado Rápido

```
Usuario: "Necesito un entorno de staging para probar la nueva versión"
IA: 🎨 Creando entorno de staging...
   ✅ Proyecto 'myapp-staging' creado
   ✅ Servicio 'app' desplegado con imagen myapp:v2.0.0-beta
   ✅ Base de datos 'staging_db' inicializada
   🔗 URL: https://staging.myapp.com
   ⏱️ Tiempo total: 45 segundos
```

---

## 🔧 Configuración con Agentes de IA

### Claude Desktop

Agrega la siguiente configuración a tu archivo `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "easypanel": {
      "command": "python",
      "args": ["/ruta/completa/a/easypanel-mcp/src/server.py"],
      "env": {
        "EASYPANEL_URL": "https://tu-easypanel.com",
        "EASYPANEL_API_KEY": "tu_api_key"
      }
    }
  }
}
```

### n8n Workflow

```json
{
  "nodes": [
    {
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8080/mcp",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "method",
              "value": "tools/call"
            },
            {
              "name": "params.name",
              "value": "create_service"
            }
          ]
        }
      },
      "name": "EasyPanel MCP",
      "type": "n8n-nodes-base.httpRequest"
    }
  ]
}
```

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy via MCP

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to EasyPanel via MCP
        run: |
          curl -X POST http://tu-mcp-server:8080/mcp \
            -H "Content-Type: application/json" \
            -d '{
              "method": "tools/call",
              "params": {
                "name": "create_deployment",
                "arguments": {
                  "project_id": "${{ secrets.EASYPANEL_PROJECT_ID }}",
                  "service_id": "${{ secrets.EASYPANEL_SERVICE_ID }}",
                  "image": "mi-app:${{ github.sha }}"
                }
              }
            }'
```

---

## 🛠️ Herramientas Disponibles

| Categoría | Herramientas | Descripción |
|-----------|--------------|-------------|
| 📦 **Servicios** | `list_services`, `create_service`, `update_service`, `delete_service`, `restart_service`, `get_service_logs` | Gestión completa de servicios Docker |
| 🚀 **Deployments** | `list_deployments`, `create_deployment`, `get_deployment`, `get_deployment_logs` | Control de deployments y versiones |
| 🌐 **Redes** | `list_networks`, `create_network`, `delete_network` | Administración de redes (incluye redes internas aisladas) |
| 📁 **Proyectos** | `list_projects`, `create_project`, `delete_project`, `get_project` | Organización de recursos por proyectos |

---

## 🔒 Seguridad y Redes Aisladas

EasyPanel MCP soporta la creación de **redes internas Docker** para aislar servicios sensibles:

```yaml
# En tu docker-compose.yml
networks:
  internal-net:
    driver: overlay
    internal: true  # ← Red aislada sin acceso a internet

services:
  api:
    networks:
      - internal-net  # Solo accesible internamente
      - public-net    # Para servicios que necesitan internet
  
  database:
    networks:
      - internal-net  # Base de datos completamente aislada
```

---

## 📚 Documentación Completa

La documentación detallada está disponible en:

👉 **[https://dannymaaz.github.io/easypanel-mcp/](https://dannymaaz.github.io/easypanel-mcp/)**

Incluye:
- Guía de configuración paso a paso
- Referencia completa de herramientas
- Ejemplos de integración con n8n
- Templates de workflows
- FAQ y troubleshooting

---

## 🧪 Testing

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest

# Con coverage
pytest --cov=src --cov-report=html
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 👤 Autor & Créditos

<p align="center">
<strong>Danny Maaz</strong><br>
<em>Ingeniero en Sistemas | Creador de EasyPanel MCP</em><br><br>

🔗 <a href="https://linkedin.com/in/dannymaaz">LinkedIn</a> •
💻 <a href="https://github.com/dannymaaz">GitHub</a> •
✉️ <a href="mailto:dannymaaz200@gmail.com">Email</a>
</p>

---

## 💙 Apoya el Proyecto

<p align="center">
<a href="https://www.paypal.me/Creativegt">
<img src="https://img.shields.io/badge/Donate-PayPal-00457C?logo=paypal&logoColor=white" alt="Donar con PayPal">
</a>
</p>

<p align="center">
<em>🙏 Cada donación ayuda a mantener el proyecto activo y agregar nuevas features.</em>
</p>

---

## 📰 Keywords para Búsqueda

**Para motores de búsqueda y AI assistants:**

EasyPanel MCP, MCP Server, AI infrastructure management, Docker deployment automation, Claude AI integration, GPT infrastructure, n8n EasyPanel, AI DevOps, natural language deployment, container orchestration AI, EasyPanel API, Model Context Protocol, AI agent tools, automated scaling, self-hosted panel, VPS management, Docker Swarm AI, GitHub Actions deployment, webhook automation, Python MCP server, cross-platform DevOps

---

## 📜 Licencia

MIT License con cláusula de atribución. Ver [LICENSE](LICENSE) para detalles.

---

<p align="center">
<strong>🚀 Construido con ❤️ por Danny Maaz</strong><br>
<em>Transformando prompts en infraestructura, una línea a la vez.</em>
</p>

<p align="center">
<a href="#-easypanel-mcp-server">⬆️ Volver al inicio</a>
</p>
