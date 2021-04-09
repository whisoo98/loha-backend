from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['GET'])#개인정보처리방침
def PrivacyPolicy(request):
    return render(request,'PrivacyPolicy.html')

@api_view(['GET'])#환불정책
def RefundPolicy(request):
    return render(request,'RefundPolicy.html')

@api_view(['GET'])#배송정책
def ShippingPolicy(request):
    return render(request,'ShippingPolicy.html')

@api_view(['GET'])#청소년보호방침
def YouthProtectionPolicy(request):
    return render(request,'YouthProtectionPolicy.html')

@api_view(['GET'])#일반이용약관
def GenralToS(request):
    return render(request,'GeneralToS.html')

@api_view(['GET'])#해외구매대행이용약관
def AbroadToS(request):
    return render(request,'AbroadToS.html')

@api_view(['GET'])#판매이용약관
def SellingToS(request):
    return render(request,'SellingToS.html')