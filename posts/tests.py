from django.test import TestCase

from django.test import Client

from django.contrib.auth import get_user_model

from django.urls import reverse

from .models import Post, Follow

import datetime as dt

from django.core.cache import cache


User = get_user_model()

# Create your tests here.


class TestUser(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'testpassword',
            email = 'test@email.yatube'
            )

    def test_pofile(self):
        response = self.client.get('/testuser/')
        self.assertEqual(response.status_code, 200)

    def test_new_post_authorized(self):
        self.client.login(username = 'testuser', password = 'testpassword')
        response = self.client.post('/new/', {'text':'testpost'}, follow = True)
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get(text = 'testpost')
        post_id = post.id
        username = self.user.username
        response = self.client.get(f'/{username}/{post_id}/')
        self.assertEqual(response.status_code, 200)

    def test_new_post_not_authorized(self):
        response = self.client.post('/new/', {'text':'testpost', 'author':self.user}, follow = True, msg = 'Не авторизованный пользователь не может создать пост')
        self.assertRedirects(response, '/auth/login/?next=/new/', status_code=302, target_status_code=200, msg_prefix='Неавторизованного не перенаправляет на логин', fetch_redirect_response=True)


class TestPost(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'testpassword',
            email = 'test@email.yatube'
            )
        self.post = Post.objects.create(
            text = 'Test post',
            author = self.user,
            pub_date = '01.01.2020'
            )
        self.post_id = self.post.pk
        cache.clear()

    def test_new_post_on_pages(self):
        self.client.login(username = 'testuser', password = 'testpassword')
        urls = ['/', '/testuser/', f'/testuser/{self.post_id}/']
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, self.post.text, count=None, status_code=200, msg_prefix='Пост не найден', html=False)

    def test_post_edit(self):
        self.client.login(username='testuser', password='testpassword')
        post_text = 'Test post'
        post_id = self.post.pk
        self.post = Post.objects.create(text=post_text, author=self.user)
        response = self.client.post(f'/testuser/{post_id}/edit/', {'text':'Modified test post'})
        urls = ['/', '/testuser/', f'/testuser/{self.post_id}/']
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, 'Modified test post', count=None, status_code=200, msg_prefix=f'Пост не найден ({self.post.text})', html=False)


class TestExceptions(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'testpassword',
            email = 'test@email.yatube'
            )
        self.post = Post.objects.create(
            text = 'Test post',
            author = self.user,
            pub_date = '01.01.2020'
            )
        self.post_id = self.post.pk
        cache.clear()

    def test_404_error(self):
        response = self.client.get('/testuserxx/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, template_name = 'misc/404.html', msg_prefix='Не использован шаблон 404.html')


class TestImg(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'testpassword',
            email = 'test@email.yatube'
            )
        self.client.force_login(self.user)
        with open('media/posts/Ava.jpg', 'rb') as img: 
            self.client.post('/new/', {'text': 'Text', 'image': img})
        cache.clear()

    def test_image_post(self):
        response = self.client.get("/testuser/1/")
        self.assertContains(response, '<img ', status_code=200 )

    def test_image_index(self):
        response = self.client.get("")
        self.assertContains(response, '<img ', status_code=200 )

    def test_image_profile(self):
        response = self.client.get("/testuser/")
        self.assertContains(response, '<img ', status_code=200 )
    

class TestWrongImgFile(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'testpassword',
            email = 'test@email.yatube'
            )
        self.client.force_login(self.user)
        with open('media/posts/test_file.txt', 'rb') as img: 
            self.client.post('/new/', {'text': 'Text', 'image': img})
        cache.clear()

    def test_txt_img(self):
        response = self.client.get("/testuser/")
        self.assertNotContains(response, '<img ', status_code=200 )


class TestFollowings(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'testpassword',
            email = 'test@email.yatube'
            )
        self.post = Post.objects.create(
            text = 'Test post',
            author = self.user,
            pub_date = '01.01.2020'
            )
        self.follower = User.objects.create_user(
            username = 'testfollower',
            password = 'testpassword',
            email = 'testfollower@email.yatube'
            )
        
    def test_not_authorized_follow(self):
        response = self.client.get('/testuser/follow')
        self.assertNotContains(response, 'Отписаться', status_code=302, msg_prefix='Удалось подписаться неавторизованному')

    def test_authorized_follow(self):
        self.client.force_login(self.follower)
        response = self.client.get('/testuser/follow')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/testuser/')

    def test_authorized_follow(self):
        self.client.force_login(self.follower)
        self.client.get('/testuser/follow')
        response = self.client.get('/follow/')
        self.assertContains(response, 'Test post')


class TestComments(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'testpassword',
            email = 'test@email.yatube'
            )
        self.post = Post.objects.create(
            text = 'Test post',
            author = self.user,
            pub_date = '01.01.2020'
            )
        self.follower = User.objects.create_user(
            username = 'testfollower',
            password = 'testpassword',
            email = 'testfollower@email.yatube'
            )

    def test_authorized_comment(self):
        self.client.force_login(self.follower)
        self.client.post('/testuser/1/comment', {'text' : 'test comment'})
        cache.clear()
        response = self.client.get('/testuser/1/')
        self.assertContains(response, 'test comment', status_code=200)
        