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
- ✅ **Fácil Integración**: Compatible con Claude Desktop, Cursor, Cline, n8n, y cualquier cliente MCP
- ✅ **Redes Aisladas**: Soporte para redes internas Docker seguras (auto-descubrimiento)
- ✅ **Auto-Scaling**: Escala servicios basado en demanda con umbrales configurables
- ✅ **Debugging Asistido**: La IA puede analizar logs, diagnosticar problemas y sugerir soluciones
- ✅ **GitHub Actions**: Trigger de deployments automáticos desde tu repositorio
- ✅ **Service Logs**: Obtención inteligente de logs vía inspección de servicio
- ✅ **Network Discovery**: Descubrimiento automático de topología de redes
- ✅ **Resource Monitoring**: Monitoreo en tiempo real de CPU, memoria y disco

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
IA (acción): 🔄 Escalando servicio 'worker' automáticamente
   📊 CPU usage: 95% → threshold 80% superado
   💾 Memory: 7.2GB / 8GB → threshold 90% superado
   📈 Escalando: CPU 2 → 4 cores, RAM 8GB → 16GB
   ⏱️ Tiempo de respuesta: 2.1 segundos
```

### ✅ Debugging Asistido

```
Usuario: "¿Por qué falla el servicio worker?"
IA: 🔍 Analizando logs del servicio 'worker'...

   📊 Service Status:
   - Status: error
   - State: crashed
   - Deployment: failed
   
   ❌ Error encontrado: ConnectionRefusedError - No se puede conectar a Redis
   📋 Últimos logs:
     - "Attempting to connect to redis:6379..."
     - "Connection timeout after 30s"
     - "Retry 1/3 failed"

   💡 Solución sugerida: El servicio Redis no está corriendo.
   Diagnóstico:
   - Redis service: stopped
   - Puerto 6379: no listening
   - Network: internal-net (OK)
   
   ¿Quieres que:
   1. Inicie el servicio 'redis-cache'?
   2. Reconfigure la conexión?
   3. Escale los recursos de Redis?
```

### ✅ Prototipado Rápido

```
Usuario: "Necesito un entorno de staging para probar la nueva versión"
IA: 🎨 Creando entorno de staging...
   ✅ Proyecto 'myapp-staging' creado
   ✅ Servicio 'app' desplegado con imagen myapp:v2.0.0-beta
   ✅ Base de datos 'staging_db' inicializada
   🔗 Red interna: staging-net (isolated)
   🔗 URL: https://staging.myapp.com
   ⏱️ Tiempo total: 45 segundos
```

### ✅ Monitoreo en Tiempo Real

```
Usuario: "¿Cómo está el rendimiento de mi servicio?"
IA: 📊 Analizando métricas en tiempo real...

   System Stats (últimos 5 min):
   - CPU: 45% average, 78% peak
   - Memory: 4.2GB / 8GB (52%)
   - Disk: 29.7GB / 309.9GB (9.6%)
   - Network: 1.2GB in, 3.4GB out
   
   Service Health:
   - api-service: ✅ healthy (99.9% uptime)
   - worker: ✅ healthy
   - postgres-db: ✅ healthy
   
   💡 Recomendación: Todo funcionando correctamente
   Próximas acciones sugeridas:
   - Programar backup en 2 horas
   - Actualizar certificado SSL en 15 días
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
| 📦 **Servicios** | `list_services`, `get_service`, `create_service`, `update_service`, `delete_service`, `restart_service`, `start_service`, `stop_service`, `deploy_service`, `get_service_logs` | Gestión completa + logs inteligentes |
| 🚀 **Deployments** | `list_deployments`, `create_deployment`, `get_deployment`, `get_deployment_logs` | Control de deployments y versiones |
| 🌐 **Redes** | `list_networks` (auto-discovery), `create_network`, `delete_network` | Descubrimiento automático de topología |
| 📁 **Proyectos** | `list_projects`, `create_project`, `delete_project`, `get_project` | Organización de recursos |
| 📊 **Monitoring** | `get_system_stats`, `get_service_stats`, `health_check`, `get_server_ip` | Métricas en tiempo real |
| ⚡ **Scaling** | `scale_service`, `auto_scale_service` | Escalado vertical y automático |
| 🔒 **Security** | `list_domains`, `create_domain`, `get_public_key` | Dominios y autenticación Git |

**Total: 25+ herramientas** disponibles para gestionar tu infraestructura con IA.

---

## 🔒 Seguridad y Redes Aisladas

### 🔐 Autenticación y Seguridad

EasyPanel MCP soporta **dos métodos de autenticación**:

1. **API Key (Recomendado)**: Más seguro, rotación fácil
2. **Email:Password**: Alternativa sin generar keys

### 🌐 Redes Aisladas (Auto-Discovery)

EasyPanel MCP ahora incluye **descubrimiento automático de redes** analizando la topología de servicios:

```python
# La IA puede descubrir redes automáticamente
networks = await client.list_networks()

# Resultado:
# - project-net (public): 3 servicios expuestos
# - project-net-internal (private): 2 servicios aislados
```

**Características:**
- ✅ **Detección automática**: Clasifica servicios como públicos o internos
- ✅ **Sin configuración manual**: EasyPanel gestiona redes automáticamente
- ✅ **Aislamiento seguro**: Servicios sin puertos públicos = aislados

### Ejemplo de Configuración

```yaml
# Servicio Público (accesible desde internet)
api-service:
  image: myapp/api:latest
  ports:
    - "8080:8080"  # Puerto público
  # → Clasificado como: PUBLIC

# Servicio Interno (aislado)
postgres-db:
  image: postgres:15
  ports: []  # Sin puertos públicos
  # → Clasificado como: INTERNAL
  # → Solo accesible por otros servicios en el mismo proyecto
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

## 🧪 Testing y Verificación

### Verificar Conexión

```bash
# Ejecutar script de test (solo lectura, sin cambios)
python test_connection.py

# Expected output:
# ✅ Connected successfully!
# ✅ Found 3 project(s)
# ✅ Found 0 service(s)
# ✅ System info retrieved
# ✅ ALL TESTS PASSED
```

### Tests Unitarios

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest

# Con coverage
pytest --cov=src --cov-report=html
```

### Verificar Configuración

```bash
# Test de configuración
python -c "from config import config; print('Config OK')"

# Test de conexión directa
python -c "
import asyncio
from src.client import EasyPanelClient
from config import config

async def test():
    client = EasyPanelClient(config.easypanel)
    await client.connect()
    print('EasyPanel healthy:', await client.health_check())
    await client.disconnect()

asyncio.run(test())
"
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
