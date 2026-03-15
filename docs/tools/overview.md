---
title: Tools Overview - EasyPanel MCP
description: Complete reference of all EasyPanel MCP tools for managing services, deployments, networks, and projects.
keywords: EasyPanel tools, MCP tools reference, service management, deployment tools, network tools
---

# 🛠️ Tools Reference

Complete reference of all tools available in EasyPanel MCP.

---

## 📋 Tools by Category

EasyPanel MCP provides **17 tools** organized into 4 categories:

| Category | Tools | Description |
|----------|-------|-------------|
| 📦 **Services** | 7 tools | Manage Docker services |
| 🚀 **Deployments** | 4 tools | Control deployments |
| 🌐 **Networks** | 3 tools | Manage Docker networks |
| 📁 **Projects** | 4 tools | Organize resources |

---

## 🎯 Tool Usage Pattern

All tools follow a consistent pattern:

### Tool Definition Structure

```json
{
  "name": "tool_name",
  "description": "What the tool does",
  "inputSchema": {
    "type": "object",
    "properties": {
      "parameter_name": {
        "type": "string|integer|boolean|object",
        "description": "Parameter description"
      }
    },
    "required": ["required_parameter"]
  }
}
```

### Tool Call Format

```json
{
  "method": "tools/call",
  "params": {
    "name": "tool_name",
    "arguments": {
      "parameter_name": "value"
    }
  }
}
```

### Tool Response Format

```json
{
  "success": true,
  "data": { ... },
  "message": "Human-readable message"
}
```

---

## 📦 Services Tools

Manage Docker services in EasyPanel.

### `list_services`

List all services, optionally filtered by project.

**Parameters:**
- `project_id` (optional): Filter by project

**Example:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "list_services",
    "arguments": {
      "project_id": "proj_123"
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "svc_abc",
      "name": "api-service",
      "image": "nginx:latest",
      "status": "running"
    }
  ],
  "message": "Found 1 services"
}
```

---

### `get_service`

Get detailed information about a specific service.

**Parameters:**
- `service_id` (required): Service ID

**Example:**
```json
{
  "name": "get_service",
  "arguments": {
    "service_id": "svc_abc123"
  }
}
```

---

### `create_service`

Create a new service.

**Parameters:**
- `name` (required): Service name
- `project_id` (required): Project ID
- `image` (required): Docker image
- `config` (optional): Additional configuration

**Example:**
```json
{
  "name": "create_service",
  "arguments": {
    "name": "my-api",
    "project_id": "proj_123",
    "image": "node:18-alpine",
    "config": {
      "ports": ["3000:3000"],
      "env": {"NODE_ENV": "production"}
    }
  }
}
```

---

### `update_service`

Update service configuration.

**Parameters:**
- `service_id` (required): Service ID
- `config` (required): New configuration

**Example:**
```json
{
  "name": "update_service",
  "arguments": {
    "service_id": "svc_abc",
    "config": {
      "replicas": 3
    }
  }
}
```

---

### `delete_service`

Delete a service.

**Parameters:**
- `service_id` (required): Service ID

---

### `restart_service`

Restart a service.

**Parameters:**
- `service_id` (required): Service ID

---

### `get_service_logs`

Get service logs.

**Parameters:**
- `service_id` (required): Service ID
- `lines` (optional): Number of lines (default: 100)

---

## 🚀 Deployments Tools

Manage deployments and versions.

### `list_deployments`

List all deployments.

**Parameters:**
- `project_id` (optional): Filter by project

---

### `get_deployment`

Get deployment details.

**Parameters:**
- `deployment_id` (required): Deployment ID

---

### `create_deployment`

Create a new deployment.

**Parameters:**
- `project_id` (required): Project ID
- `service_id` (required): Service ID
- `image` (required): Docker image to deploy
- `config` (optional): Additional configuration

**Example:**
```json
{
  "name": "create_deployment",
  "arguments": {
    "project_id": "proj_123",
    "service_id": "svc_abc",
    "image": "myapp:v2.0.0",
    "config": {
      "strategy": "rolling"
    }
  }
}
```

---

### `get_deployment_logs`

Get deployment logs.

**Parameters:**
- `deployment_id` (required): Deployment ID

---

## 🌐 Networks Tools

Manage Docker networks including internal isolated networks.

### `list_networks`

List all networks.

**Parameters:** None

---

### `create_network`

Create a new network.

**Parameters:**
- `name` (required): Network name
- `internal` (optional): Isolated network (default: false)
- `driver` (optional): Network driver (default: "overlay")

**Example - Create Internal Network:**
```json
{
  "name": "create_network",
  "arguments": {
    "name": "database-net",
    "internal": true,
    "driver": "overlay"
  }
}
```

**Example - Create Public Network:**
```json
{
  "name": "create_network",
  "arguments": {
    "name": "public-net",
    "internal": false
  }
}
```

---

### `delete_network`

Delete a network.

**Parameters:**
- `network_id` (required): Network ID

---

## 📁 Projects Tools

Organize resources into projects.

### `list_projects`

List all projects.

**Parameters:** None

---

### `get_project`

Get project details.

**Parameters:**
- `project_id` (required): Project ID

---

### `create_project`

Create a new project.

**Parameters:**
- `name` (required): Project name
- `description` (optional): Project description

**Example:**
```json
{
  "name": "create_project",
  "arguments": {
    "name": "production-app",
    "description": "Production environment for main application"
  }
}
```

---

### `delete_project`

Delete a project.

**Parameters:**
- `project_id` (required): Project ID

---

## 🔧 Tool Execution Examples

### Example 1: Complete Deployment Flow

```json
// 1. Create project
{
  "name": "create_project",
  "arguments": {
    "name": "my-app",
    "description": "My application"
  }
}

// 2. Create internal network
{
  "name": "create_network",
  "arguments": {
    "name": "my-app-internal",
    "internal": true
  }
}

// 3. Create database service
{
  "name": "create_service",
  "arguments": {
    "name": "postgres-db",
    "project_id": "proj_123",
    "image": "postgres:15",
    "config": {
      "networks": ["my-app-internal"],
      "env": {
        "POSTGRES_PASSWORD": "secret"
      }
    }
  }
}

// 4. Create API service
{
  "name": "create_service",
  "arguments": {
    "name": "api-service",
    "project_id": "proj_123",
    "image": "myapp/api:latest",
    "config": {
      "ports": ["8080:8080"],
      "env": {
        "DATABASE_URL": "postgres://postgres:secret@postgres-db:5432/app"
      }
    }
  }
}
```

### Example 2: Service Management

```json
// List all services
{
  "name": "list_services"
}

// Get specific service
{
  "name": "get_service",
  "arguments": {
    "service_id": "svc_abc"
  }
}

// Get logs
{
  "name": "get_service_logs",
  "arguments": {
    "service_id": "svc_abc",
    "lines": 50
  }
}

// Restart service
{
  "name": "restart_service",
  "arguments": {
    "service_id": "svc_abc"
  }
}
```

---

## 📊 Response Codes

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error description"
}
```

---

## 🆘 Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Service not found` | Invalid service ID | Check service ID exists |
| `Project not found` | Invalid project ID | Verify project exists |
| `Connection refused` | EasyPanel unreachable | Check URL and network |
| `Unauthorized` | Invalid API key | Regenerate API key |
| `Timeout` | Request timeout | Increase `EASYPANEL_TIMEOUT` |

---

## 📚 Related Documentation

- **[Services Tools](services.md)** - Detailed service management
- **[Deployments Tools](deployments.md)** - Deployment management
- **[Networks Tools](networks.md)** - Network configuration
- **[Projects Tools](projects.md)** - Project organization

---

<p align="center" markdown>
**🛠️ Master all tools!** Choose a category to learn more.
</p>
