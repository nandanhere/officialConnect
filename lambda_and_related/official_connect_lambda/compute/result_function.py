
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import json



def safe_find(results_info, to_find):
    if results_info[to_find]:
        results_info[to_find] = results_info[to_find].find('p')
        if results_info[to_find]:
            if to_find == 'sem':
                results_info[to_find] = results_info[to_find].get_text(strip=True)[-1:]
            else:
                results_info[to_find] = results_info[to_find].get_text(strip=True)
        else:
            results_info['error'] = True
            return json.dumps(results_info)
    else:
        if to_find == 'cgpa':
            results_info[to_find] = '-'
        else:
            results_info['error'] = True
        return json.dumps(results_info)

def results(usn,even=False,suppli=False):
    results_info = {
        'error': False
    }
    url = 'http://exam.msrit.edu/' + ("eresultseven/" if even else "eresultssupply" if suppli else "")
    url += "?usn=" + usn + "&option=com_examresult&task=getResult"
    # values = {
    #     'usn': usn.upper(),
    #     'option': 'com_examresult',
    #     'task': 'getResult'
    # }
    # data = urllib.parse.urlencode(values)
    # data = data.encode('ascii')
    # print(data)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        results_html = res.read().decode('utf-8')
    # print(results_html)
    # print(results_html)
    soup = BeautifulSoup(results_html, 'html.parser')
    results_info['sem'] = soup.find('div', {'class': 'uk-card uk-card-body stu-data stu-data2'})
    safe_find(results_info, 'sem')
    results_info['credits_registered'] = soup.find('div', {'class': 'uk-card uk-card-default uk-card-body credits-sec1'})
    safe_find(results_info, 'credits_registered')
    results_info['credits_earned'] = soup.find('div', {'class': 'uk-card uk-card-default uk-card-body credits-sec2'})
    safe_find(results_info, 'credits_earned')
    results_info['sgpa'] = soup.find('div', {'class': 'uk-card uk-card-default uk-card-body credits-sec3'})
    safe_find(results_info, 'sgpa')
    results_info['cgpa'] = soup.find('div', {'class': 'uk-card uk-card-default uk-card-body credits-sec4'})
    safe_find(results_info, 'cgpa')

    all_subject_results_html = soup.find('table', {'class', 'uk-table uk-table-striped res-table'})
    if all_subject_results_html:
        all_subject_results_html = all_subject_results_html.find_all('tr')
        if all_subject_results_html:
            all_subject_results_html = all_subject_results_html[1:]
        else:
            results_info['error'] = True
            return json.dumps(results_info)
    else:
        results_info['error'] = True
        return json.dumps(results_info)
    all_subject_results = []
    for one_subject_results_html in all_subject_results_html:
        one_subject_results = []
        row = one_subject_results_html.find_all('td')
        for cell in row:
            one_subject_results.append(cell.get_text(strip=True))
        all_subject_results.append(one_subject_results)
    results_info['results'] = all_subject_results

    return {
        'statusCode':200,
        'body':json.dumps(results_info)
    }
    
def lambda_handler(event, context):
    even = event['queryStringParameters']['even'] == "yes"
    suppli = event['queryStringParameters']['suppli'] == "yes"
    usn  = event['queryStringParameters']['usn']
    return results(usn,even,suppli)