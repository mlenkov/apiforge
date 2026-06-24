# Yandex API Configurations

Configuration files for Yandex APIs.

## Available Configurations

### metrika.json

Complete configuration for Yandex Metrika API.

#### API Management (`/management/v1/`)

| Resource | Method | Description |
|----------|--------|-------------|
| `counters` | GET | Список доступных счетчиков |
| `counter` | GET | Информация о счетчике |
| `counter_create` | POST | Создание счетчика |
| `counter_update` | PUT | Изменение счетчика |
| `counter_delete` | DELETE | Удаление счетчика |
| `counter_undelete` | POST | Восстановление счетчика |
| `goals` | GET | Список целей |
| `goal` | GET | Информация о цели |
| `goal_create` | POST | Создание цели |
| `goal_update` | PUT | Изменение цели |
| `goal_delete` | DELETE | Удаление цели |
| `filters` | GET | Список фильтров |
| `filter_create` | POST | Создание фильтра |
| `filter_delete` | DELETE | Удаление фильтра |
| `operations` | GET | Список операций |
| `grants` | GET | Список грантов |
| `grant_create` | POST | Создание гранта |
| `grant_delete` | DELETE | Удаление гранта |
| `segments` | GET | Список сегментов |
| `segment_create` | POST | Создание сегмента |
| `segment_delete` | DELETE | Удаление сегмента |
| `labels` | GET | Список меток |
| `label_create` | POST | Создание метки |
| `label_update` | PUT | Изменение метки |
| `label_delete` | DELETE | Удаление метки |
| `label_bind_counters` | POST | Привязка счетчиков к метке |
| `label_unbind_counters` | POST | Отвязка счетчиков от метки |
| `accounts` | GET | Список аккаунтов |
| `representatives` | GET | Список представителей |
| `representative_create` | POST | Создание представителя |
| `representative_delete` | DELETE | Удаление представителя |
| `direct_clients` | GET | Список клиентов Директа |
| `direct_clients_bind` | POST | Привязка клиентов Директа |
| `direct_clients_unbind` | DELETE | Отвязка клиентов Директа |
| `exports` | GET | Список экспортов |
| `export_create` | POST | Создание экспорта |
| `export_delete` | DELETE | Удаление экспорта |

#### API Statistics (`/stat/v1/`)

| Resource | Method | Description |
|----------|--------|-------------|
| `stat_data` | GET | Получение данных (таблица) |
| `stat_data_drilldown` | GET | Древовидный отчет |
| `stat_data_bytime` | GET | Данные по времени |
| `stat_data_comparison` | GET | Сравнение сегментов |

#### API Logs (`/management/v1/counter/{id}/logrequests`)

| Resource | Method | Description |
|----------|--------|-------------|
| `logrequests` | GET | Список запросов |
| `logrequest` | GET | Информация о запросе |
| `logrequest_create` | POST | Создание запроса |
| `logrequest_cancel` | POST | Отмена запроса |
| `logrequest_reset` | POST | Сброс запроса |
| `logrequest_clean` | POST | Очистка запроса |
| `logrequest_download` | GET | Скачивание данных |

#### Reference Data

| Resource | Method | Description |
|----------|--------|-------------|
| `messengers` | GET | Список мессенджеров |
| `social_networks` | GET | Список социальных сетей |
| `currencies` | GET | Список валют |
| `timezones` | GET | Список часовых поясов |

#### Goal Types

- `url` — Посещение страниц
- `action` — JavaScript-событие
- `step` — Составная цель
- `number` — Количество просмотров
- `visit_duration` — Продолжительность визита
- `file` — Скачивание файлов
- `phone` — Клик по номеру телефона
- `email` — Клик по email
- `messenger` — Переход в мессенджер
- `social` — Переход в социальную сеть
- `chat` — Клик по чату
- `payment_system` — Платежная система

---

### direct.json

Complete configuration for Yandex Direct API with 30+ services.

#### Reports
- **reports** — Получение статистики по аккаунту Директа

#### Campaigns
- **campaigns** — Управление кампаниями

#### Ad Groups
- **adgroups** — Управление группами объявлений

#### Ads
- **ads** — Управление объявлениями

#### Keywords
- **keywords** — Управление ключевыми фразами

#### Bids
- **bids** — Управление ставками
- **keywordbids** — Ставки по ключевым фразам
- **bidmodifiers** — Корректировки ставок

#### Negative Keywords
- **negativekeywordsharedsets** — Наборы минус-фраз

#### Media
- **adimages** — Изображения
- **creatives** — Креативы
- **advideos** — Видео

#### Turbo Pages
- **turbopages** — Турбо-страницы
- **leads** — Данные из форм

#### Extensions
- **sitelinks** — Быстрые ссылки
- **adextensions** — Расширения

#### Audience
- **audiencetargets** — Нацеливание на аудиторию
- **retargetinglists** — Ретаргетинг

#### Clients
- **clients** — Рекламодатели
- **agencyclients** — Клиенты агентства

#### Feeds
- **feeds** — Фиды

#### Dictionaries
- **dictionaries** — Справочники

#### Changes
- **changes** — Проверка изменений

#### Strategies
- **strategies** — Стратегии

#### Account
- **accountlogins** — Логины
- **balance** — Баланс
- **units** — Баллы
- **grants** — Гранты

---

## Setup

### 1. Get OAuth Token

1. Go to [Yandex OAuth](https://yandex.ru/dev/direct/doc/ru/concepts/access)
2. Create an application
3. Get your OAuth token

### 2. Set Environment Variables

```bash
# For Metrika
export YANDEX_METRIKA_TOKEN="your-oauth-token"

# For Direct
export YANDEX_DIRECT_TOKEN="your-oauth-token"
export YANDEX_DIRECT_CLIENT_LOGIN="your-login"  # Optional
```

### 3. Use the Configuration

```python
from apiforge import ApiForgeClient

# Metrika
client = ApiForgeClient(config_path="apiforge-configs/yandex/metrika.json")

# Direct
client = ApiForgeClient(config_path="apiforge-configs/yandex/direct.json")
```

## Examples

See [examples/](../../examples/) directory for complete usage examples.

## Documentation

- [Yandex Metrika API](https://yandex.ru/dev/metrika/)
- [Yandex Direct API](https://yandex.ru/dev/direct/doc/ru/concepts/overview)
