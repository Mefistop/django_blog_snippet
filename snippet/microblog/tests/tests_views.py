from django.test import TestCase
from microblog.models import User, Profile, Blog, Comment
from django.urls import reverse

class BlogViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='Ivan', password='qwerty123456')
        number_of_blogs = 8
        for num in range(number_of_blogs):
            User.objects.create(username=num, password=f'qwerty123456{num}')
            profile = Profile.objects.get(id=1)
            profile.is_blogger = True
            Blog.objects.create(
                author=profile,
                title=f'New blog by {num}',
                content=f'Very interesting text.I write it {num}',
            )
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/blog/blogs/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('microblog:blog-list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('microblog:blog-list'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'microblog/blog_list.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('microblog:blog-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['blog_list']) == 5)

    def test_lists_all_authors(self):
        resp = self.client.get(reverse('microblog:blog-list') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['blog_list']) == 3)

    def test_access_login_user(self):
        profile = Profile.objects.get(id=1)
        profile.is_blogger = True
        profile.save()
        login = self.client.login(username='Ivan', password='qwerty123456')
        resp = self.client.get(reverse('microblog:blog-create'))
        self.assertEqual(str(resp.context['user']), 'Ivan')
        self.assertEqual(resp.status_code, 200)

    def test_access_login_user_is_not_blogger(self):
        login = self.client.login(username='Ivan', password='qwerty123456')
        resp = self.client.get(reverse('microblog:blog-create'))
        self.assertEqual(resp.status_code, 403)

    def test_access_no_login_user(self):
        resp = self.client.get(reverse('microblog:blog-create'))
        self.assertEqual(resp.status_code, 302)