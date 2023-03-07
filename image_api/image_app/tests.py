from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from accounts.models import Account, AccountTier
import io
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class ImageViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.account_tier = AccountTier.objects.create(
            name='Base',
            thumbnail_sizes='200',
            original_url=False,
            expiring_url=False
        )
        self.account = Account.objects.create(user=self.user, account_tier=self.account_tier)
        self.client.force_authenticate(user=self.user)

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGB', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_upload_photo(self):
        """
        Test if we can upload a photo
        """

        url = reverse('user-images:upload-photo')

        photo_file = self.generate_photo_file()

        data = {
            'photo': photo_file
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
