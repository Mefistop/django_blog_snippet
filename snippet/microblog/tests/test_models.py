from django.test import TestCase
from microblog.models import User, Profile, Blog, Comment

class ProfileModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='Ivan', password='qwerty123456')

    def test_create_user(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'Ivan')

    def test_create_profile(self):
        profile = Profile.objects.get(id=1)
        self.assertIsNotNone(profile)

    def test_bio_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertEqual(field_label, 'bio')

    def test_is_blogger_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('is_blogger').verbose_name
        self.assertEqual(field_label, 'is blogger')

    def test_user_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_profile_field_is_blogger(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.is_blogger, False)

    def test_profile_object_name_not_blogger(self):
        profile = Profile.objects.get(id=1)
        expected_object_name = f'User {profile.user.username}'
        self.assertEqual(expected_object_name, str(profile))

    def test_profile_object_name_blogger(self):
        profile = Profile.objects.get(id=1)
        profile.is_blogger = True
        expected_object_name = f'Blogger {profile.user.username}'
        self.assertEqual(expected_object_name, str(profile))


class BlogModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='Ivan', password='qwerty123456')
        profile = Profile.objects.get(id=1)
        profile.is_blogger = True
        Blog.objects.create(author=profile, title='New blog', content='Very interesting text.')

    def test_create_blog(self):
        blog = Blog.objects.get(id=1)
        self.assertIsNotNone(blog)

    def test_author_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_created_at_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_content_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')

    def test_is_archived_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('is_archived').verbose_name
        self.assertEqual(field_label, 'is archived')

    def test_title_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_field_is_archived(self):
        blog = Blog.objects.get(id=1)
        self.assertEqual(blog.is_archived, False)

    def test_blog_object_name(self):
        blog = Blog.objects.get(id=1)
        expected_object_name = f'Blog "{blog.title}" by {blog.author.user.username}'
        self.assertEqual(expected_object_name, str(blog))


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='Ivan', password='qwerty123456')
        profile = Profile.objects.get(id=1)
        profile.is_blogger = True
        blog = Blog.objects.create(author=profile, title='New blog', content='Very interesting text.')
        Comment.objects.create(author=profile, blog=blog, content='My first comment')

    def test_create_comment(self):
        comment = Comment.objects.get(id=1)
        self.assertIsNotNone(comment)

    def test_author_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_blog_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('blog').verbose_name
        self.assertEqual(field_label, 'blog')

    def test_content_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')

    def test_is_archive_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('is_archived').verbose_name
        self.assertEqual(field_label, 'is archived')

    def test_field_is_archived(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.is_archived, False)

    def test_Comment_object_name(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = f"Comment to blog with title '{comment.blog.title}' by {comment.author.user.username}"
        self.assertEqual(expected_object_name, str(comment))