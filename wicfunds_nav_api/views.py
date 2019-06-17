import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    return HttpResponse('The Arbitrage Funds, Daily NAV Updates (API v1.0)')

@csrf_exempt
def get_taq_performance(request):
    performance_url = "https://arbitragefunds.s3.amazonaws.com/performance/TAQ_Performance.CSV"
    json_response = get_performances_general(performance_url)
    return JsonResponse([json_response], safe=False)

@csrf_exempt
def get_arb_performance(request):
    arb_performance_url = "https://arbitragefunds.s3.amazonaws.com/performance/ARB_Performance.CSV"
    json_response = get_performances_general(arb_performance_url)
    return JsonResponse([json_response], safe=False)

@csrf_exempt
def get_aed_performance(request):
    performance_url = "https://arbitragefunds.s3.amazonaws.com/performance/AED_Performance.CSV"
    json_response = get_performances_general(performance_url)
    return JsonResponse([json_response], safe=False)

@csrf_exempt
def get_taco_performance(request):
    performance_url = "https://arbitragefunds.s3.amazonaws.com/performance/TACO_Performance.CSV"
    json_response = get_performances_general(performance_url)
    return JsonResponse([json_response], safe=False)

@csrf_exempt
def get_performances_general(url):
    daily_performance = pd.read_csv(url, header=1)
    info_to_display = daily_performance.stack().groupby(level=0).apply(lambda x: x.unique().tolist())[4]
    as_of_info = info_to_display[1].split(' ')
    info_to_display[0] += ' ' + ' '.join(as_of_info[2:])

    information_array = {}
    for info in info_to_display:
        if 'quarter' in info.lower():
            key = ' '.join(info.split(' ')[0:4])
            information_array[key] = ' '.join(info.split(' ')[4:])
        else:
            key = ' '.join(info.split(' ')[0:2])
            information_array[key] = ' '.join(info.split(' ')[2:])

    json_response = {}
    if '3 YR' in daily_performance.columns.values:
        json_response['label_one'] = '3 YR'
        json_response['label_two'] = '5 YR'
    else:
        json_response['label_one'] = '5 YR'
        json_response['label_two'] = '10 YR'
    
    # Change column names
    daily_performance.columns = ['ticker', 'class', 'min_investment', 'gross_expense_ratio', 'net_expense_ratio',
                                 'tickerx', 'daily_nav', 'daily_change_dollar', 'daily_change_percentage',
                                 'ytd_return', 'tickery', 'month_end_1yr', 'month_end_5yr', 'month_end_10yr',
                                 'month_end_since_inception', 'tickerz', 'quarter_end_1yr', 'quarter_end_5yr',
                                 'quarter_end_10yr', 'quarter_end_since_inception', 'tickerzzz', 'quarter_pop_1yr',
                                 'quarter_pop_5yr', 'quarter_pop_10yr', 'quarter_pop_since_inception']
    del daily_performance['tickerx']
    del daily_performance['tickery']
    del daily_performance['tickerz']
    del daily_performance['tickerzzz']

    daily_performance = daily_performance.iloc[0:4]
    
    classes = daily_performance['class'].unique()

    for share_class in classes:
        json_response[share_class] = daily_performance[daily_performance['class'] == share_class].\
            drop(columns=['class']).to_json(orient='records')

    json_response['AS_OF_INFO'] = [information_array]

    return json_response
