from django.core.mail import send_mail
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

import content_create.settings.defaults
from accounts.api.v1.serializers import UserSerializer
from accounts.models import User
from category.api.v1.serializers import CategorySerializer, VideoSerializer, VideolikeSerializer, SaveVideoSerializer, \
    RecentShownSerializers
from category.models import Category, Video, VideoLikes, SaveVideos, RecentShownVideos
from django.db.models import Sum
from datetime import datetime, timedelta
import stripe

# stripe.api_key = 'sk_test_51KeXrmExsbXRovz76iC19UwNt6uq4XfEjMZIIwfHoz8JW6Sq9UFLk8PfmpqHtE49a27bWjXgeLgRViJC4LpBoSUM001fgxvoRx'
stripe.api_key = content_create.settings.defaults.STRIPE_SECRET_KEY
print(stripe.api_key)


class CategoryListApiView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class VideoListApiView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VideoSerializer

    # print(Video.y)

    def get_queryset(self):
        queryset = Video.objects.all()
        category = self.request.query_params.get('category', None)
        recent, saved = self.request.query_params.get('recent'), self.request.query_params.get('saved')
        print("saved ")
        if recent is not None:
            return self.request.user.recentshownvideos.video.all() if hasattr(self.request.user,
                                                                              "recentshownvideos") else []
        if saved is not None:
            return self.request.user.savevideos.video.all() if hasattr(self.request.user, "savevideos") else []
        if category is not None:
            return Video.objects.filter(category__name=category)
        return queryset

    # parser_classes = (FormParser, MultiPartParser)


class VideoDetailAPIView(RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = VideoSerializer

    def get_queryset(self):
        return Video.objects.all()


# class Like(ListCreateAPIView):
#     serializer_class = VideolikeSerializer
#     queryset = VideoLikes.objects.all()
class Like(ListCreateAPIView):
    serializer_class = VideolikeSerializer
    queryset = VideoLikes.objects.all()


class LikeUpdate(RetrieveUpdateDestroyAPIView):
    serializer_class = VideolikeSerializer
    queryset = VideoLikes.objects.all()


class SaveVideo(ListCreateAPIView):
    serializer_class = SaveVideoSerializer
    queryset = SaveVideos.objects.all()


class SaveVideosUpdate(RetrieveUpdateDestroyAPIView):
    serializer_class = SaveVideoSerializer
    queryset = SaveVideos.objects.all()


class RecentVideos(ListCreateAPIView):
    serializer_class = RecentShownSerializers
    queryset = RecentShownVideos.objects.all()


class RecentVideosUpdate(RetrieveUpdateDestroyAPIView):
    serializer_class = RecentShownSerializers
    queryset = RecentShownVideos.objects.all()

    # def get(self, request, pk):
    #     video = Video.objects.filter(pk=pk)
    #     like_count = video.likevideos.count()
    #     serializer = VideolikeSerializer(like_count, many=True)
    #     return Response(serializer.data)
    #
    # def post(self, request, pk):
    #     likeusers = User.objects.get(id=2)
    #     likevideo = Video.objects.filter(pk=pk)
    #     check = VideoLikes.objects.filter(Q(likeusers=likeusers) & Q(likevideo = likevideo.last()))
    #     if (check.exists()):
    #         return Response({
    #             "status": status.HTTP_400_BAD_REQUEST,
    #             "message": "Already Liked"
    #         })
    #     new_like = VideoLikes.objects.create(likeusers=likeusers, likevideo=likevideo.last())
    #     new_like.save()
    #     serializer = VideolikeSerializer(new_like)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class category_content(ListAPIView):
#     serializer_class = VideoSerializer
#
#     def get_queryset(self):
#         category = self.request.query_params.get('category', None)
#
#         return Video.objects.filter(category__name=category)


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
        total_subscriber = self.request.query_params.get('total_subscriber', None)
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
        if total_subscriber == "true":
            pro_user_count = User.objects.aggregate(Sum('subscription_buy'))
            response['total_subscriber'] = pro_user_count
        return Response(response)


class StripeCreateCheckoutSessionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        print("in create checkout session")
        YOUR_DOMAIN = "http://localhost:3000"
        current_user = self.request.user.id
        print("checkout Session view")
        print(current_user)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            success_url=YOUR_DOMAIN + "/payment-success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=YOUR_DOMAIN + "/payment-cancel/",
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

            mode="payment",
        )
        # have to edit filed

        return Response(checkout_session.url, status=303)


class StripeSuccessAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        session_id = self.request.query_params.get('session_id', None)
        response = stripe.checkout.Session.retrieve(
            session_id,
        )
        if (response.status == "complete"):
            print('Alhamdulliah')
            print(response.customer_details.email)
            print(response.customer_details.name)
            user = User.objects.get(id=response.metadata.current_user)
            print(user.is_pro)
            user.is_pro = True
            print(user.pro_expiry_date)
            expiry = datetime.now() + timedelta(30)
            user.pro_expiry_date = expiry
            print(user.pro_expiry_date)
            if user.subscription_buy is None:
                user.subscription_buy = 1
            else:
                user.subscription_buy = user.subscription_buy + 1

            user.save()
            # user.save(update_fields=['is_pro'])
            print(user.is_pro)

            return Response(True)

        else:
            return Response(False)


# @csrf_exempt
# def stripe_webhook_view(request):
#     endpoint_secret = 'whsec_ed2c4b532bd6c36c87b878f1d1156ab13516e9c2f60108300fadf6ed6d687a36'
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)
#         # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         # current_user = request.user.id
#         print('Alhamdulliah')
#         CUSTOMER_EMAIL = session["customer_details"]["email"]
#         current_user = session["metadata"]["current_user"]
#         print(current_user)
#         user = User.objects.get(id=current_user)
#         print(user.is_pro)
#         user.is_pro = True
#         print(user.pro_expiry_date)
#         expiry = datetime.now() + timedelta(30)
#         user.pro_expiry_date = expiry
#         print(user.pro_expiry_date)
#         user.save()
#         print(CUSTOMER_EMAIL)
#         print(current_user)
#         send_mail(
#             subject="subcription",
#             message="thanks for your purchase",
#             recipient_list=[CUSTOMER_EMAIL],
#             from_email="emon@gmail.com",
#
#         )
#         print(session)
#     return HttpResponse(status=200)
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

class ReactNativeStripeCheckoutSessionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # current_user = self.request.user.id
        # customer = stripe.Customer.create(current_user)
        # ephemeralKey = stripe.EphemeralKey.create(
        #     customer=customer['id'],
        #     stripe_version='2020-08-27',
        # )
        paymentIntent = stripe.PaymentIntent.create(
            amount=1099,
            currency='usd',
            # customer=customer['id'],
            automatic_payment_methods={
                'enabled': True,
            },
        )
        print("payment")
        print(paymentIntent)
        # print(customer)
        # print(ephemeralKey)

        publishableKey = "pk_test_51KeXrmExsbXRovz7Ve5VBK7RLrMst5UZYDmL5izxHiaczqqUrGhGmhz8wwijvUxjJR8SOa6e9LIxIPSai3QhaWh100YSdfWuFb"
        return Response(paymentIntent, status=200)


class NativeAfterPaymentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        print(user.username)
        print(user.is_pro)
        user.is_pro = True
        print('user expiry date')
        print(user.pro_expiry_date)
        expiry = datetime.now() + timedelta(30)
        user.pro_expiry_date = expiry
        print('after expiry date')
        print(user.pro_expiry_date)
        if user.subscription_buy is None:
            user.subscription_buy = 1
        else:
            user.subscription_buy = user.subscription_buy + 1

        user.save()
        print('finally expiry date')
        print(user.pro_expiry_date)
        print(user.subscription_buy)
        # user.save(update_fields=['is_pro'])
        print(user.is_pro)
        return Response("User Filed Updated Successfully")

