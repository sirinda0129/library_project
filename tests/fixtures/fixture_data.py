import pytest


@pytest.fixture
def disapproved_post():
    from posts.models import Post
    return Post.objects.create(title='Title for test post1', url='http://example.net/test-url/', language='RU')


@pytest.fixture
def approved_post():
    from posts.models import Post
    return Post.objects.create(title='Title for test post2', url='http://example.net/test/url/', language='RU', approved=True)



@pytest.fixture
def group1():
    from posts.models import Group
    return Group.objects.create(title='Test group1', slug='test-group-1')


@pytest.fixture
def group2():
    from posts.models import Group
    return Group.objects.create(title='Testgroup2', slug='testgroup2')


@pytest.fixture
def post1():
    from posts.models import Post
    return Post.objects.create(title='Title for test post1', url='http://example.net/test/1', language='RU', approved=True)


@pytest.fixture()
def post2():
    from posts.models import Post
    return Post.objects.create(title='Title for test post2', url='http://example.net/test/url/2', language='EN', approved=True)
