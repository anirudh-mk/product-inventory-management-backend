from rest_framework import serializers
from .models import Products, Variant, SubVariant


class SubVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVariant
        fields = ['options']


class VariantSerializer(serializers.ModelSerializer):
    options = SubVariantSerializer(many=True, source='products_subvariant_variant')

    class Meta:
        model = Variant
        fields = ['name', 'options']


class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, source='products_variant_product')

    class Meta:
        model = Products
        fields = [
            'ProductID',
            'ProductCode',
            'ProductName',
            'CreatedDate',
            'ProductImage',
            'UpdatedDate',
            'CreatedUser',
            'IsFavourite',
            'Active',
            'HSNCode',
            'TotalStock',
            'variants'
        ]

    def create(self, validated_data):
        variants_data = validated_data.pop('products_variant_product')
        product = Products.objects.create(**validated_data)
        for variant_data in variants_data:
            options_data = variant_data.pop('products_subvariant_variant')
            variant = Variant.objects.create(product=product, **variant_data)
            for option_data in options_data:
                SubVariant.objects.create(variant=variant, **option_data)
        return product
