
import json
import os
import errno

cookies = {
    'XSRF-TOKEN': 'b8f78a6e-5d8e-4e2e-b6e2-1c04e2f736bb',
    'JSESSIONID': '0C816AA5EBAB40459461893AD490E1EF',
    'dtCookie': 'v_4_srv_1_sn_D1858A36512EF655C19B19928E9275A1_perc_100000_ol_0_mul_1_app-3A37bc123ce5d9a8ed_0',
    '_ga': 'GA1.1.442847169.1698408790',
    '_ga_JGSX0KVE09': 'GS1.1.1698413973.2.1.1698413989.0.0.0',
    'AWSALB': 'jFhrGg6Y2seymrYHkSucC68feEuvfGI0MIzpqg8iB+TMLJuAfIaLkIMfFLzF4oKCQ0XX9bqaDh1XUUnBvTFhnNcmy9zq/VNwY3Xl714LO6gY8VwxgQ+9JxWVaPth',
    'AWSALBCORS': 'jFhrGg6Y2seymrYHkSucC68feEuvfGI0MIzpqg8iB+TMLJuAfIaLkIMfFLzF4oKCQ0XX9bqaDh1XUUnBvTFhnNcmy9zq/VNwY3Xl714LO6gY8VwxgQ+9JxWVaPth',
}

headers = {
    'authority': 'nevadaepro.com',
    'accept': 'application/xml, text/xml, */*; q=0.01',
    'accept-language': 'en-IN,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': 'XSRF-TOKEN=b8f78a6e-5d8e-4e2e-b6e2-1c04e2f736bb; JSESSIONID=0C816AA5EBAB40459461893AD490E1EF; dtCookie=v_4_srv_1_sn_D1858A36512EF655C19B19928E9275A1_perc_100000_ol_0_mul_1_app-3A37bc123ce5d9a8ed_0; _ga=GA1.1.442847169.1698408790; _ga_JGSX0KVE09=GS1.1.1698413973.2.1.1698413989.0.0.0; AWSALB=jFhrGg6Y2seymrYHkSucC68feEuvfGI0MIzpqg8iB+TMLJuAfIaLkIMfFLzF4oKCQ0XX9bqaDh1XUUnBvTFhnNcmy9zq/VNwY3Xl714LO6gY8VwxgQ+9JxWVaPth; AWSALBCORS=jFhrGg6Y2seymrYHkSucC68feEuvfGI0MIzpqg8iB+TMLJuAfIaLkIMfFLzF4oKCQ0XX9bqaDh1XUUnBvTFhnNcmy9zq/VNwY3Xl714LO6gY8VwxgQ+9JxWVaPth',
    'faces-request': 'partial/ajax',
    'origin': 'https://nevadaepro.com',
    'referer': 'https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data = {
    'javax.faces.partial.ajax': 'true',
    'javax.faces.source': 'bidSearchResultsForm:bidResultId',
    'javax.faces.partial.execute': 'bidSearchResultsForm:bidResultId',
    'javax.faces.partial.render': 'bidSearchResultsForm:bidResultId',
    'bidSearchResultsForm:bidResultId': 'bidSearchResultsForm:bidResultId',
    'bidSearchResultsForm:bidResultId_pagination': 'true',
    'bidSearchResultsForm:bidResultId_first': '25',
    'bidSearchResultsForm:bidResultId_rows': '25',
    'bidSearchResultsForm:bidResultId_encodeFeature': 'true',
    'bidSearchResultsForm': 'bidSearchResultsForm',
    '_csrf': 'b8f78a6e-5d8e-4e2e-b6e2-1c04e2f736bb',
    'openBids': 'true',
    'javax.faces.ViewState': '-2910554563181073180:7507559653843305143',
}



def write_json(data,filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)