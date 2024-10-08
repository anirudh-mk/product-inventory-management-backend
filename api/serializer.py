import uuid

from rest_framework import serializers
from .models import Products, Variant, SubVariant
from django.contrib.auth.models import User


class SubVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVariant
        fields = ['options']


class VariantSerializer(serializers.ModelSerializer):
    sub_variants = SubVariantSerializer(many=True, read_only=True)
    options = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Variant
        fields = ['name', 'options', 'sub_variants']

    def create(self, validated_data):
        options = validated_data.pop('options')
        variant = Variant.objects.create(**validated_data)
        for option in options:
            SubVariant.objects.create(variant=variant, options=option)
        return variant


class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)

    class Meta:
        model = Products
        fields = [
            'id',
            'ProductID',
            'ProductCode',
            'ProductName',
            'CreatedDate',
            'ProductImage',
            'UpdatedDate',
            'IsFavourite',
            'Active',
            'HSNCode',
            'TotalStock',
            'variants'
        ]

    def create(self, validated_data):
        variants_data = validated_data.pop('variants')
        user = self.context.get('user')
        product = Products.objects.create(CreatedUser=user, **validated_data)
        for variant_data in variants_data:
            VariantSerializer().create({**variant_data, 'product': product})
        return product


class StockCreateSerializer(serializers.ModelSerializer):
    options = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Variant
        fields = ['name', 'options', 'product']

    def create(self, validated_data):
        options = validated_data.pop('options', [])
        variant = Variant.objects.create(**validated_data)
        for option in options:
            SubVariant.objects.create(variant=variant, options=option)
        return variant


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]