from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.title


class Post(models.Model):
    LANGUAGE_DICT = [('RU', 'Русский'), ('EN', 'English')]
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    url = models.URLField(unique=True, verbose_name="Ссылка")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True, db_index=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE,
    #                            related_name="author_posts",
    #                            verbose_name="Пользователь")
    # saving this for future
    group = models.ManyToManyField(Group, related_name="tags_posts", blank=True,
                                   verbose_name="Тэги")
    language = models.CharField(max_length=2, choices=LANGUAGE_DICT, verbose_name="Язык")
    approved = models.BooleanField(default=False, verbose_name="Одобрено модератором")

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title
