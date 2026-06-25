# Config Creation Guide

Полное руководство по созданию конфигураций для ApiForge.

## Структура конфига

```json
{
  "base_url": "https://api.example.com",
  "auth": {
    "token": "${API_TOKEN}"
  },
  "default_headers": {
    "X-Custom-Header": "value"
  },
  "resources": {
    "resource_name": {
      "path": "/endpoint/{param}",
      "method": "GET",
      "description": "Что делает endpoint",
      "parameters": {
        "param": {
          "type": "string",
          "required": true,
          "description": "Описание параметра"
        }
      },
      "headers": {
        "X-Resource-Header": "value"
      }
    }
  }
}
```

## Поле по полю

### base_url (обязательно)

Базовый URL API. Все запросы будут относительно этого URL.

```json
{
  "base_url": "https://api.example.com"
}
```

**Требования:**
- Валидный URI
- Рекомендуется HTTPS
- Без слэша на конце

### auth (опционально)

Аутентификация. Поддерживаемые типы:

```json
{
  "auth": {
    "token": "OAuth bearer token",
    "api_key": "API ключ",
    "username": "Basic auth логин",
    "password": "Basic auth пароль"
  }
}
```

**Использование переменных окружения:**

```json
{
  "auth": {
    "token": "${YANDEX_OAUTH_TOKEN}"
  }
}
```

### default_headers (опционально)

Заголовки, добавляемые ко всем запросам:

```json
{
  "default_headers": {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer ${TOKEN}"
  }
}
```

### resources (обязательно)

Определения API endpoints. Ключ — имя ресурса, значение — конфигурация.

## Ресурс

### Обязательные поля

| Поле | Тип | Описание |
|------|-----|----------|
| `path` | string | Путь endpoint (поддерживает `{param}` плейсхолдеры) |

### Опциональные поля

| Поле | Тип | По умолчанию | Описание |
|------|-----|--------------|----------|
| `method` | string | `"GET"` | HTTP метод |
| `description` | string | — | Описание endpoint |
| `parameters` | object | `{}` | Определения параметров |
| `headers` | object | `{}` | Заголовки для этого endpoint |

### HTTP методы

Поддерживаются: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`

### Параметры

Определение параметра:

```json
{
  "param_name": {
    "type": "string",
    "required": true,
    "description": "Описание",
    "default": "значение"
  }
}
```

| Поле | Тип | Обязательно | Описание |
|------|-----|-------------|----------|
| `type` | string | Нет | Тип: `string`, `integer`, `number`, `boolean` |
| `required` | boolean | Нет | Обязательный параметр (по умолчанию `false`) |
| `description` | string | Нет | Описание параметра |
| `default` | any | Нет | Значение по умолчанию |

### Path параметры

Используйте `{param_name}` в пути:

```json
{
  "resources": {
    "get_user": {
      "path": "/users/{user_id}",
      "method": "GET",
      "parameters": {
        "user_id": {
          "type": "integer",
          "required": true
        }
      }
    }
  }
}
```

## Примеры

### Простой GET endpoint

```json
{
  "resources": {
    "list_users": {
      "path": "/users",
      "method": "GET",
      "description": "Список пользователей",
      "parameters": {
        "limit": {
          "type": "integer",
          "required": false,
          "description": "Максимум элементов",
          "default": 10
        }
      }
    }
  }
}
```

### POST с телом запроса

```json
{
  "resources": {
    "create_user": {
      "path": "/users",
      "method": "POST",
      "description": "Создать пользователя",
      "parameters": {
        "name": {
          "type": "string",
          "required": true,
          "description": "Имя пользователя"
        },
        "email": {
          "type": "string",
          "required": true,
          "description": "Email"
        }
      }
    }
  }
}
```

### Вложенные пути

```json
{
  "resources": {
    "get_user_posts": {
      "path": "/users/{user_id}/posts/{post_id}",
      "method": "GET",
      "parameters": {
        "user_id": {
          "type": "integer",
          "required": true
        },
        "post_id": {
          "type": "integer",
          "required": true
        }
      }
    }
  }
}
```

### Endpoint с кастомными заголовками

```json
{
  "resources": {
    "admin_endpoint": {
      "path": "/admin/users",
      "method": "GET",
      "headers": {
        "X-Admin-Token": "${ADMIN_TOKEN}"
      }
    }
  }
}
```

## Валидация

### Через CLI

```bash
# Проверить все конфиги
apiforge doctor

# Проверить конкретный провайдер
apiforge doctor --provider yandex

# Проверить конкретный API
apiforge doctor --provider yandex --api metrika
```

### Через Python

```python
from apiforge.config import load_config

try:
    config = load_config("my_config.json")
    print("Конфиг валиден")
except ApiForgeConfigError as e:
    print(f"Ошибка: {e}")
```

### Ошибки валидации

ApiForge проверяет:
- Наличие `base_url` и `resources`
- Валидность URI в `base_url`
- Корректность HTTP методов
- Наличие `path` у каждого ресурса
- Типы параметров

Пример ошибки:
```
Configuration validation failed:
[resources.users.method] 'INVALID' is not one of ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
  -> Use one of: DELETE, GET, PATCH, POST, PUT
```

## Установка конфигов

### Рекомендуемая структура

```
configs/
├── _template/
│   └── api_template.json    # JSON Schema
├── yandex/
│   ├── metrika.json
│   ├── direct.json
│   └── ...
└── my_api/
    └── main.json
```

### Куда класть конфиги

1. **В проекте:** `./configs/my_api.json`
2. **Глобально:** `~/.apiforge/configs/my_api/main.json`

```python
from apiforge import Client

# Локальный конфиг
client = Client(config_path="configs/my_api.json")

# Глобальный конфиг
from apiforge.config import get_config_path, load_config
path = get_config_path("my_api", "main")
config = load_config(path)
client = Client(config=config)
```
