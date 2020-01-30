from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from StockRetriever import get_N_last_stock_differences_for


def index(request):
    context = {}
    return render(request, 'dashboard_app/dashboard_base.html', context)


@csrf_exempt
def update_stock_prices(request):
    if request.method == 'GET':
        points = request.GET.get('points', None)
        interval = request.GET.get('interval', None)

        # Validate the queries to avoid errors
        if (points not in ['10', '20', '30']) or (interval not in ['1d', '1wk', '1mo']):
            # If 'None' or any other invalid value return an error
            return JsonResponse({'error-message': 'Invalid parameters requested from server'}, status=422)

        # First obtain the data that will populate the graph
        latest_stocks = get_N_last_stock_differences_for(['amzn', 'msft'], N=int(points), interval=interval)

        # Then build the data object which will hold that data
        data = {
            'labels': [{"d": date.day, "m": date.month, "y": date.year} for date in latest_stocks.get('dates')],
            'datasets': [{"label": 'AWS',
                          'backgroundColor': 'rgb(255, 99, 132)',  # These should be stored in each CSP
                          'borderColor': 'rgb(255, 99, 132)',  # These should be stored in each CSP
                          # 'data': [73, -6, -99, 79, 93, -32, -99],
                          'data': latest_stocks.get('amzn', []),
                          'fill': False,
                          },
                         {'label': 'AZURE',
                          'backgroundColor': 'rgb(54, 162, 235)',  # These should be stored in each CSP
                          'borderColor': 'rgb(54, 162, 235)',  # These should be stored in each CSP
                          # 'data': [-98, -26, 23, -95, 1, -72, -14],
                          'data': latest_stocks.get('msft', []),
                          'fill': False
                          }],
        }
        return JsonResponse(data)
    else:
        # We ignore any other type of request (eg. GET, PUT etc.)
        return JsonResponse({'error-message': 'No data could be retrieved from server'}, status=422)
