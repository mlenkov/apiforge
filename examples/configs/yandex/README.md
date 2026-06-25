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

### webmaster.json

Complete configuration for Yandex Webmaster API.

#### User
| Resource | Method | Description |
|----------|--------|-------------|
| `user` | GET | Получение идентификатора пользователя |

#### Sites (Hosts)
| Resource | Method | Description |
|----------|--------|-------------|
| `hosts` | GET | Список сайтов пользователя |
| `host_add` | POST | Добавление сайта |
| `host` | GET | Информация о сайте |
| `host_delete` | DELETE | Удаление сайта |
| `host_summary` | GET | Статистика сайта |
| `host_important_urls` | GET | Мониторинг важных страниц |
| `host_important_urls_history` | GET | История изменений важной страницы |

#### Verification
| Resource | Method | Description |
|----------|--------|-------------|
| `host_verification` | GET | Информация о подтверждении сайта |
| `host_verification_start` | POST | Запуск подтверждения прав |
| `host_owners` | GET | Список владельцев сайта |

#### Sitemaps
| Resource | Method | Description |
|----------|--------|-------------|
| `host_sitemaps` | GET | Список файлов Sitemap |
| `host_sitemap` | GET | Информация о Sitemap |
| `host_user_added_sitemaps` | GET | Список пользовательских Sitemap |
| `host_user_added_sitemap_add` | POST | Добавление Sitemap |
| `host_user_added_sitemap_info` | GET | Информация о пользовательском Sitemap |
| `host_user_added_sitemap_delete` | DELETE | Удаление Sitemap |

#### Search Queries
| Resource | Method | Description |
|----------|--------|-------------|
| `host_search_queries_popular` | GET | Популярные поисковые запросы |
| `host_search_queries_history_all` | GET | Статистика по всем запросам |
| `host_search_queries_history` | GET | Статистика по запросу |
| `host_query_analytics` | GET | Мониторинг запросов |

#### Recrawl
| Resource | Method | Description |
|----------|--------|-------------|
| `host_recrawl_queue` | GET | Список задач на переобход |
| `host_recrawl_add` | POST | Отправка на переобход |
| `host_recrawl_quota` | GET | Проверка квоты |
| `host_recrawl_task` | GET | Статус задачи |

#### Diagnostics & Indexing
| Resource | Method | Description |
|----------|--------|-------------|
| `host_diagnostics` | GET | Диагностика сайта |
| `host_indexing_history` | GET | История индексирования |
| `host_indexing_samples` | GET | Примеры загруженных страниц |
| `host_insearch_history` | GET | История страниц в поиске |
| `host_insearch_samples` | GET | Примеры страниц в поиске |
| `host_search_events_history` | GET | История появления/исключения страниц |
| `host_search_events_samples` | GET | Примеры появившихся/удаленных страниц |

#### Links
| Resource | Method | Description |
|----------|--------|-------------|
| `host_links_internal_samples` | GET | Неработающие внутренние ссылки |
| `host_links_internal_history` | GET | История внутренних ссылок |
| `host_links_external_samples` | GET | Внешние ссылки на сайт |
| `host_links_external_history` | GET | История внешних ссылок |

#### Feeds
| Resource | Method | Description |
|----------|--------|-------------|
| `host_feeds_list` | GET | Список загруженных фидов |
| `host_feed_add_start` | POST | Асинхронная загрузка фида |
| `host_feed_add_info` | GET | Статус загрузки фида |
| `host_feeds_batch_add` | POST | Загрузка нескольких фидов |
| `host_feeds_batch_remove` | POST | Удаление нескольких фидов |

---

### admetrica.json

Complete configuration for Yandex AdMetrica (Метрика для медийной рекламы) API.

#### Campaigns
| Resource | Method | Description |
|----------|--------|-------------|
| `campaigns` | GET | Список кампаний |
| `campaign` | GET | Информация о кампании |
| `campaign_create` | POST | Создание кампании |
| `campaign_update` | PUT | Изменение кампании |
| `campaign_delete` | DELETE | Удаление кампании |
| `campaign_copy` | POST | Копирование кампании |

#### Advertisers
| Resource | Method | Description |
|----------|--------|-------------|
| `advertisers` | GET | Список рекламодателей |
| `advertiser` | GET | Информация о рекламодателе |
| `advertiser_create` | POST | Создание рекламодателя |
| `advertiser_update` | PUT | Изменение рекламодателя |
| `advertiser_delete` | DELETE | Удаление рекламодателя |

#### Goals
| Resource | Method | Description |
|----------|--------|-------------|
| `goals` | GET | Список целей |
| `goal` | GET | Информация о цели |
| `goal_create` | POST | Создание цели |
| `goal_update` | PUT | Изменение цели |
| `goal_delete` | DELETE | Удаление цели |

#### Landing Pages
| Resource | Method | Description |
|----------|--------|-------------|
| `landing_pages` | GET | Список посадочных страниц |
| `landing_page` | GET | Информация о посадочной странице |
| `landing_page_create` | POST | Создание посадочной страницы |
| `landing_page_update` | PUT | Изменение посадочной страницы |
| `landing_page_delete` | DELETE | Удаление посадочной страницы |

#### Grants
| Resource | Method | Description |
|----------|--------|-------------|
| `grants` | GET | Список доступов |
| `grant_create` | POST | Создание доступа |
| `grant_delete` | DELETE | Удаление доступа |

#### Statistics
| Resource | Method | Description |
|----------|--------|-------------|
| `stat_data` | GET | Таблица данных |
| `stat_data_drilldown` | GET | Древовидный отчет |
| `stat_data_bytime` | GET | Данные по времени |
| `stat_summary` | GET | Сводка по кампаниям |
| `stat_comparison` | GET | Сравнение сегментов |

---

### audience.json

Complete configuration for Yandex Audience (Яндекс Аудитории) API.

#### Segments
| Resource | Method | Description |
|----------|--------|-------------|
| `segments` | GET | Список сегментов |
| `segment` | GET | Информация о сегменте |
| `segment_create` | POST | Создание сегмента |
| `segment_update` | PUT | Изменение сегмента |
| `segment_delete` | DELETE | Удаление сегмента |
| `segment_upload` | POST | Загрузка данных |
| `segment_upload_check` | GET | Проверка статуса загрузки |
| `segment_reach` | GET | Охват сегмента |
| `segment_logs` | GET | Логи загрузки |
| `segment_status` | GET | Статус сегмента |
| `segment_progress` | GET | Прогресс обработки |

#### Permissions
| Resource | Method | Description |
|----------|--------|-------------|
| `permissions` | GET | Список разрешений |
| `permission_create` | POST | Создание разрешения |
| `permission_delete` | DELETE | Удаление разрешения |

#### Accounts
| Resource | Method | Description |
|----------|--------|-------------|
| `accounts` | GET | Список аккаунтов |
| `representatives` | GET | Список представителей |
| `representative_create` | POST | Создание представителя |
| `representative_update` | PUT | Изменение представителя |
| `representative_delete` | DELETE | Удаление представителя |

#### Pixels
| Resource | Method | Description |
|----------|--------|-------------|
| `pixels` | GET | Список пикселей |
| `pixel` | GET | Информация о пикселе |
| `pixel_create` | POST | Создание пикселя |
| `pixel_update` | PUT | Изменение пикселя |
| `pixel_delete` | DELETE | Удаление пикселя |
| `pixel_create_segment` | POST | Создание сегмента |
| `pixel_segments` | GET | Список сегментов пикселя |

#### Metrika Segments
| Resource | Method | Description |
|----------|--------|-------------|
| `metrika_segments` | GET | Список сегментов Метрики |
| `metrika_segment` | GET | Информация о сегменте Метрики |

#### Geo Segments
| Resource | Method | Description |
|----------|--------|-------------|
| `geo_segments` | GET | Список гео-сегментов |
| `geo_segment` | GET | Информация о гео-сегменте |
| `geo_segment_create` | POST | Создание гео-сегмента |
| `geo_segment_update` | PUT | Изменение гео-сегмента |
| `geo_segment_delete` | DELETE | Удаление гео-сегмента |

#### Lookalike Segments
| Resource | Method | Description |
|----------|--------|-------------|
| `lookalike_segments` | GET | Список lookalike-сегментов |
| `lookalike_segment` | GET | Информация о lookalike-сегменте |
| `lookalike_segment_create` | POST | Создание lookalike-сегмента |
| `lookalike_segment_delete` | DELETE | Удаление lookalike-сегмента |

#### Combined Segments
| Resource | Method | Description |
|----------|--------|-------------|
| `combined_segments` | GET | Список комбинированных сегментов |
| `combined_segment` | GET | Информация о комбинированном сегменте |
| `combined_segment_create` | POST | Создание комбинированного сегмента |
| `combined_segment_update` | PUT | Изменение комбинированного сегмента |
| `combined_segment_delete` | DELETE | Удаление комбинированного сегмента |

#### CRM Segments
| Resource | Method | Description |
|----------|--------|-------------|
| `crm_segments` | GET | Список CRM-сегментов |
| `crm_segment` | GET | Информация о CRM-сегменте |
| `crm_segment_create` | POST | Создание CRM-сегмента |
| `crm_segment_update` | PUT | Изменение CRM-сегмента |
| `crm_segment_delete` | DELETE | Удаление CRM-сегмента |
| `crm_segment_upload` | POST | Загрузка данных в CRM-сегмент |
| `crm_segment_upload_check` | GET | Проверка статуса загрузки |

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

# For Webmaster
export YANDEX_WEBMASTER_TOKEN="your-oauth-token"

# For AdMetrica
export YANDEX_ADMETRICA_TOKEN="your-oauth-token"

# For Audience
export YANDEX_AUDIENCE_TOKEN="your-oauth-token"
```

### 3. Use the Configuration

```python
from apiforge import ApiForgeClient

# Metrika
client = ApiForgeClient(config_path="apiforge-configs/yandex/metrika.json")

# Direct
client = ApiForgeClient(config_path="apiforge-configs/yandex/direct.json")

# Webmaster
client = ApiForgeClient(config_path="apiforge-configs/yandex/webmaster.json")

# AdMetrica
client = ApiForgeClient(config_path="apiforge-configs/yandex/admetrica.json")

# Audience
client = ApiForgeClient(config_path="apiforge-configs/yandex/audience.json")
```

## Examples

See [examples/](../../examples/) directory for complete usage examples.

## Documentation

- [Yandex Metrika API](https://yandex.ru/dev/metrika/)
- [Yandex Direct API](https://yandex.ru/dev/direct/doc/ru/concepts/overview)
- [Yandex Webmaster API](https://yandex.ru/dev/webmaster/doc/ru/concepts/getting-started)
- [Yandex AdMetrica API](https://yandex.ru/dev/admetrica/doc/ru/)
- [Yandex Audience API](https://yandex.ru/dev/audience/ru/)
