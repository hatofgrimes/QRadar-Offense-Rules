import json
import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_IP = os.getenv('QRADAR_IP')
QRADAR_TOKEN = os.getenv('QRADAR_TOKEN')

RULES_DIR = 'rules'

# QRadar Analytics Rules API endpoint-i
QRADAR_URL = f'https://{QRADAR_IP}/api/analytics/rules'

HEADERS = {
    'SEC': QRADAR_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Version': '12.0',
}


def deploy_rules():
  print(
      f'[+] GitHub Actions vasitəsilə QRadar ({QRADAR_IP}) qaydaları'
      ' yüklənir və aktivləşdirilir...'
  )

  if not os.path.exists(RULES_DIR):
    print(f'[XƏTA] \'{RULES_DIR}\' qovluğu tapılmadı!')
    return

  for filename in os.listdir(RULES_DIR):
    if filename.endswith('.json'):
      file_path = os.path.join(RULES_DIR, filename)

      try:
        with open(file_path, 'r', encoding='utf-8') as f:
          rule_json = json.load(f)
      except Exception as e:
        print(f'  [XƏTA] {filename} oxunmadı: {e}')
        continue

      # QAYDANI MƏCBURİ AKTİV EDİRİK VƏ OFFENSE YARATMASINI TƏMİN EDİRİK
      rule_json['enabled'] = True

      try:
        response = requests.post(
            QRADAR_URL, headers=HEADERS, json=rule_json, verify=False, timeout=20
        )

        if response.status_code in [200, 201]:
          print(
              f'  [UĞURLU] {filename} QRadar-a API ilə göndərildi və Offense'
              ' üçün aktivləşdirildi!'
          )
        else:
          print(
              f'  [STATUS] {filename} QRadar cavabı: {response.status_code} -'
              f' {response.text}'
          )

      except Exception as err:
        print(f'  [XƏTA] API sorğu xətası ({filename}): {err}')


if __name__ == '__main__':
  deploy_rules()
