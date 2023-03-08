from io import BytesIO

from PIL import Image as pilImage
from accounts.models import Account, AccountTier
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from .models import Image


class ImageUploadTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

        self.basic_tier = AccountTier.objects.create(
            name='Basic',
            thumbnail_sizes='200',
            original_url=False,
            expiring_url=False,
        )

        self.basic_account = Account.objects.create(
            user=self.user,
            account_tier=self.basic_tier,
        )

        self.client.force_authenticate(user=self.user)

    def test_upload_image(self):
        # Create a test image
        image_data = BytesIO()
        image = pilImage.new('RGB', (100, 100), (255, 255, 255))
        image.save(image_data, 'jpeg')
        image_data.seek(0)
        image_file = SimpleUploadedFile("test_image.jpg", image_data.read(), content_type="image/jpeg")

        self.image_data = {
            'image': image_file,
            'user': self.user.id
        }
        response = self.client.post('/image_api/upload-image//', self.image_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)
        image = Image.objects.first()
        self.assertEqual(image.user, self.user)

    def test_list_images(self):
        # Create some images for the user
        Image.objects.create(user=self.user, image='images/test1.jpg')
        Image.objects.create(user=self.user, image='images/test2.jpg')

        response = self.client.get('/image_api/list-image//')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class AccountTierTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.admin_user)
        self.basic_tier = AccountTier.objects.create(
            name='Basic Tier',
            thumbnail_sizes='200',
            original_url=False,
            expiring_url=False
        )
        self.premium_tier = AccountTier.objects.create(
            name='Premium Tier',
            thumbnail_sizes='200,400',
            original_url=True,
            expiring_url=False
        )
        self.enterprise_tier = AccountTier.objects.create(
            name='Enterprise Tier',
            thumbnail_sizes='200,400,600',
            original_url=True,
            expiring_url=True
        )

    def test_create_account_tier(self):
        url = reverse('tiers-list')
        data = {
            'name': 'New Tier',
            'thumbnail_sizes': '200,300,400',
            'original_url': True,
            'expiring_url': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tier = AccountTier.objects.get(name='New Tier')
        self.assertEqual(tier.thumbnail_sizes, '200,300,400')
        self.assertTrue(tier.original_url)
        self.assertTrue(tier.expiring_url)

    def test_list_account_tiers(self):
        url = reverse('tiers-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tiers = response.json()
        self.assertEqual(len(tiers), 3)

    def test_retrieve_account_tier(self):
        url = reverse('tiers-detail', args=[self.basic_tier.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tier = response.json()
        self.assertEqual(tier['name'], self.basic_tier.name)
        self.assertEqual(tier['thumbnail_sizes'], self.basic_tier.thumbnail_sizes)
        self.assertEqual(tier['original_url'], self.basic_tier.original_url)
        self.assertEqual(tier['expiring_url'], self.basic_tier.expiring_url)

    def test_update_account_tier(self):
        url = reverse('tiers-detail', args=[self.basic_tier.pk])
        data = {
            'name': 'Updated Tier',
            'thumbnail_sizes': '300,400',
            'original_url': True,
            'expiring_url': False
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tier = AccountTier.objects.get(pk=self.basic_tier.pk)
        self.assertEqual(tier.name, 'Updated Tier')
        self.assertEqual(tier.thumbnail_sizes, '300,400')
        self.assertTrue(tier.original_url)
        self.assertFalse(tier.expiring_url)

    def test_delete_account_tier(self):
        url = reverse('tiers-detail', args=[self.basic_tier.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AccountTier.objects.count(), 2)
