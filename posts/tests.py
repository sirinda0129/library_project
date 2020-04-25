import datetime as dt

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post, Group


class TestPost(TestCase):

    def setUp(self):
        self.client = Client()
        self.group = Group.objects.create(title='Test group', slug='test-group', description='Group for test')
        self.post1 = Post.objects.create(title='Test post', url='http://example.net/test-url', description='link for test.', language='EN')

    def test_disapproved_post(self):
        response = self.client.get('/')
        self.assertNotContains(response, self.post1.title, status_code=200, html=False)

    def test_approved_post(self):
        post2 = Post.objects.create(title='Another post', url='http://another.net/test-url', description='link for test.', language='EN', approved=True)
        post2.group.add(self.group)
        urls = ['/', f'/group/{self.group.slug}/', f'/posts/{post2.id}/']
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, post2.title, status_code=200, html=False)
