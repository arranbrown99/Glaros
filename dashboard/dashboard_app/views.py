from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.core.paginator import Paginator
from StockRetriever import get_N_last_stock_differences_for
from .models import MigrationEntry


def index(request):
    context = {}
    return render(request, 'dashboard_app/dashboard_base.html', context)


# Helper Method
def date_to_dict(date):
    """Takes a datetime.date and returns its dictionary equivalent in the format:
    {"d": day, "m": month, "y": year}
    """
    return {"d": date.day, "m": date.month, "y": date.year}


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
            'labels': [date_to_dict(date) for date in latest_stocks.get('dates')],
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


def update_migration_timeline(request):
    if request.method == 'GET':
        # First obtain the data that will populate the timeline
        last_migrations = MigrationEntry.objects.all().order_by("-_date")[:10][::-1]

        # Then build the data object which will hold that data
        data = {'migrations': []}
        for i in range(len(last_migrations)):
            entry = last_migrations[i]

            # Now we'll format the migration entries for the chart to accept them
            entry_date = date_to_dict(entry._date)

            # If we are on the last entry, the 'date_until' variable should be today's date.
            # Meaning that since the last migration, the app is still running on that CSP until this day.
            if i == len(last_migrations) - 1:
                date_until = date.today()
            else:
                date_until = last_migrations[i + 1]._date  # until the next migration (i.e. next entry).

            # Example: ['AWS', {'d': 30, 'm': 1, 'y': 2020}, {'d': 2, 'm': 2, 'y': 2020}]
            structured_entry = [
                entry._to,
                entry_date,
                date_to_dict(date_until)
            ]

            data.get('migrations', []).append(structured_entry)

        return JsonResponse(data)
    else:
        # We ignore any other type of request (eg. GET, PUT etc.)
        return JsonResponse({'error-message': 'No data could be retrieved from server'}, status=422)


def update_migration_table(request):
    if request.method == 'GET':
        # If page size isn't specified or not valid, default to 10
        try:
            page_size = int(request.GET['size'])
        except:
            page_size = 10

        migrations_list = MigrationEntry.objects.all().order_by("-_date")
        paginator = Paginator(migrations_list, page_size)
        page = request.GET.get('page')

        formatted_migrations = []
        for m in paginator.get_page(page):
            formatted_migrations.append(
                {
                    "id": m.id,
                    "date": m._date,
                    "from": m._from,
                    "to": m._to,
                }
            )

        data = {
            "last_page": (MigrationEntry.objects.all().count() // page_size) + 1,
            "data": formatted_migrations
        }
        return JsonResponse(data)
    else:
        # We ignore any other type of request (eg. GET, PUT etc.)
        return JsonResponse({'error-message': 'No data could be retrieved from server'}, status=422)
