import math
import json
import datetime
import pdb
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from models import Place
from trip.models import LogEntry, Resource, Activities


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1))\
                                              * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def how_many_kilometers(to_station, from_station):
    origin = to_station.Latitude, to_station.Longitude
    destination = from_station.Latitude, to_station.Longitude
    return distance(origin,destination)

def nearby_places(rel_place, distance_threshold):
    pass

def create_trip(request, template_name):
    """
    creates a trip for you
    """
    return render_to_response(template_name, RequestContext(request))

def get_nearby_places(request, place_name, threshold = 0.1):
    place = Place.objects.filter(DisplayName__icontains = place_name)
    if not place:
        response = {'response':500, 'data':"No such place!" }
        return HttpResponse(json.dumps(response))
    place = place[0]
    lat = place.Latitude
    lon = place.Longitude
    lat_range = (float(lat)-threshold, float(lat)+threshold)
    long_range = (float(lon)-threshold, float(lon)+threshold)
    nearby = Place.objects.filter(Latitude__range = lat_range, Longitude__range = long_range).values_list('DisplayName')
    if not nearby:
        response = {'response':500, 'data':"no nearby places!" }
        return HttpResponse(json.dumps(response))

    response = {'response':200, 'data':list(nearby)}
    return HttpResponse(json.dumps(response))

def create_log_entry(request):
    """ Create a log entry for the trip
    """
    user_id = request.POST.get('user_id','')
    trip_id = request.POST.get('trip_id','')
    lat = request.POST.get('latitude', '')
    lon = request.POST.get('logitude','')
    log_type = request.POST.get('log_type','')
    log_time = request.POST.get('log_time','')
    data = request.POST.get('data','')
    caption = request.POST.get('caption','')

    LogEntry(UserID = user_id,
            TripID = trip_id,
            Latitude =lat,
            Longitude = lon,
            LogTime = log_time,
            LogType = log_type,
            Data = data).save()

    if caption:
        LogEntry(UserID = user_id,
            TripID = trip_id,
            Latitude =lat,
            Longitude = lon,
            LogTime = log_time,
            LogType = 'text',
            Data = data).save()
    response = {'response':200, 'data':"success"}
    return HttpResponse(json.dumps(response))



def plan_trip(request):
    """
    request will have details like:
    1. Total budget
    2. Place (from, to)
    3. from - to (date)
    4. modus transportandi

    returns suggested hotels, corresponding expenditures
    """
    total = request.POST.get('total_budget','')

    from_station_id = request.POST.get('from_station','')
    to_station_id = request.POST.get('to_station','')

    from_station = Place.objects.get(PlaceID = from_station_id)
    to_station = Place.objects.get(PlaceID = to_station_id)

    tr_type = request.POST.get('travel_type','')

    to_day = request.POST.get('to_day','')
    from_day = request.POST.get('from_day','')

    to_day = datetime.datetime.strptime(to_day,"%d-%m-%y")
    from_day = datetime.datetime.strptime(from_day,"%d-%m-%y")

    kms = how_many_kilometers(from_station, to_station)
    days = (to_day - from_day).days

    travel_expenditure = get_travel_cost(kms)
    remaining_budget = total - travel_expenditure

    suggested_hotels = match_hotels_by_budget(to_station_id, remaining_budget/days)
    hotel_list = [{'name':json.dumps(i.Data)['hotel_type'],
                   'expense':json.dumps(i.Data)['cost_per_day']*days} for i in suggested_hotels]
    data = {'travel_expense':travel_expenditure, 'hotels':hotel_list}
    return HttpResponse(json.dumps({'response':200, 'data':data}))



def trip_planner(request):
    """
    HERE BE DRAGONS!!
    this tiny little function
    creates a timeline of
    """
    destinations = request.POST.getlist('places')
    travel_mode = request.POST.get('travel_mode','')
    from_date = request.POST.get('from_date','')
    to_date = request.POST.get('to_date','')
    budget = request.POST.get('budget','')
    import pdb; pdb.set_trace()

    pass




def diff_transport_fares(a,b):
    """
    difference between fares
    """
    adata = json.loads(a.Data)
    bdata = json.loads(b.Data)
    return cmp(adata['cost_per_km'], bdata['cost_per_km'])

def diff_hotel_fares(a,b):
    """
    difference between fares
    """
    adata = json.loads(a.Data)
    bdata = json.loads(b.Data)
    return cmp(adata['cost_per_day'], bdata['cost_per_day'])



def match_transport_by_budget(tr_b, tr_type, place_id):

    """
    returns list of Resource objects matching budget
    """
    transport_fares = Resource.objects.filter(Data__icontains = '''"transport_type": "%s"}'''%tr_type).filter(PlaceID=place_id)

    transport_fares = list(transport_fares)
    transport_fares.sort(cmp=diff_transport_fares)
    if len(transport_fares) >=3:
        return transport_fares[:3]
    else:
        return transport_fares


def match_hotels_by_budget(place_id,hotel_b):
    """
    returns cheapest, costliest and avg hotels based on budget
    """
    hotels = Resource.objects.filter(PlaceID = place_id).filter(Data__icontains = '''"hotel_type""}''')
    if not hotels:
        return []
    hotels = list(hotels)
    hotels.sort(cmp=diff_hotel_fares)
    cheapest = hotels[0]
    for i in hotels:
        if json.loads(hotels.Data)['cost_per_day']>hotel_b:
            break
    costliest = hotels[i-1]
    avg = hotels[i/2]
    return cheapest, avg, costliest


def breakup_budget_place(total, kms, to_station_id):
    bud = total
    travel_ex = get_travel_cost(kms)
    bud -= travel_ex
    c,a,co = match_hotels_by_budget(to_station_id, bud)
    hotel_ex = days * a
    if hotel_ex >= bud:
        hotel_ex = days*c
    bud -= hotel_ex
    return travel_ex, hotel_ex, bud

def activities_at(place_id, day, duration):
    all_acs = Activities.objects.filter(PlaceID = place_id).filter(Duration__lt = duration*24)
    acs=[]
    if all_acs.count() >= 2:
        all_acs = all_acs[:2]
    for a in all_acs:
        acs.append({'date':str(day),'activity' : a.Name })
    return acs

def create_timeline(destinations, from_date, to_date):
    """
    returns a timeline dict. repr. of type [{date:, activity:},]
    """
    timeline = []
    from_date = datetime.datetime.strptime(from_date,"%d-%m-%y")
    to_date =  datetime.datetime.strptime(to_date,"%d-%m-%y")

    days = (to_date - from_date).days

    date = from_date
    if len(destinations) == days:
        for place in destinations:
            timeline+=(activities_at(place,date,datetime.timedelta(1)))
            date = date + datetime.timedelta(1)
    elif len(destinations) > days:
        d= destinations.pop()
        timeline+=(activities_at(d,date,datetime.timedelta(len(destinations)-days)))
        date = date + datetime.timedelta(1)
        for place in destinations:
            timeline+=(activities_at(place,date,datetime.timedelta(1)))
            date = date + datetime.timedelta(1)

    return timeline


def breakup_budget_old(total,tr_type, days, kms):
    """
    heursitic to find out % breakup of budget
    """
    #lukkhagiri
    transport_fares = Resource.objects.filter(Data__icontains = '''"transport_type": "%s"}'''%tr_type)\
        .values_list('Data', flat = True)


    transp_fare = 0
    for i in transport_fares:
        transp_fare = transp_fare + json.loads(i)['cost_per_km']

    hotel_fares = Resource.objects.filter(Data__icontains = '''"hotel_type":''').values_list('Data', flat = True)
    hotel_fare = 0
    for i in hotel_fares:
        hotel_fare = hotel_fare + min_hotel_fare, json.loads(i)['cost_per_day']


    total_stay_kharcha = days * min_hotel_fare
    total_travel_kharcha = kms*min_transp_fare * 2
    return total_travel_kharcha, total_stay_kharcha

def get_travel_cost(kms,  avg_cost = 11):
    return kms*avg_cost*2