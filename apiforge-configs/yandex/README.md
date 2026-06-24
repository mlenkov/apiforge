# Yandex Direct API Configuration

Configuration files for Yandex Direct API.

## Available Configurations

### direct.json

Complete configuration for Yandex Direct API with all available services:

## Services

### Reports
- **reports** - Получение статистики по аккаунту Директа

### Campaigns
- **campaigns** - Управление кампаниями (add, delete, get, update, archive, unarchive, resume, suspend)

### Ad Groups
- **adgroups** - Управление группами объявлений (add, delete, get, update)

### Ads
- **ads** - Управление объявлениями (add, delete, get, update, archive, unarchive, resume, suspend, moderate)

### Keywords
- **keywords** - Управление ключевыми фразами и автотаргетингами (add, delete, get, update, resume, suspend)

### Bids
- **bids** - Управление ставками (get, set, setAuto)
- **keywordbids** - Управление ставками по ключевым фразам (get, set, setAuto)
- **bidmodifiers** - Управление корректировками ставок (add, delete, get, set)

### Negative Keywords
- **negativekeywordsharedsets** - Управление наборами минус-фраз (add, delete, get, update)

### Keywords Research
- **keywordsresearch** - Предобработка ключевых фраз (deduplicate, hasSearchVolume)

### Businesses
- **businesses** - Получение профилей организаций (get)

### Media
- **adimages** - Операции с изображениями (add, delete, get)
- **creatives** - Получение креативов (add, get)
- **advideos** - Операции с видео (add, get)

### Turbo Pages
- **turbopages** - Получение параметров Турбо-страниц (get)
- **leads** - Получение данных из форм на Турбо-страницах (get)

### Extensions
- **sitelinks** - Операции с быстрыми ссылками (add, delete, get)
- **adextensions** - Операции с расширениями объявлений (add, delete, get)

### Audience
- **audiencetargets** - Управление условиями нацеливания на аудиторию (add, delete, get, resume, setBids, suspend)
- **retargetinglists** - Управление условиями ретаргетинга и подбора аудитории (add, delete, get, update)

### Clients
- **clients** - Управление параметрами рекламодателя (get, update)
- **agencyclients** - Управление клиентами агентства (add, get, update)

### Feeds
- **feeds** - Операции с фидами (add, delete, get, update)

### Dictionaries
- **dictionaries** - Получение справочных данных (get)

### Changes
- **changes** - Проверка наличия изменений (check, checkCampaigns, checkDictionaries)

### Strategies
- **strategies** - Операции с пакетными стратегиями (get, set)

### Account
- **accountlogins** - Получение списка логинов (get)
- **balance** - Получение информации о балансе (get)
- **units** - Получение информации об использовании баллов (get)
- **grants** - Получение списка грантов (get)

## Setup

### 1. Get OAuth Token

1. Go to [Yandex OAuth](https://yandex.ru/dev/direct/doc/ru/concepts/access)
2. Create an application
3. Get your OAuth token

### 2. Set Environment Variables

```bash
# Linux/macOS
export YANDEX_DIRECT_TOKEN="your-oauth-token"
export YANDEX_DIRECT_CLIENT_LOGIN="your-login"  # Optional

# Windows
set YANDEX_DIRECT_TOKEN=your-oauth-token
set YANDEX_DIRECT_CLIENT_LOGIN=your-login
```

### 3. Use the Configuration

```python
from apiforge import ApiForgeClient

client = ApiForgeClient(
    config_path="apiforge-configs/yandex/direct.json"
)

# Get campaigns
response = client.request("campaigns", data={
    "params": {
        "fieldNames": ["Id", "Name", "Status"]
    }
})

# Get report
response = client.request("reports", data={
    "params": {
        "SelectionCriteria": {},
        "FieldNames": ["Date", "Impressions", "Clicks"],
        "ReportName": "my_report",
        "ReportType": "ACCOUNT_PERFORMANCE_REPORT",
        "DateRangeType": "LAST_7_DAYS",
        "Format": "TSV",
        "IncludeVAT": "YES"
    }
})
```

## Sandbox

For testing, use the sandbox environment:

```python
from apiforge import ApiForgeClient

client = ApiForgeClient(
    config_path="apiforge-configs/yandex/direct.json"
)

# Override base URL for sandbox
client._base_url = "https://api-sandbox.direct.yandex.com/json/v5"
client._adapter.base_url = client._base_url
```

## Examples

See [examples/yandex_direct_reports.py](../../examples/yandex_direct_reports.py) for complete usage examples.

## Documentation

- [Yandex Direct API Documentation](https://yandex.ru/dev/direct/doc/ru/concepts/overview)
- [API Reference](https://yandex.ru/dev/direct/doc/ru/concepts/about)
- [Reports Service](https://yandex.ru/dev/direct/doc/ru/reports)
- [HTTP Headers](https://yandex.ru/dev/direct/doc/ru/headers)
- [Sandbox](https://yandex.ru/dev/direct/doc/ru/concepts/sandbox)
