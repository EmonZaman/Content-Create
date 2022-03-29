from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from accounts.api.v1.serializers import UserSerializer
from accounts.models import User
from category.api.v1.serializers import CategorySerializer, VideoSerializer
from category.models import Category, Video

from datetime import datetime, timedelta
import stripe

stripe.api_key = 'sk_test_51KeXrmExsbXRovz76iC19UwNt6uq4XfEjMZIIwfHoz8JW6Sq9UFLk8PfmpqHtE49a27bWjXgeLgRViJC4LpBoSUM001fgxvoRx'


class CategoryListApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class VideoListApiView(ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    # parser_classes = (FormParser, MultiPartParser)


class VideoDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class category_content(ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category', None)

        return Video.objects.filter(category__name=category)


class category_content_count(GenericAPIView):
    serializer_class = VideoSerializer

    def get(self, request, *args, **kwargs):
        response = {}
        category = self.request.query_params.get('category', None)

        response["this_category_found_videos"] = Video.objects.filter(category__name=category).count()
        return Response(response)


class LastSevenDaysUserListAPIView(ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=7))
        return queryset


class LastSevenDaySubscriberListAPIView(ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=7), is_pro=True)
        return queryset


class UserAndSubscriberCountAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        response = {}
        # total_user= self.request.query_params.get('User', None)
        total_pro_user = self.request.query_params.get('total_pro_user', None)
        pro_user_seven = self.request.query_params.get('pro_user_seven', None)
        pro_user_today = self.request.query_params.get('pro_user_today', None)
        users_last_seven_days = self.request.query_params.get('users_last_seven_days', None)
        total_users = self.request.query_params.get('total_users', None)
        users_today = self.request.query_params.get('users_today', None)

        if total_pro_user == "true":
            pro_user_count = User.objects.filter(is_pro=True).count()
            response['Total_pro_users'] = pro_user_count
        if pro_user_seven == "true":
            pro_user_count = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=7),
                                                 is_pro=True).count()
            response['pro_users_last_seven_days'] = pro_user_count
        if pro_user_today == "true":
            pro_user_count = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=1),
                                                 is_pro=True).count()
            response['pro_users_today'] = pro_user_count
        if users_last_seven_days == "true":
            pro_user_count = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=7)).count()
            response['users_last_seven_days'] = pro_user_count
        if total_users == "true":
            pro_user_count = User.objects.count()
            response['total_users'] = pro_user_count

        if users_today == "true":
            pro_user_count = User.objects.filter(date_joined__gte=datetime.now() - timedelta(days=1)).count()
            response['users_today'] = pro_user_count

        return Response(response)


class CreateCheckoutSessionAPIView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        print("in create checkout session")

        YOUR_DOMAIN = "https://django-testing-app-check.herokuapp.com"
        current_user = self.request.user.id
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

        return Response(checkout_session.url, status=303)


#


@csrf_exempt
def stripe_webhook_view(request):
    endpoint_secret = 'whsec_ed2c4b532bd6c36c87b878f1d1156ab13516e9c2f60108300fadf6ed6d687a36'
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
        user = User.objects.get(id=current_user)
        print(user.is_pro)
        user.is_pro = True
        print(user.pro_expiry_date)
        expiry = datetime.now() + timedelta(30)
        user.pro_expiry_date = expiry
        print(user.pro_expiry_date)
        user.save()

        print(CUSTOMER_EMAIL)
        print(current_user)
        send_mail(
            subject="subcription",
            message="thanks for your purchase",
            recipient_list=[CUSTOMER_EMAIL],
            from_email="emon@gmail.com",

        )

        # print(session)

    return HttpResponse(status=200)
# @csrf_exempt
# def my_webhook_view(self, request):
#     payload = request.data
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, self.endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return Response(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return Response(status=400)
#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#
#         # Save an order in your database, marked as 'awaiting payment'
#         self.create_order(session)
#
#         # Check if the order is already paid (for example, from a card payment)
#         #
#         # A delayed notification payment will have an `unpaid` status, as
#         # you're still waiting for funds to be transferred from the customer's
#         # account.
#         if session.payment_status == "paid":
#             # Fulfill the purchase
#             self.fulfill_order(session)
#
#     elif event['type'] == 'checkout.session.async_payment_succeeded':
#         session = event['data']['object']
#
#         # Fulfill the purchase
#         self.fulfill_order(session)
#
#     elif event['type'] == 'checkout.session.async_payment_failed':
#         session = event['data']['object']
#
#         # Send an email to the customer asking them to retry their order
#         self.email_customer_about_failed_payment(session)
#
#     # Passed signature verification
#     return Response(status=200)
#
# def fulfill_order(self, session):
#
#     print("Fulfilling order")
#     user = self.request.user
#     user.is_pro = True
#     user.save(update_fields=['is_pro'])
#
# def create_order(self, session):
#     #
#     print("Creating order")
#
# def email_customer_about_failed_payment(self, session):
#     #
#     print("Emailing customer")
