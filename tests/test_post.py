import pytest
from django.shortcuts import reverse


class TestPost:

    @pytest.mark.django_db(transaction=True)
    def test_disapproved_post(self, client, disapproved_post):
        response = client.get(reverse('post', args=[disapproved_post.id]))
        assert response.status_code == 404, 'Проверьте, что непроверенный пост не появляется на сайте'

    @pytest.mark.django_db(transaction=True)
    def test_approved_post(self, client, approved_post, group1):
        approved_post.group.add(group1)
        approved_post.approved = True
        urls = ['/', reverse('group', args=[group1.slug]),
                reverse('post', args=[approved_post.id])]
        for url in urls:
            response = client.get(url)
            assert response.content.decode().find(
                approved_post.title), 'Проверьте, что подтверженный модератором пост появляется на странице'

    @pytest.mark.django_db(transaction=True)
    def test_post_create(self, client):
        response = client.post(reverse('new_post'), {
                               'title': 'Заголовок', 'url': 'http://url.net', 'language': 'RU'}, follow=True)
        assert response.status_code == 200, 'Проверьте, что неавторизованный пользователь может предложить запись'

        assert response.redirect_chain[0][0] == '/', 'Проверьте, что после предложения записи, клиент перенаправляется на главную страницу'

        response = client.post(reverse('new_post'), {}, follow=True)
        assert not response.redirect_chain, 'Проверьте, что при отправке невалидных данных, клиент остается на странице создания записи'
