from rest_framework import serializers
from .models import Product
from django.core.validators import MaxValueValidator,MinValueValidator

class ListAllCategoriesSerializer(serializers.Serializer):
    shop_no = serializers.IntegerField(default=1, verbose='멀티쇼핑몰 번호')
    category_no = serializers.IntegerField(verbose='분류 번호')
    display_group = serializers.IntegerField(validators=[
        MaxValueValidator(3),
        MinValueValidator(1)
    ], verbose='상세 상품분류')#최소: [1]    ~최대: [3]
    limit = serializers.IntegerField(validators=[
        MaxValueValidator(50000),
        MinValueValidator(1)
    ], default=50000, verbose = '조회결과 최대건수')#최소: [1]    ~최대: [50000]
