import datetime
import time
import requests
import json
from .. import helpers
from src.objects.graph_objects.nodes import node_factory
from src.scripts.generate_node_id import generate_node_id

requests_counter = 0
search_items_per_page = 10


def requests_check():
    global requests_counter

    # print(.format(requests_counter), end='\r')
    if requests_counter > 599:
        print('rate limit hit. Wait 5 mins')
        countdown(h=0, m=5, s=0)
        requests_count = 0
    else:
        requests_counter += 1


def make_search_params(query, page_number):
    return {'q': query,
            'items_per_page': search_items_per_page,
            'start_index': ((page_number - 1) * search_items_per_page)
            }


def search(url, params):
    config = helpers.get_config()

    response = requests.get(url=url, headers=config.header, params=params)

    print(url)

    if response.status_code == 401:
        q = params['q']
        print(f'bad search request: {q}')
        return None

    result = json.loads(response.text)

    items = []

    for item in result['items']:
        if item['kind'] == 'searchresults#company':
            item['node_type'] = node_factory.ch_company_str
            item['node_id'] = generate_node_id(item['company_number'],node_factory.ch_company_str)
            item['init_token'] = item['company_number']

        elif item['kind'] == 'searchresults#officer':
            item['node_type'] = node_factory.ch_officer_str
            item['node_id'] = generate_node_id(item['links']['self'].split('/')[2], node_factory.ch_officer_str)
            item['init_token'] = item['links']['self'].split('/')[2]
        else:
            item['kind'] = 'ERROR TYPE NOT ACCOUNTED FOR'
            item['node_id'] = 'ERROR TYPE NOT ACCOUNTED FOR'
            item['name'] = 'ERROR TYPE NOT ACCOUNTED FOR'
            continue

        item['name'] = item['title']

        description = item['description']
        address = item['address_snippet']

        item['display_description'] = f"""{description}
                                          {address}"""

        items.append(item)

    return items


def companies_house_search(query, page_number, search_type=None):
    if search_type is None:
        return search_all(query, page_number)
    elif search_type == node_factory.ch_company_str:
        return search_companies(query, page_number)
    elif search_type == node_factory.ch_officer_str:
        return search_officers(query, page_number)
    else:
        print(f'SYSTEM ERROR incorrect type for Companies House Search {search_type}')
        return []

def search_all(query, page_number):
    url = 'https://api.company-information.service.gov.uk/search'
    params = make_search_params(query, page_number)
    return search(url, params)


def search_companies(query, page_number):
    url = 'https://api.company-information.service.gov.uk/search/companies'
    params = make_search_params(query, page_number)
    return search(url, params)


def search_officers(query, page_number):
    url = 'https://api.company-information.service.gov.uk/search/officers'
    params = make_search_params(query, page_number)
    return search(url, params)


def get_officer(officer_id):
    url = 'https://api.company-information.service.gov.uk/officers/{officer_id}/appointments'.format(
        officer_id=officer_id)

    return get_with_paging(url=url)


# Create class that acts as a countdown
def countdown(h, m, s):
    # Calculate the total number of seconds
    total_seconds = h * 3600 + m * 60 + s

    # While loop that checks if total_seconds reaches zero
    # If not zero, decrement total time by one second
    while total_seconds > 0:
        # Timer represents time left on countdown
        timer = datetime.timedelta(seconds=total_seconds)

        # Prints the time left on the timerit
        print(timer, end="\r")

        # Delays the program one second
        time.sleep(1)

        # Reduces total time by one second
        total_seconds -= 1

    print("Bzzzt! The countdown is at zero seconds!")


def get_company_officer_ids(company_number):
    config = helpers.get_config()
    url = config.companies_house_api_base_url + '/company/{company_number}/officers'.format(
        company_number=company_number)
    print(url)
    result = get_with_paging(url=url)
    if result is None:
        return None

    ids = []

    for item in result['items']:
        officer_id = item['links']['officer']['appointments'].split('/')[2]
        if officer_id in ids:
            continue
        ids.append(officer_id)

    return ids


def get_company(company_number):
    config = helpers.get_config()

    url = config.companies_house_api_base_url + '/company/{companyNumber}'.format(companyNumber=company_number)
    # print(url)
    response = requests.get(url=url, headers=config.header)
    # print(response.status_code)
    if response.status_code != 200:
        print('Bad response from Companies House API')
        print(response.status_code)
        print(response.text)
        return None

    result = json.loads(response.text)
    return result


def get_with_paging(url):
    print('getting with Paging')
    config = helpers.get_config()
    items_per_page = 35
    start_index = 0
    page = 0
    total_pages = 1

    go = True

    final_result = None
    items = []

    while go:
        page += 1
        requests_check()
        print('{0} Companies House requests. On page {1} of {2}'.format(requests_counter, page, total_pages), end='\r')

        # print('items_per_page: {items_per_page}, start_index: {start_index}'.format(items_per_page=items_per_page,
        #                                                                             start_index=start_index))
        params = {'items_per_page': items_per_page, 'start_index': start_index}

        response = requests.get(url=url, headers=config.header, params=params)

        # print(response.status_code)
        if response.status_code != 200:
            print('Bad response pulling from Companies House API')
            print(response.text)
            return None

        result = json.loads(response.text)

        total_pages = int(result['total_results'] / items_per_page)

        if config.appointments_limit != -1 and result['total_results'] >= config.appointments_limit:

            if result['kind'] == 'officer-list':
                print('LIMIT BREACHED company {cn} has {num} officers'.format(cn=result['links']['self'].split('/')[1],
                                                                              num=result['total_results']))
            else:
                print("APPOINTMENT LIMIT BREACHED officer {officer} has {num} appointments"
                      .format(officer=result['name'], num=result['total_results']))
            final_result = result
            final_result['items'] = items
            break

        items += result['items']
        if (start_index + items_per_page) >= result['total_results']:
            go = False
            final_result = result
            final_result['items'] = items

        start_index += items_per_page

    return final_result


def extract_id_from_link(link):
    return link.split('/')[2]
