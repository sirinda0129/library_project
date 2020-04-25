import pytest

from posts.models import Post


class TestGroupAPI:

    @pytest.mark.django_db(transaction=True)
    def test_get_group_list(self, client, approved_post, post1, post2, group1, group2):
        approved_post.group.add(group2)
        post1.group.add(group1)
        post2.group.add(group1)

        response = client.get('/api/v1/group/')
        assert response.status_code != 404, 'Проверьте, что url /api/v1/group/ существует'

        assert response.status_code == 200, 'Проверьте, что неавторизованный пользователь может получить список всех групп'

        test_data = response.json()
        assert test_data.get(
            'count') == 2, 'Проверьте, что запрос возвращает все группы'

        assert 'results' in test_data, 'Проверьте, что возвращаемый словарь содержит ключ results'

    @pytest.mark.django_db(transaction=True)
    def test_group_detail(self, client, group1):
        response = client.get(f'/api/v1/group/{group1.slug}/')
        assert response.status_code != 404, 'Проверьте, что страница с такой группой существует'

        assert response.status_code == 200, 'Проверьте, что неавторизованный пользователь может просматривать посты группы'

        assert type(response.json()
                    ) == dict, 'Проверьте, что запрос возвращает словарь'
