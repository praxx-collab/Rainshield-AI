from django.shortcuts import render, redirect
from .models import Worker, Policy
import requests


# REGISTER
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        city = request.POST.get("city")
        income = request.POST.get("income")

        worker = Worker.objects.create(
            name=name,
            city=city,
            daily_income=income
        )

        return redirect(f"/dashboard/{worker.id}/")

    return render(request, "register.html")


# DASHBOARD
def dashboard(request, worker_id):
    worker = Worker.objects.get(id=worker_id)

    # Dynamic premium (AI feel)
    if worker.daily_income < 300:
        premium = 30
    elif worker.daily_income < 600:
        premium = 50
    else:
        premium = 80

    Policy.objects.create(
        worker=worker,
        premium=premium
    )

    return render(request, "dashboard.html", {
        "worker": worker,
        "premium": premium
    })


# CLAIM SYSTEM (FINAL VERSION)
def claim(request):
    city = request.GET.get('city', 'Pune')

    API_KEY = "dd7d4f96cefd6e2eb0e56572190f60b6"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    response = requests.get(url)
    data = response.json()

    # ❗ Handle invalid city
    if data.get("cod") != 200:
        return render(request, "claim.html", {
            "city": city,
            "result": "❌ Invalid city name",
            "status_class": "danger"
        })

    # Safe weather extraction
    weather = data.get("weather", [{}])[0].get("main", "Clear")

    # Detect rain
    rain = weather.lower() in ["rain", "drizzle", "thunderstorm"]

    # 🔥 DEMO CONTROL (optional)
    force_rain = request.GET.get('force_rain')
    if force_rain == "true":
        rain = True

    # Movement control
    movement_param = request.GET.get('move')
    if movement_param == "moving":
        movement = "moving"
    else:
        movement = "static"

    # Orders control
    orders_param = request.GET.get('orders')
    if orders_param:
        orders = int(orders_param)
    else:
        orders = 0

    # FINAL LOGIC
    if not rain:
        result = "❌ No claim (No disruption)"
        status_class = "danger"

    elif movement == "moving" and orders > 0:
        result = "✅ Claim Approved ₹500"
        status_class = "success"

    elif movement == "static" and orders == 0:
        result = "⚠️ Suspicious (Possible fraud)"
        status_class = "warning"

    else:
        result = "🔍 Under Review"
        status_class = "warning"

    return render(request, "claim.html", {
        "city": city,
        "weather": weather,
        "rain": rain,
        "movement": movement,
        "orders": orders,
        "result": result,
        "status_class": status_class
    })