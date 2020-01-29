from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def index(request):
    context = {}
    return render(request, 'dashboard_app/dashboard_base.html', context)

@csrf_exempt
def update_stock_prices(request):
    print("CALLED")
    if request.method == 'GET':
        # First obtain the data that will populate the graph
        ##############################################################
        # THIS BIT WILL USE THE StockRetriever class to get the data #
        ##############################################################

        # Then build the data object which will hold that data
        data = {
            'labels': ['January', 'February', 'TEST', 'April', 'May', 'June', 'July'],
            'datasets': [{"label": 'AWS',
                          'backgroundColor': 'rgb(255, 99, 132)',  # These should be stored in each CSP
                          'borderColor': 'rgb(255, 99, 132)',  # These should be stored in each CSP
                          'data': [73, -6, -99, 79, 93, -32, -99],
                          'fill': False,
                          },
                         {'label': 'AZURE',
                          'backgroundColor': 'rgb(54, 162, 235)',  # These should be stored in each CSP
                          'borderColor': 'rgb(54, 162, 235)',  # These should be stored in each CSP
                          'data': [-98, -26, 23, -95, 1, -72, -14],
                          'fill': False
                          }]
        }
        return JsonResponse(data)
    else:
        # We ignore any other type of request (eg. GET, PUT etc.)
        return JsonResponse({'error-message': 'No data could be retrieved from server'}, status=422)
