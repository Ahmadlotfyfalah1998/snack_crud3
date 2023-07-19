from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from django.contrib.auth import get_user_model
from .models import Snack
from django.urls import reverse
# Create your tests here.
class Snacktest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='random',email='random@random.com',
            password='random@12345'
        )
        self.snack = Snack.objects.create(
            title = 'test',
            purchaser=self.user,
            description = 'test_dis'
        )

    def test_str_method(self):
        self.assertEqual(str(self.snack),'test')

    def test_detail_view(self):
        url = reverse('snack_detail',args=[self.snack.id])  
        response = self.client.get(url)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'snack_detail.html')


    def test_create_view(self):
        url = reverse('snack_create')
        data={
            "title": "test_2",
            "purchaser" : self.user.id,
            "description": 'description'
        }


        response = self.client.post(path=url,data = data,follow = True)
        self.assertTemplateUsed(response,'snack_detail.html')
        self.assertEqual(len(Snack.objects.all()),2)
        self.assertRedirects(response, reverse('snack_detail',args=[2]))
        
        
        
    def test_update_view(self):
        url = reverse('snack_update', args=[self.snack.id])
        data = {
            "title": "updated_test",
            "purchaser": self.user.id,
            "description": 'updated_description'
        }

        response = self.client.post(path=url, data=data, follow=True)
        self.assertTemplateUsed(response, 'snack_list.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Snack.objects.get(id=self.snack.id).title, 'updated_test')

    def test_delete_view(self):
        url = reverse('snack_delete', args=[self.snack.id])

        response = self.client.post(path=url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Snack.objects.all()), 0)
        self.assertRedirects(response, reverse('snack_list'))