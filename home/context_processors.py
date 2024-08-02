from home.models import HomePage

def base_data(request):
    data = {}
    home = HomePage.objects.get()
    home_page = HomePage.objects.get()
    data["home"] = home
    data["home_page"] = home_page
    return data