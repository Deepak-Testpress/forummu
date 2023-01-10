from django.test import TestCase
from django.urls import reverse, resolve
from board.views import home, board_topics, new_topic
from board.models import Board, Topic, Post
from django.contrib.auth.models import User
from board.views import edit_post
from board.forms import NewPostForm
from board.views import topic_posts


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(
            name="Django", description="Django board."
        )
        url = reverse("home")
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve("/home/")
        self.assertEquals(view.func, home)


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name="Django", description="Django board.")

    def test_board_topics_view_success_status_code(self):
        url = reverse("board_topics", kwargs={"board_id": 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse("board_topics", kwargs={"board_id": 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve("/boards/1/topics")
        self.assertEquals(view.func, board_topics)


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name="Django", description="Django board.")
        self.username = "john"
        self.password = "123"
        User.objects.create_user(
            username=self.username,
            email="john@doe.com",
            password=self.password,
        )
        self.client.login(username=self.username, password=self.password)

    def test_new_topic_view_redirect_status_code(self):
        url = reverse("new_topic", kwargs={"board_id": 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):  #%
        url = reverse("new_topic", kwargs={"board_id": 999})
        self.client.login()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve("/boards/1/new/")
        self.assertEquals(view.func, new_topic)

    def test_new_topic_invalid_post_data(self):

        url = reverse("new_topic", kwargs={"board_id": 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)


class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(
            name="Django", description="Django board."
        )
        self.username = "john"
        self.password = "123"
        user = User.objects.create_user(
            username=self.username,
            email="john@doe.com",
            password=self.password,
        )
        self.topic = Topic.objects.create(
            subject="Hello, world", board=self.board, starter=user
        )
        self.post = Post.objects.create(
            message="Lorem ipsum dolor sit amet",
            topic=self.topic,
            created_by=user,
        )
        self.url = reverse(
            "edit_post",
            kwargs={
                "board_id": self.board.id,
                "topic_id": self.topic.id,
                "post_id": self.post.id,
            },
        )


class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    def test_redirection(self):

        login_url = reverse("login")
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            "{login_url}?next={url}".format(login_url=login_url, url=self.url),
        )


class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):

        super().setUp()
        username = "jane"
        password = "321"
        user = User.objects.create_user(
            username=username, email="jane@doe.com", password=password
        )
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.client.get(self.url)
        self.assertEqual(self.response.status_code, 404)


class PostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve("/boards/1/topics/1/posts/1/edit")
        self.assertEquals(view.func, edit_post)

    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, NewPostForm)

    def test_form_inputs(self):
        """
        The view must contain two inputs: csrf, message textarea
        """
        self.assertContains(self.response, "<input", 1)
        self.assertContains(self.response, "<textarea", 1)


class SuccessfulPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(
            self.url, {"message": "edited message"}
        )

    def test_redirection(self):
        topic_posts_url = reverse(
            "topic_posts",
            kwargs={"board_id": self.board.id, "topic_id": self.topic.id},
        )
        self.assertRedirects(self.response, topic_posts_url)

    def test_post_changed(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.message, "edited message")


class InvalidPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 302)


class TopicPostsTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django', description='Django board.')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        topic = Topic.objects.create(subject='Hello, world', board=board, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'board_id': board.id, 'topic_id': topic.id})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEquals(view.func, topic_posts )