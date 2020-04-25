import pytest

from posts.models import Post

class TestPostAPI:

    @pytest.mark.django_db(transaction=True)
    def test_get_post_list(self, client, approved_post, post1, post2, group1, group2):
        response = client.get('/api/v1/posts/')
        assert response.status_code != 404, 'Проверьте, что url /api/v1/posts/ существует'

        assert response.status_code == 200, 'Проверьте, что неавторизованный пользователь может просматривать все посты'

        test_data = response.json()
        assert test_data.get(
            'count') == 3, 'Проверьте, что запрос возвращает все посты'

        assert 'results' in test_data, 'Проверьте, что возвращаемый словарь содержит ключ results'
        approved_post.group.add(group2, group1)
        post1.group.add(group1)
        post2.group.add(group1)
        group1_posts_count = Post.objects.filter(group=group1).count()

        response = client.get(f'/api/v1/posts/?group={group1.slug}')
        test_data = response.json()
        assert test_data.get(
            'count') == group1_posts_count, f'Проверьте, что запрос возвращает все посты с группой {group1.slug}'

    @pytest.mark.django_db(transaction=True)
    def test_post_detail(self, client, post1):
        response = client.get(f'/api/v1/posts/{post1.pk}/')
        assert response.status_code != 404, 'Проверьте, что страница с таким постом существует'

        assert response.status_code == 200, 'Проверьте, что неавторизованный пользователь может просматривать пост'

        assert type(response.json()
                    ) == dict, 'Проверьте, что запрос возвращает словарь'

    @pytest.mark.django_db(transaction=True)
    def test_post_create(self, client):
        data = {
            'title': 'Заголовок',
            'url': 'http://url.net/',
            'language': 'RU',
        }
        response = client.post('/api/v1/posts/', data=data)
        assert response.status_code == 201, 'Проверьте, что неавторизованный пользователь может предложить запись'

        assert type(response.json(
        )) == dict, 'Проверьте, что после создания записи запрос возвращает словарь'

        response = client.post('/api/v1/posts/', data={})
        assert response.status_code == 400, 'Проверьте, что при POST-запросе с неправильными данными, возвращается статус-код 400'

    @pytest.mark.django_db(transaction=True)
    def test_post_edit(self, client, post1):
        data = {
            'description': 'Добавили описание ссылке к post1'
        }
        response = client.patch(f'/api/v1/posts/{post1.id}/', data=data)
        assert response.status_code == 401, 'Проверьте, что пользователь без админских прав не может редактировать пост'

        response = client.delete(f'/api/v1/posts/{post1.id}/')
        assert response.status_code == 401, 'Проверьте, что пользователь без админских прав не может удалить пост'
