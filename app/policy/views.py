from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['GET'])
def PrivacyPolicy(request):
    return render(request,'PrivacyPolicy.html')

@api_view(['GET'])
def RefundPolicy(request):
    return render(request,'RefundPolicy.html')

@api_view(['GET'])
def ShippingPolicy(request):
    return render(request,'ShippingPolicy.html')

@api_view(['GET'])
def TermsOfService(request):
    return render(request,'TermsOfService.html')