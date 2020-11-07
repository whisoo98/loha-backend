from rest_framework import serializers
from .models import Categories
from django.core.validators import MaxValueValidator, MinValueValidator


class ListAllCategoriesSerializer(serializers.Serializer): #ALL from cafe 24
    shop_no = serializers.IntegerField(default=1, verbose = '멀티쇼핑몰 번호')
    category_depth = serializers.IntegerField(validators=[
            MaxValueValidator(4),
            MinValueValidator(1)
        ], verbose='분류 Depth') #최소: [1]    ~최대: [4]
    category_no = serializers.IntegerField(verbose='분류 번호')
    parent_category_no = serializers.IntegerField(default=1, verbose='부모 분류 번호')
    category_name = serializers.CharField(max_length=50, verbose='분류명')
    limit =serializers.IntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ], default=10, verbose='조회결과 최대건수') #최소: [1]    ~최대: [100]
    offset = serializers.IntegerField(validators=[
            MaxValueValidator(8000),
        ], verbose='조회결과 시작위치') #최대값: [8000]
