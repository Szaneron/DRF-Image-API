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
    thumbnail_url_200 = serializers.SerializerMethodField()
    thumbnail_url_400 = serializers.SerializerMethodField()
    original_url = serializers.SerializerMethodField()
    expiring_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'image', 'uploaded_at', 'user', 'thumbnail_url_200', 'thumbnail_url_400', 'original_url',
                  'expiring_url']

    def get_thumbnail_url_200(self, obj):
        request = self.context.get('request')
        account = Account.objects.get(user=obj.user)
        if account.account_type == Account.BASIC or account.account_type == Account.PREMIUM or account.account_type == Account.ENTERPRISE:
            return request.build_absolute_uri(obj.image.url + "?height=200")
        return None

    def get_thumbnail_url_400(self, obj):
        request = self.context.get('request')
        account = Account.objects.get(user=obj.user)
        if account.account_type == Account.PREMIUM or account.account_type == Account.ENTERPRISE:
            return request.build_absolute_uri(obj.image.url + "?height=400")
        return None

    def get_original_url(self, obj):
        request = self.context.get('request')
        account = Account.objects.get(user=obj.user)
        if account.account_type == Account.PREMIUM or account.account_type == Account.ENTERPRISE:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_expiring_url(self, obj):
        request = self.context.get('request')
        account = Account.objects.get(user=obj.user)
        if account.account_type == Account.ENTERPRISE:
            expire_seconds = request.query_params.get('expire_seconds', 300)
            expire_seconds = max(min(expire_seconds, 30000), 300)
            return request.build_absolute_uri(obj.image.url + f"?expire_seconds={expire_seconds}")
        return None
