#!/usr/bin/env python3
import requests
import json
import sys

def get_ip_info():
    try:
        response = requests.get('http://ip-api.com/json/', timeout=10)
        data = response.json()
        
        if data.get('status') == 'success':
            return {
                "success": "true",
                "ip": data.get('query', 'N/A'),
                "country": data.get('country', 'N/A'),
                "country_code": data.get('countryCode', 'N/A'),
                "region": data.get('regionName', 'N/A'),
                "city": data.get('city', 'N/A'),
                "zip": data.get('zip', 'N/A'),
                "latitude": data.get('lat', 'N/A'),
                "longitude": data.get('lon', 'N/A'),
                "timezone": data.get('timezone', 'N/A'),
                "isp": data.get('isp', 'N/A'),
                "organization": data.get('org', 'N/A'),
                "as": data.get('as', 'N/A')
            }
        else:
            return {"success": "false", "error": "API returned non-success status"}
            
    except requests.exceptions.RequestException as e:
        return {"success": "false", "error": str(e)}

def main():
    if len(sys.argv) < 2 or sys.argv[1] != 'info':
        print("Usage: python ip.py info")
        sys.exit(1)
    
    result = get_ip_info()
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
