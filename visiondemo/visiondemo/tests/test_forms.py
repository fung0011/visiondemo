from django.test import SimpleTestCase
from .forms import URLForm, UploadFileForm

class TestForms(SimpleTestCase):
    def test_urlform(self):
        form = URLForm()
        form.myinput = 'http://places.csail.mit.edu/demo/1.jpg'
        self.assertTrue(form.is_valid())

    def test_uploadfileform(self):
        form = UploadFileForm()
        form.file = File(open("/demo.jpg"))
        form.save()
        loca = form.objects.get(id=1).file.path
        self.failUnless(open(loca), 'file not found')
        self.assertTrue(form.is_valid())

    def test_urlform_NoData(self):
        form = URLForm()
        self.assertFalse(form.is_valid())

    def test_uploadfileform_NoData(self):
        form = UploadFileForm()
        self.assertFalse(form.is_valid())
