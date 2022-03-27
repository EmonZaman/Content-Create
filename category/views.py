from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
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




# class SuccessView(ListView):
#     # context_object_name = 'userproject_list'
#     template_name = "success.html"
#     def get_queryset(self, request):
#         current_user = request.user
#         print( current_user.id)
#         print(current_user.is_pro)
#         current_user.is_pro= True
#
#         return current_user

class CancelView(TemplateView):
    template_name = "cancel.html"


class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        product = UserSubscription.objects.get(name="Test Product")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
        })

        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        print("in create checkout session")
        # product_id= self.kwargs["pk"]
        # product = UserSubscription.objects.get(id=3)
        # print(product.price)
        # print(product.name)
        # print(product.user.username)
        current_user = request.user.id
        print("checkout Session view")
        print(current_user)
        # print( current_user.id)
        # print(current_user.is_pro)
        # current_user.is_pro= True
        # current_user.save()
        # print(current_user.is_pro)
        # print(current_user.pro_expiry_date)
        # expiry = datetime.now() + timedelta(30)
        # current_user.pro_expiry_date = expiry
        # print(current_user.pro_expiry_date)
        # current_user.save()

        # YOUR_DOMAIN = "https://django-testing-app-check.herokuapp.com"
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            # payment_method_type=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 30000,
                        'product_data': {
                            'name': 'checkout',

                        },
                    },
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    # 'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            metadata={
                "current_user": current_user

            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        # return JsonResponse({
        #     'id': checkout_session.id
        #
        # })
        # print(checkout_session)


        return redirect(checkout_session.url, code=303)



@csrf_exempt
def stripe_webhook_view(request):
    endpoint_secret= 'whsec_ed2c4b532bd6c36c87b878f1d1156ab13516e9c2f60108300fadf6ed6d687a36'
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
        # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # current_user = request.user.id
        print('Alhamdulliah')
        # print( current_user)
        # print(current_user.is_pro)
        # current_user.is_pro= True
        # current_user.save()
        # print('alhamdulliah')
        # Fulfill the purchase...
        CUSTOMER_EMAIL = session["customer_details"]["email"]
        current_user = session["metadata"]["current_user"]
        print(current_user)
        user = User.objects.get(id= current_user)
        print(user.is_pro)
        user.is_pro= True
        print(user.pro_expiry_date)
        expiry = datetime.now() + timedelta(30)
        user.pro_expiry_date = expiry
        print(user.pro_expiry_date)
        user.save()


        print(CUSTOMER_EMAIL)
        print(current_user)
        send_mail(
            subject= "subcription",
            message= "thanks for your purchase",
            recipient_list= [CUSTOMER_EMAIL],
            from_email= "emon@gmail.com",

        )

        # print(session)

    return HttpResponse(status=200)