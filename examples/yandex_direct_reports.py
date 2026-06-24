"""
Example: Yandex Direct Reports API

This example demonstrates how to use ApiForge to get statistics
from Yandex Direct Reports service.

Prerequisites:
1. Install apiforge: pip install apiforge
2. Get OAuth token from Yandex: https://yandex.ru/dev/direct/doc/ru/concepts/access
3. Set environment variables:
   - YANDEX_DIRECT_TOKEN: Your OAuth token
   - YANDEX_DIRECT_CLIENT_LOGIN: Your Yandex Direct login (if different from token owner)
"""

import os
from datetime import datetime, timedelta
from apiforge import ApiForgeClient


def main():
    # Ensure environment variables are set
    token = os.environ.get("YANDEX_DIRECT_TOKEN")
    client_login = os.environ.get("YANDEX_DIRECT_CLIENT_LOGIN")
    
    if not token:
        print("Error: YANDEX_DIRECT_TOKEN environment variable not set")
        print("Please set it to your OAuth token")
        return
    
    # Create client from config
    config_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "apiforge-configs",
        "yandex",
        "direct.json"
    )
    
    client = ApiForgeClient(config_path=config_path)
    
    # Override client login if provided
    if client_login:
        client._default_headers["Client-Login"] = client_login
    
    # Example 1: Get account performance report for last 7 days
    print("\n=== Account Performance Report (Last 7 Days) ===")
    
    try:
        response = client.request(
            "reports",
            data={
                "params": {
                    "SelectionCriteria": {},
                    "FieldNames": [
                        "Date",
                        "CampaignName",
                        "Impressions",
                        "Clicks",
                        "Cost",
                        "Ctr",
                        "AvgCpc",
                        "AvgPageviews"
                    ],
                    "ReportName": f"account_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "ReportType": "ACCOUNT_PERFORMANCE_REPORT",
                    "DateRangeType": "LAST_7_DAYS",
                    "Format": "TSV",
                    "IncludeVAT": "YES"
                }
            }
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response:\n{response.text()}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Get campaign performance report for custom date range
    print("\n=== Campaign Performance Report (Custom Date Range) ===")
    
    date_from = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    date_to = datetime.now().strftime("%Y-%m-%d")
    
    try:
        response = client.request(
            "reports",
            data={
                "params": {
                    "SelectionCriteria": {
                        "DateFrom": date_from,
                        "DateTo": date_to
                    },
                    "FieldNames": [
                        "Date",
                        "CampaignId",
                        "CampaignName",
                        "CampaignType",
                        "Impressions",
                        "Clicks",
                        "Cost",
                        "Ctr",
                        "AvgCpc",
                        "Conversions",
                        "CostPerConversion",
                        "ConversionRate"
                    ],
                    "ReportName": f"campaign_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "ReportType": "CAMPAIGN_PERFORMANCE_REPORT",
                    "DateRangeType": "CUSTOM_DATE",
                    "Format": "TSV",
                    "IncludeVAT": "YES"
                }
            }
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response:\n{response.text()}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Get ad group performance report with filtering
    print("\n=== Ad Group Performance Report (With Filter) ===")
    
    try:
        response = client.request(
            "reports",
            data={
                "params": {
                    "SelectionCriteria": {
                        "DateRangeType": "LAST_30_DAYS",
                        "Filter": [
                            {
                                "Field": "Impressions",
                                "Operator": "GREATER_THAN",
                                "Values": ["100"]
                            }
                        ]
                    },
                    "FieldNames": [
                        "Date",
                        "CampaignName",
                        "AdGroupId",
                        "AdGroupName",
                        "Impressions",
                        "Clicks",
                        "Cost",
                        "Ctr",
                        "AvgCpc"
                    ],
                    "ReportName": f"adgroup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "ReportType": "ADGROUP_PERFORMANCE_REPORT",
                    "DateRangeType": "LAST_30_DAYS",
                    "Format": "TSV",
                    "IncludeVAT": "YES"
                }
            }
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response:\n{response.text()}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 4: Get search query performance report
    print("\n=== Search Query Performance Report ===")
    
    try:
        response = client.request(
            "reports",
            data={
                "params": {
                    "SelectionCriteria": {},
                    "FieldNames": [
                        "Date",
                        "CampaignName",
                        "AdGroupId",
                        "AdGroupName",
                        "Query",
                        "Impressions",
                        "Clicks",
                        "Cost",
                        "Ctr",
                        "AvgCpc",
                        "Conversions",
                        "CostPerConversion"
                    ],
                    "ReportName": f"search_query_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "ReportType": "SEARCH_QUERY_PERFORMANCE_REPORT",
                    "DateRangeType": "LAST_30_DAYS",
                    "Format": "TSV",
                    "IncludeVAT": "YES"
                }
            }
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response:\n{response.text()}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 5: Get list of campaigns
    print("\n=== List of Campaigns ===")
    
    try:
        response = client.request(
            "campaigns",
            params={
                "fieldNames": ["Id", "Name", "Status", "Type", "DailyBudget"]
            }
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response:\n{response.json()}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Close the client
    client.close()
    print("\nDone!")


if __name__ == "__main__":
    main()
