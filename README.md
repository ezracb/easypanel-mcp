# 🚀 EasyPanel MCP Server

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/MCP-Protocol-green?logo=anthregex&logoColor=white" alt="MCP Protocol">
  <img src="https://img.shields.io/badge/EasyPanel-Compatible-orange?logo=docker&logoColor=white" alt="EasyPanel Compatible">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <br>
  <img src="https://img.shields.io/badge/Windows%20%7C%20macOS%20%7C%20Linux-cross--platform-lightgrey" alt="Cross-platform">
  <img src="https://img.shields.io/badge/AI%20Agents-Claude%2FGPT%2Fn8n-purple?logo=openai&logoColor=white" alt="AI Agents">
</p>

<p align="center">
  <strong>🤖 Connect your AI Agent with EasyPanel and deploy infrastructure with natural prompts</strong>
</p>

<p align="center">
  <em>Transform how you manage your infrastructure: from command lines to natural conversations with AI</em>
</p>

---

## 📖 What is EasyPanel MCP?

**EasyPanel MCP** is a **Model Context Protocol (MCP)** server that allows AI agents (Claude, GPT, n8n, etc.) to interact directly with your **EasyPanel** dashboard to manage infrastructure, deploy services, and administer Docker containers using natural language.

### 🔑 Key Features

- ✅ **Full Natural Language Control**: "Deploy my Flask API with PostgreSQL"
- ✅ **Multi-Platform**: Works on Windows, macOS, and Linux
- ✅ **Easy Integration**: Compatible with Claude Desktop, Cursor, Cline, n8n, and any MCP client
- ✅ **Isolated Networks**: Support for secure internal Docker networks (auto-discovery)
- ✅ **Auto-Scaling**: Scale services based on demand with configurable thresholds
- ✅ **Assisted Debugging**: The AI can analyze logs, diagnose problems, and suggest solutions
- ✅ **GitHub Actions**: Trigger automatic deployments from your repository
- ✅ **Service Logs**: Intelligent log retrieval via service inspection
- ✅ **Network Discovery**: Automatic network topology discovery
- ✅ **Resource Monitoring**: Real-time CPU, memory, and disk monitoring

---

## ⚡ Quick Installation (Docker/Easypanel)

### 1. Fork & Deploy
You can fork this repository to your own account and connect it to **Easypanel**.

### 2. Environment Variables
Ensure you provide the following environment variables in your Easypanel App settings:
- `EASYPANEL_URL`: Your Easypanel instance URL (e.g., `https://dash.yourdomain.com`)
- `EASYPANEL_API_KEY`: Your API Key from Easypanel settings.

### 3. Run Command
The Docker container is configured to run in **HTTP mode** by default:
`python src/server.py http`

---

## 🛠️ Available Tools

| Category | Tools | Description |
|-----------|--------------|-------------|
| 📦 **Services** | `list_services`, `get_service`, `create_service`, `update_service`, `delete_service`, `restart_service`, `start_service`, `stop_service`, `deploy_service`, `get_service_logs` | Complete management + intelligent logs |
| 🚀 **Deployments** | `list_deployments`, `create_deployment`, `get_deployment`, `get_deployment_logs` | Control deployments and versions |
| 🌐 **Networks** | `list_networks` (auto-discovery), `create_network`, `delete_network` | Automatic topology discovery |
| 📁 **Projects** | `list_projects`, `create_project`, `delete_project`, `get_project` | Resource organization |
| 📊 **Monitoring** | `get_system_stats`, `get_service_stats`, `health_check`, `get_server_ip` | Real-time metrics |
| ⚡ **Scaling** | `scale_service`, `auto_scale_service` | Vertical and automatic scaling |
| 🔒 **Security** | `list_domains`, `create_domain`, `get_public_key` | Domains and Git authentication |

---

## 🔒 Security & Isolated Networks

### 🔐 Authentication
EasyPanel MCP supports **API Key** authentication (recommended).

### 🌐 Network Auto-Discovery
EasyPanel MCP includes **automatic network discovery** by analyzing service topology. 
- **Public Services**: Services with exposed ports are classified as PUBLIC.
- **Internal Services**: Services without public ports are classified as INTERNAL and isolated for security.

---

## 🤝 Contributing
Contributions are welcome! Please fork the repository and open a Pull Request.

---

## 👤 Author & Credits
**Danny Maaz**  
*Systems Engineer | Creator of EasyPanel MCP*  
🔗 [LinkedIn](https://linkedin.com/in/dannymaaz) • 💻 [GitHub](https://github.com/dannymaaz)

---

## 📜 License
MIT License. See [LICENSE](LICENSE) for details.
Forcing redeploy Tue Mar 24 12:22:37 WIB 2026
