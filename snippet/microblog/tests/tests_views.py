from django.test import TestCase
from microblog.models import User, Profile, Blog, Comment
from django.urls import reverse

class BlogViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='Ivan-blogger', password='qwerty123456')
        profile = Profile.objects.get(id=1)
        profile.is_blogger = True
        profile.save()
        User.objects.create_user(username='Petr', password='asdfg15092421')
        number_of_blogs = 8
        for num in range(number_of_blogs):
            Blog.objects.create(
                author=profile,
                title=f'New blog by {num}',
                content=f'Very interesting text.I write it {num}',
            )
    def test_view_url_blog_list_exists_at_desired_location(self):
        resp = self.client.get("/blog/blogs/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_blog_list_accessible_by_name(self):
        resp = self.client.get(reverse('microblog:blog-list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('microblog:blog-list'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'microblog/blog_list.html')

    def test_pagination_is_five(self):
        resp = self.client.get(reverse('microblog:blog-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['blog_list']) == 5)

    def test_lists_all_blogs(self):
        resp = self.client.get(reverse('microblog:blog-list') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['blog_list']) == 3)

    def test_access_to_create_blog_login_user_is_blogger(self):
        login = self.client.login(username='Ivan-blogger', password='qwerty123456')
        resp = self.client.get(reverse('microblog:blog-create'))
        self.assertEqual(str(resp.context['user']), 'Ivan-blogger')
        self.assertEqual(resp.status_code, 200)

    def test_access_to_create_blog_login_user_is_not_blogger(self):
        login = self.client.login(username='Petr', password='asdfg15092421')
        resp = self.client.get(reverse('microblog:blog-create'))
        self.assertEqual(resp.status_code, 403)

    def test_access_to_create_blog_no_login_user(self):
        resp = self.client.get(reverse('microblog:blog-create'))
        self.assertEqual(resp.status_code, 302)

    def test_view_url_blog_detail_exists_at_desired_location(self):
        resp = self.client.get("/blog/blogs/1")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_blog_detail_accessible_by_name(self):
        resp = self.client.get(reverse('microblog:blog-detail', kwargs={'pk':1}))
        self.assertEqual(resp.status_code, 200)

    def test_view_blog_detail_correct_template(self):
        resp = self.client.get(reverse('microblog:blog-detail', kwargs={'pk':1}))
        self.assertTemplateUsed(resp, 'microblog/blog_detail.html')

    def test_view_detail_access_to_update_login_user_with_access(self):
        login = self.client.login(username='Ivan-blogger', password='qwerty123456')
        resp = self.client.get(reverse('microblog:blog-update', kwargs={'pk':1}))
        self.assertEqual(resp.status_code, 200)

    def test_view_detail_access_to_update_login_user_without_access(self):
        login = self.client.login(username='Petr', password='asdfg15092421')
        resp = self.client.get(reverse('microblog:blog-update', kwargs={'pk':1}))
        self.assertEqual(resp.status_code, 403)

    def test_view_detail_access_to_delete_login_user_with_access(self):
        login = self.client.login(username='Ivan-blogger', password='qwerty123456')
        resp = self.client.get(reverse('microblog:blog-delete', kwargs={'pk':1}))
        self.assertEqual(resp.status_code, 200)

    def test_view_detail_access_to_delete_login_user_without_access(self):
        login = self.client.login(username='Petr', password='asdfg15092421')
        resp = self.client.get(reverse('microblog:blog-delete', kwargs={'pk':1}))
        self.assertEqual(resp.status_code, 403)

    def test_to_update_blog(self):
        login = self.client.login(username='Ivan-blogger', password='qwerty123456')
        resp = self.client.post(
            reverse('microblog:blog-update', kwargs={'pk':1}),
            {'title': 'New blog by one', 'content':'Very interesting text.I write it'}
        )
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(reverse('microblog:blog-update', kwargs={'pk': 1}))
        self.assertEqual(resp.context['object'].title, 'New blog by one')

    def test_to_delete_blog(self):
        login = self.client.login(username='Ivan-blogger', password='qwerty123456')
        resp = self.client.delete(
            reverse('microblog:blog-delete', kwargs={'pk':1}),
            {'pk': 1}
        )
        resp = self.client.get(reverse('microblog:blog-detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 404)


class BloggerViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        username = 'Bloger N'
        password = 'qwerty12345'
        blogger_num = 10
        for blogger in range(blogger_num):
            user = User.objects.create_user(username=username+f'{blogger}', password=password)
            profile = user.profile
            profile.is_blogger = True
            profile.save()

    def test_view_url_blogger_list_exists_at_desired_location(self):
        resp = self.client.get("/blog/bloggers/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_blogger_list_accessible_by_name(self):
        resp = self.client.get(reverse('microblog:blogger-list'))
        self.assertEqual(resp.status_code, 200)

    def test_uses_correct_templates(self):
        resp = self.client.get(reverse('microblog:blogger-list'))
        self.assertTemplateUsed(resp, 'microblog/profile_list.html')

    def test_view_correct_count_bloggers(self):
        resp = self.client.get(reverse('microblog:blogger-list'))
        self.assertEqual(len(resp.context['object_list']), 10)

    def test_view_url_blogger_detail_exists_at_desired_location(self):
        resp = self.client.get("/blog/bloggers/1")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_detail_list_accessible_by_name(self):
        resp = self.client.get(reverse('microblog:blogger-detail', kwargs={'pk':1}))
        self.assertEqual(resp.status_code, 200)


class CommentViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.blogger = User.objects.create_user(username='Ivan-blogger', password='qwerty123456')
        profile = Profile.objects.get(id=1)
        profile.is_blogger = True
        profile.save()
        User.objects.create_user(username='Petr-user', password='asdfg15092421')
        Blog.objects.create(title="New bog", author=profile, content='My very popular blog')

    def test_view_url_create_comment_exists_at_desired_location(self):
        login = self.client.login(username='Ivan-blogger', password='qwerty123456')
        resp = self.client.get("/blog/blogs/1/create_comment")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_create_comment_accessible_by_name(self):
        login = self.client.login(username='Ivan-blogger', password='qwerty123456')
        resp = self.client.get(reverse('microblog:comment-create', kwargs={'pk':1}))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_create_comment_not_logging_user(self):
        resp = self.client.get(reverse('microblog:comment-create', kwargs={'pk':1}))
        self.assertEqual(resp.status_code, 302)

    def test_view_url_create_comment_logging_user_blogger(self):
        login = self.client.login(username='Ivan-blogger', password='qwerty123456')
        resp = self.client.get(reverse('microblog:comment-create', kwargs={'pk':1}))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_create_comment_logging_user_not_blogger(self):
        login = self.client.login(username='Petr-user', password='asdfg15092421')
        resp = self.client.get(reverse('microblog:comment-create', kwargs={'pk':1}))
        self.assertEqual(resp.status_code, 200)

    def test_create_comment_user_is_blogger(self):
        login = self.client.login(username='Ivan-blogger', password='qwerty123456')
        resp = self.client.post(reverse('microblog:comment-create', kwargs={'pk':1}), {"content":'My first comment'})
        self.assertEqual(resp.status_code, 302)
        resp_with_comment = self.client.get(reverse('microblog:blog-detail', kwargs={'pk':1}))
        blog = resp_with_comment.context['object']
        comment = blog.comments.all()
        self.assertEqual(len(comment), 1)

    def test_create_comment_user_is_not_blogger(self):
        login = self.client.login(username='Petr-user', password='asdfg15092421')
        resp = self.client.post(reverse('microblog:comment-create', kwargs={'pk':1}), {"content":'My first comment'})
        self.assertEqual(resp.status_code, 302)
        resp_with_comment = self.client.get(reverse('microblog:blog-detail', kwargs={'pk':1}))
        blog = resp_with_comment.context['object']
        comment = blog.comments.all()
        self.assertEqual(len(comment), 1)