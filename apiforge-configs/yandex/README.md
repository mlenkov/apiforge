# Yandex Direct API Configuration

Configuration files for Yandex Direct API.

## Available Configurations

### direct.json

Complete configuration for Yandex Direct API with all available resources:

- **Reports** - Get statistics and reports
- **Campaigns** - Manage advertising campaigns
- **Ad Groups** - Manage ad groups
- **Ads** - Manage advertisements
- **Keywords** - Manage keywords
- And many more...

## Setup

### 1. Get OAuth Token

1. Go to [Yandex OAuth](https://yandex.ru/dev/direct/doc/ru/concepts/access)
2. Create an application
3. Get your OAuth token

### 2. Set Environment Variables

```bash
# Linux/macOS
export YANDEX_DIRECT_TOKEN="your-oauth-token"
export YANDEX_DIRECT_CLIENT_LOGIN="your-login"  # Optional, if different from token owner

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

# Make a request
response = client.request("reports", data={...})
```

## Sandbox

For testing, use the sandbox environment:

```python
import os

# Use sandbox URL
client = ApiForgeClient(
    config_path="apiforge-configs/yandex/direct.json"
)

# Override base URL for sandbox
client._base_url = "https://api-sandbox.direct.yandex.com/json/v5"
client._adapter.base_url = client._base_url
```

## Resources

### Reports

Get statistics and reports from Yandex Direct.

**Endpoint:** `POST /reports`

**Required Parameters:**
- `SelectionCriteria` - Data selection criteria
- `FieldNames` - Fields to include in report
- `ReportName` - Unique report name
- `ReportType` - Type of report
- `DateRangeType` - Report period
- `Format` - Report format (TSV)
- `IncludeVAT` - Include VAT in amounts

**Report Types:**
- `ACCOUNT_PERFORMANCE_REPORT` - Account statistics
- `CAMPAIGN_PERFORMANCE_REPORT` - Campaign statistics
- `ADGROUP_PERFORMANCE_REPORT` - Ad group statistics
- `AD_PERFORMANCE_REPORT` - Ad statistics
- `CRITERIA_PERFORMANCE_REPORT` - Keyword statistics
- `CUSTOM_REPORT` - Custom report
- `REACH_AND_FREQUENCY_PERFORMANCE_REPORT` - Display campaign statistics
- `SEARCH_QUERY_PERFORMANCE_REPORT` - Search query statistics

**Date Range Types:**
- `TODAY` - Current day
- `YESTERDAY` - Yesterday
- `LAST_3_DAYS` - Last 3 days
- `LAST_7_DAYS` - Last 7 days
- `LAST_30_DAYS` - Last 30 days
- `CUSTOM_DATE` - Custom date range
- `ALL_TIME` - All available statistics

### Campaigns

Get list of advertising campaigns.

**Endpoint:** `GET /campaigns`

**Parameters:**
- `fieldNames` - Fields to include in response

### Ad Groups

Get list of ad groups.

**Endpoint:** `GET /adgroups`

**Parameters:**
- `fieldNames` - Fields to include in response

### Ads

Get list of advertisements.

**Endpoint:** `GET /ads`

**Parameters:**
- `fieldNames` - Fields to include in response

### Keywords

Get list of keywords.

**Endpoint:** `GET /keywords`

**Parameters:**
- `fieldNames` - Fields to include in response

## Examples

See [examples/yandex_direct_reports.py](../../examples/yandex_direct_reports.py) for complete usage examples.

## Documentation

- [Yandex Direct API Documentation](https://yandex.ru/dev/direct/doc/ru/reports)
- [Reports Service](https://yandex.ru/dev/direct/doc/ru/reports)
- [HTTP Headers](https://yandex.ru/dev/direct/doc/ru/headers)
- [Report Specification](https://yandex.ru/dev/direct/doc/ru/spec)
- [Sandbox](https://yandex.ru/dev/direct/doc/ru/concepts/sandbox)
