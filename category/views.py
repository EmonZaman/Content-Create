from django.shortcuts import render, redirect
from .models import *
# Create your views here.
import stripe


def charge(request):
    return render(request, 'charge.html')


from datetime import datetime, timedelta


def subscription(request):
    # if request.method == 'POST':
    #     amount = 1000
    #     stripe.api_key = "sk_test_51KeXrmExsbXRovz76iC19UwNt6uq4XfEjMZIIwfHoz8JW6Sq9UFLk8PfmpqHtE49a27bWjXgeLgRViJC4LpBoSUM001fgxvoRx"
    #     customer = stripe.Customer.create(
    #         email=request.user.email,
    #         source=request.POST['stripeToken']
    #     )
    #     charge = stripe.Charge.create(
    #         customer=customer,
    #         amount=amount,
    #
    #     )
    #     print(charge)
    # if charge['paid'] == True:
    #     profile = Profile.objects.fileter(user = request.user).first()
    #     profile.is_pro =True
    #     expiry = datetime.now() + timedelta(30)
    #     profile.pro_expiry_date = expiry
    #     profile.save()
    # return redirect('/charge/')

    return render(request, 's.html')
