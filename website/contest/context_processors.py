from contest import models

def contests_available(request):
    contests = models.Contest.objects.filter(published=True)
    return {'contests': contests}
