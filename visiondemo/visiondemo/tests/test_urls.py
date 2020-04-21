from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import index, fileupload, result

class TestUrls(SimpleTestCase):

    def test_index_url(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_fileupload_url(self):
        url = reverse('fileupload')
        self.assertEquals(resolve(url).func, fileupload)

    def test_result_url(self):
        url = reverse('result')
        self.assertEquals(resolve(url).func, result)
