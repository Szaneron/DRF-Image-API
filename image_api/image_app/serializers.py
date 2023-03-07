from rest_framework import serializers
from .models import Image
from django.conf import settings
from rest_framework import serializers
from .models import Image
import accounts.models
from django.conf import settings
from PIL import Image as PILImage
from io import BytesIO
from urllib.parse import urljoin
from accounts.models import Account


class ImageSerializer(serializers.ModelSerializer):
    thumbnail_urls = serializers.SerializerMethodField()
    original_url = serializers.SerializerMethodField()
    expiring_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'image', 'uploaded_at', 'user', 'thumbnail_urls', 'original_url', 'expiring_url']

    def get_thumbnail_urls(self, obj):
        request = self.context.get('request')
        account = Account.objects.get(user=obj.user)
        account_tier = account.account_tier
        thumbnail_sizes = account_tier.thumbnail_sizes.split(',') if account_tier else ['200']
        thumbnail_urls = {}
        for size in thumbnail_sizes:
            thumbnail_urls[size] = request.build_absolute_uri(obj.image.url + f"?height={size}")
        return thumbnail_urls

    def get_original_url(self, obj):
        request = self.context.get('request')
        account = Account.objects.get(user=obj.user)
        account_tier = account.account_tier
        if account_tier and account_tier.original_url:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_expiring_url(self, obj):
        request = self.context.get('request')
        account = Account.objects.get(user=obj.user)
        account_tier = account.account_tier
        if account_tier and account_tier.expiring_url:
            expire_seconds = request.query_params.get('expire_seconds', 300)
            expire_seconds = max(min(expire_seconds, 30000), 300)
            return request.build_absolute_uri(obj.image.url + f"?expire_seconds={expire_seconds}")
        return None

    def validate_image(self, value):
        if value.content_type not in ['image/jpeg', 'image/png']:
            raise serializers.ValidationError('Invalid image format')
        return value
