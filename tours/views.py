from django.shortcuts import render

from django.views import View

from .data import departures, description, subtitle, title, tours


def my_render(request, html, data):
    data['title'] = title
    data['subtitle'] = subtitle
    data['description'] = description
    data['departures'] = departures

    return render(request, html, data)


class MainView(View):
    def get(self, request, *args, **kwargs):
        chosen_tours = []
        for id, tour_info in tours.items():
            chosen_tours.append({'title': tour_info['title'], 'description': tour_info['description'],
                                 'picture': tour_info['picture'], 'id': str(id)})

        return my_render(request, 'tours/index.html', {'tours': chosen_tours})


class DepartureView(View):
    def get(self, request, departure, *args, **kwargs):

        chosen_tours = []
        min_price = int(1e10)
        max_price = 0
        min_nights = int(1e10)
        max_nights = 0
        for tour_id, tour_info in tours.items():
            if tour_info['departure'] == departure:
                chosen_tours.append((str(tour_id), tour_info))
                min_price = min(min_price, tour_info['price'])
                max_price = max(max_price, tour_info['price'])
                min_nights = min(min_nights, tour_info['nights'])
                max_nights = max(max_nights, tour_info['nights'])

        departure = departures[departure].split()[1]

        return my_render(request, 'tours/departure.html', {'min_nights': min_nights, 'max_nights': max_nights,
                                                           'min_price': min_price, 'max_price': max_price,
                                                           'chosen_tours': chosen_tours, 'count': len(chosen_tours),
                                                           'departure': departure})


class TourView(View):
    def get(self, request, id, *args, **kwargs):
        tour = tours[id]
        departure = departures[tour['departure']].split()[1]
        return my_render(request, 'tours/tour.html', {'tour': tour, 'departure': departure})
