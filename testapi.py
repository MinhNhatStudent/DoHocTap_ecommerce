import requests
try:
    response = requests.get('http://localhost:5000/recommend_bp/similar/1')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {e}')
