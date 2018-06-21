import requests

base_url = 'https://nba.hupu.com/match/nba?offset=-'
page = 0


def parser(url):
    response = requests.get(url)
    result = response.json()
    print(result['data']['date'])
    for item in result['data']['list']:
        print(item['home_name'], item['home_score'], ':', item['away_score'], item['away_name'])


if __name__ == '__main__':
    while page < 3:
        parser(base_url + str(page))
        page += 1
