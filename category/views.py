from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import UserSubscription
from .models import *
# Create your views here.
import stripe

stripe.api_key = 'sk_test_51KeXrmExsbXRovz76iC19UwNt6uq4XfEjMZIIwfHoz8JW6Sq9UFLk8PfmpqHtE49a27bWjXgeLgRViJC4LpBoSUM001fgxvoRx'


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

class SuccessView(TemplateView):

     template_name = "success.html"

class CancelView(TemplateView):
     template_name = "cancel.html"

class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        product= UserSubscription.objects.get(name="Test Product")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
        })

        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        print("in create checkout session")
        # product_id= self.kwargs["pk"]
        product = UserSubscription.objects.get(id=3)
        print(product.price)
        print(product.name)
        print(product.user.username)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            # payment_method_type=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,


                        },
                    },
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    # 'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        # return JsonResponse({
        #     'id': checkout_session.id
        #
        # })
        return redirect(checkout_session.url, code=303)
