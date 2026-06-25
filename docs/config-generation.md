# Config Generation Guide (AI)

Руководство для ИИ по автоматической генерации конфигураций ApiForge из документации API.

## Формат конфига

```json
{
  "base_url": "string (обязательно)",
  "auth": {
    "token": "string",
    "api_key": "string",
    "username": "string",
    "password": "string"
  },
  "default_headers": {
    "Header-Name": "value"
  },
  "resources": {
    "resource_name": {
      "path": "string (обязательно)",
      "method": "GET|POST|PUT|DELETE|PATCH (по умолчанию GET)",
      "description": "string",
      "parameters": {
        "param_name": {
          "type": "string|integer|number|boolean",
          "required": true|false,
          "description": "string",
          "default": "any"
        }
      },
      "headers": {
        "Header-Name": "value"
      }
    }
  }
}
```

## Алгоритм генерации

### 1. Определи base_url

```json
{
  "base_url": "https://api.example.com/v1"
}
```

Из документации API возьми базовый URL. Убери trailing slash.

### 2. Определи аутентификацию

Если API использует:
- **OAuth/Bearer token**: `"auth": {"token": "${TOKEN}"}`
- **API key**: `"auth": {"api_key": "${API_KEY}"}`
- **Basic auth**: `"auth": {"username": "${USER}", "password": "${PASS}"}`

Используй `${ENV_VAR}` для секретов.

### 3. Определи default_headers

```json
{
  "default_headers": {
    "Content-Type": "application/json",
    "Accept": "application/json"
  }
}
```

### 4. Создай ресурсы

Для каждого endpoint из документации:

**Input (документация API):**
```
GET /users
Получить список пользователей
Параметры:
  - limit (integer, optional) - Максимум элементов
  - offset (integer, optional) - Смещение
```

**Output (ресурс):**
```json
{
  "list_users": {
    "path": "/users",
    "method": "GET",
    "description": "Получить список пользователей",
    "parameters": {
      "limit": {
        "type": "integer",
        "required": false,
        "description": "Максимум элементов"
      },
      "offset": {
        "type": "integer",
        "required": false,
        "description": "Смещение"
      }
    }
  }
}
```

### 5. Именование ресурсов

Формат: `{действие}_{сущность}`

| Метод | Именование | Пример |
|-------|------------|--------|
| GET /items | `list_items` | `list_users`, `list_orders` |
| GET /items/{id} | `get_item` | `get_user`, `get_order` |
| POST /items | `create_item` | `create_user`, `create_order` |
| PUT /items/{id} | `update_item` | `update_user`, `update_order` |
| DELETE /items/{id} | `delete_item` | `delete_user`, `delete_order` |
| PATCH /items/{id} | `patch_item` | `patch_user`, `patch_order` |

### 6. Path параметры

```
/users/{user_id}/posts/{post_id}
```

```json
{
  "path": "/users/{user_id}/posts/{post_id}",
  "parameters": {
    "user_id": {"type": "integer", "required": true},
    "post_id": {"type": "integer", "required": true}
  }
}
```

### 7. Маппинг типов

| Тип API | Тип ApiForge |
|---------|--------------|
| string, text, email, url, uuid | `string` |
| integer, int, long, id | `integer` |
| number, float, double, decimal | `number` |
| boolean, bool, flag | `boolean` |

## Промпт для генерации

```
Создай конфиг ApiForge для API {название}.

Документация API: {ссылка или текст}

Базовый URL: {url}
Аутентификация: {тип}
```

## Пример: GitHub API

**Input:**
```
GitHub REST API
Base URL: https://api.github.com
Auth: Bearer token
Endpoints:
- GET /repos/{owner}/{repo} - Get a repository
- GET /repos/{owner}/{repo}/issues - List issues
- POST /repos/{owner}/{repo}/issues - Create issue
```

**Output:**
```json
{
  "base_url": "https://api.github.com",
  "auth": {
    "token": "${GITHUB_TOKEN}"
  },
  "default_headers": {
    "Accept": "application/vnd.github.v3+json"
  },
  "resources": {
    "get_repository": {
      "path": "/repos/{owner}/{repo}",
      "method": "GET",
      "description": "Get a repository",
      "parameters": {
        "owner": {
          "type": "string",
          "required": true,
          "description": "Repository owner"
        },
        "repo": {
          "type": "string",
          "required": true,
          "description": "Repository name"
        }
      }
    },
    "list_issues": {
      "path": "/repos/{owner}/{repo}/issues",
      "method": "GET",
      "description": "List issues",
      "parameters": {
        "owner": {
          "type": "string",
          "required": true
        },
        "repo": {
          "type": "string",
          "required": true
        },
        "state": {
          "type": "string",
          "required": false,
          "description": "Filter by state: open, closed, all"
        },
        "per_page": {
          "type": "integer",
          "required": false,
          "description": "Results per page",
          "default": 30
        }
      }
    },
    "create_issue": {
      "path": "/repos/{owner}/{repo}/issues",
      "method": "POST",
      "description": "Create an issue",
      "parameters": {
        "owner": {
          "type": "string",
          "required": true
        },
        "repo": {
          "type": "string",
          "required": true
        },
        "title": {
          "type": "string",
          "required": true,
          "description": "Issue title"
        },
        "body": {
          "type": "string",
          "required": false,
          "description": "Issue body"
        }
      }
    }
  }
}
```

## Валидация после генерации

```bash
# Сохрани конфиг в configs/my_api.json
# Проверь:
apiforge doctor --provider my_api
```

## Частые ошибки

1. **Нет `path`** — каждый ресурс обязан иметь `path`
2. **Невалидный method** — только GET, POST, PUT, DELETE, PATCH
3. **Невалидный base_url** — должен быть полным URI
4. **Дублирующие имена** — каждый ресурс должен иметь уникальное имя

## Шаблон для копирования

```json
{
  "base_url": "https://api.example.com",
  "auth": {
    "token": "${API_TOKEN}"
  },
  "default_headers": {
    "Content-Type": "application/json"
  },
  "resources": {
    "list_items": {
      "path": "/items",
      "method": "GET",
      "description": "List all items",
      "parameters": {
        "limit": {
          "type": "integer",
          "required": false,
          "description": "Max items",
          "default": 10
        }
      }
    },
    "get_item": {
      "path": "/items/{item_id}",
      "method": "GET",
      "description": "Get item by ID",
      "parameters": {
        "item_id": {
          "type": "string",
          "required": true,
          "description": "Item ID"
        }
      }
    },
    "create_item": {
      "path": "/items",
      "method": "POST",
      "description": "Create new item",
      "parameters": {
        "name": {
          "type": "string",
          "required": true,
          "description": "Item name"
        }
      }
    }
  }
}
```
