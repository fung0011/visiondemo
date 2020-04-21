from django.test import TestCase, Client
from django.urls import reverse
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.result_url = reverse('result')
        self.fileupload_url = reverse('fileupload')

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'visiondemo/demo.html')

    def test_result_GET(self):
        response = self.client.get(self.result_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'visiondemo/result.html')

    def text_fileupload_POST_NoData(self):
        response = self.client.post(self.fileupload_url)
        self.assertEquals(response.status_code, 404)

    def text_fileupload_POST_url(self):
        response = self.client.post(self.fileupload_url, {
            'myinput': 'http://places.csail.mit.edu/demo/1.jpg'
        })
        self.assertEquals(response.status_code, 302)
        
    def text_fileupload_POST_file(self):
        response = self.client.post(self.fileupload_url, {
            'file': File(open("/demo.jpg")
        })
        self.assertEquals(response.status_code, 302)
