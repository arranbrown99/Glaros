import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date
from django.core.paginator import Paginator
from .models import MigrationEntry

# Glaros non-Django imports
from StockRetriever import get_N_last_stock_differences_for
from cloud_service_providers.AbstractCSP import AbstractCSP
from cloud_service_providers.AwsCSP import AwsCSP
from cloud_service_providers.AzureCSP import AzureCSP
from cloud_service_providers.GoogleCSP import GoogleCSP

# file that stores the general information of the app provided by the Driver
from dashboard.settings import GENERAL_INFO_FILE


def index(request):
    context = {}

    # Get data to populate the General Information area:
    with open(GENERAL_INFO_FILE, "r") as jsonFile:
        data = json.load(jsonFile)

    # Get Location
    currently_on = data.get("GLAROS_CURRENTLY_ON")

    # Get IP
    current_ip = data.get("GLAROS_CURRENT_IP")

    # Get Status
    current_status = data.get("GLAROS_CURRENT_STATUS")

    # Get Colour
    currently_on_colour = data.get(
        "GLAROS_CURRENTLY_ON_COLOUR", 'rgb(255,0,0)')

    # Get Dates
    date_format = "%d/%m/%Y"
    try:
        last_migration = MigrationEntry.objects.last()._date.strftime(date_format)
    except AttributeError:
        last_migration = "No migration history"

    current_date = date.today().strftime(date_format)

    # Add to context
    csp_stock_list = AbstractCSP.get_stock_names()
    csp_list = []
    for name in csp_stock_list:
        csp_list.append(AbstractCSP.get_csp(name).get_formal_name())
    context['currently_on'] = currently_on if currently_on in csp_list else "..."
    context['current_status'] = current_status if current_status in [
        "Running", "Migrating"] else "..."
    context['last_migration'] = last_migration
    context['current_date'] = current_date
    context['current_ip'] = current_ip
    context['currently_on_colour'] = currently_on_colour
    return render(request, 'dashboard_app/dashboard_base.html', context)


# Helper Method
def datetime_to_dict(dt):
    """Takes a datetime.datetime and returns its dictionary equivalent in the format:
    {"y": year, "m": month, "d": day, "h": hours, "m": minutes, "s": seconds}
    """
    return {"y": dt.year, "m": dt.month, "d": dt.day, "h": dt.hour, "min": dt.minute, "s": dt.second}


def update_stock_prices(request):
    if request.method == 'GET':
        points = request.GET.get('points', None)
        interval = request.GET.get('interval', None)

        # Validate the queries to avoid errors
        if (points not in ['10', '20', '30']) or (interval not in ['1d', '1wk', '1mo']):
            # If 'None' or any other invalid value return an error
            return JsonResponse({'error-message': 'Invalid parameters requested from server'}, status=422)

        # Obtain the stock names of all available CSPs
        all_stock_names = AbstractCSP.get_stock_names()

        print(len(all_stock_names))
        for stock in all_stock_names:
            print(">>>>>>>>", stock)

        # First obtain the data that will populate the graph
        latest_stocks = get_N_last_stock_differences_for(
            all_stock_names, N=int(points), interval=interval)

        # Then build the data object which will hold that data
        data = {
            'labels': [date_to_dict(date) for date in latest_stocks.get('dates')],
            'datasets': [],
        }

        # Create a dataset for each available CSP
        for stock in all_stock_names:
            csp = AbstractCSP.get_csp(stock)  # get the class reference
            obj = {"label": str(csp.get_formal_name()),
                   'backgroundColor': str(csp.ui_colour),
                   'borderColor': str(csp.ui_colour),
                   'data': latest_stocks.get(stock, []),
                   'fill': False,
                   }
            data['datasets'].append(obj)

        return JsonResponse(data)
    else:
        # We ignore any other type of request (eg. GET, PUT etc.)
        return JsonResponse({'error-message': 'No data could be retrieved from server'}, status=422)


def update_migration_timeline(request):
    if request.method == 'GET':
        # First obtain the data that will populate the timeline
        last_migrations = MigrationEntry.objects.all().order_by(
            "-_date")[:10][::-1]

        # Then build the data object which will hold that data and colors
        data = {'migrations': [], }

        # List to store the row order in which CSP will appear on the timeline
        chart_row_ordering = []

        for i in range(len(last_migrations)):
            entry = last_migrations[i]

            # Now we'll format the migration entries for the chart to accept them
            entry_date = date_to_dict(entry._date)

            # If we are on the last entry, the 'date_until' variable should be today's date.
            # Meaning that since the last migration, the app is still running on that CSP until this day.
            if i == len(last_migrations) - 1:
                date_until = date.today()
            else:
                # until the next migration (i.e. next entry).
                date_until = last_migrations[i + 1]._date

            # Example: ['AWS', {'d': 30, 'm': 1, 'y': 2020}, {'d': 2, 'm': 2, 'y': 2020}]
            structured_entry = [
                entry._to,
                entry_date,
                date_to_dict(date_until)
            ]

            data.get('migrations', []).append(structured_entry)

            # Capture the order the database entry appeared in
            if entry._to not in chart_row_ordering:
                chart_row_ordering.append(entry._to)

        # Reference to all CSP needed to choose row colours
        all_csps = [AbstractCSP.get_csp(name) for name in AbstractCSP.get_stock_names()]
        colors_list = []

        # Loop through all CSPs to find the correct colour
        for row_name in chart_row_ordering:
            chosen_color = AbstractCSP.ui_colour  # in case we don't find a matching CSP class
            for csp in all_csps:
                if csp.get_formal_name() == row_name:
                    chosen_color = csp.ui_colour  # if found, update it
                    break
            colors_list.append(chosen_color)

        data['colors_list'] = colors_list

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
