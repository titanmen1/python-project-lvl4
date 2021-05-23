from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from .models import Status, Label, Task, User

USERNAME = 'test_user'
PASSWORD = 'Efwefwef1223'

STATUS_DATA = {'name': 'Новая'}
LABEL_DATA = {'name': 'new_label'}

# task form fields:
TASK_NAME, TASK_DESCRIPTION, TASK_STATUS, TASK_EXECUTOR, TASK_AUTHOR, TASK_LABELS = (  # noqa: E501
    'name', 'description', 'status', 'executor', 'author', 'label'
)

# def get_test_data():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     with open(os.path.join(current_dir, 'fixtures', 'test_data.json'), 'r') as file:
#         content = file.read()
#     return json.loads(content)


def create_user(is_staff):
    User.objects.create_user(username=USERNAME, password=PASSWORD)
    user = User.objects.get(username=USERNAME)
    user.is_staff = is_staff
    user.save()
    return user


def prepare_db(staff_user=False):
    Status.objects.create(name=STATUS_DATA['name'])
    Label.objects.create(name=LABEL_DATA['name'])
    status = Status.objects.get(name=STATUS_DATA['name'])
    label = Label.objects.get(name=LABEL_DATA['name'])
    user = create_user(is_staff=staff_user)
    return status, label, user


def create_and_get_task():
    Task.objects.create(name='test_task',
                        description='description',
                        status=Status.objects.get(name=STATUS_DATA['name']),
                        author=User.objects.get(username=USERNAME),
                        executor=User.objects.get(username=USERNAME)
                        )
    return Task.objects.get(name='test_task')


def create_task_data(status, label, user):
    task_data = {
        TASK_NAME: 'task_1',
        TASK_DESCRIPTION: 'description',
        TASK_STATUS: status.pk,
        TASK_EXECUTOR: user.pk,
        TASK_AUTHOR: user.pk,
        TASK_LABELS: [label.pk],
    }
    return task_data


class TestRegisterAndLogin(TestCase):

    # User can register in system
    def test_register(self):
        client = Client()
        response = client.post(reverse('create'), {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'username': USERNAME,
            'password1': PASSWORD,
            'password2': PASSWORD
        }, follow=True)
        user_in_db = User.objects.get(username=USERNAME)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(USERNAME, user_in_db.username)

    # Registered user can login
    def test_login(self):
        client = Client()
        User.objects.create_user(username=USERNAME, password=PASSWORD)
        response = client.post(reverse('login'), {'username': USERNAME,
                                                  'password': PASSWORD
                                                  }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)


class TestStatusCRUD(TestCase):

    # Authenticated staff user can create statuses
    def test_create_status(self):
        client = Client()
        user = create_user(is_staff=True)
        client.force_login(user)
        response = client.post(reverse('create_status'), STATUS_DATA)
        status_in_db = Status.objects.get(name=STATUS_DATA['name'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(STATUS_DATA['name'], status_in_db.name)

    # Authenticated staff user can update statuses
    def test_update_status(self):
        client = Client()
        user = create_user(is_staff=True)
        client.force_login(user)
        Status.objects.create(name='old_name')
        old_status = Status.objects.get(name='old_name')
        status_url = reverse('update_status', args=[str(old_status.pk)])
        response = client.post(status_url, STATUS_DATA)
        status_in_db = Status.objects.get(pk=old_status.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(STATUS_DATA['name'], status_in_db.name)

    # Authenticated staff user can delete statuses
    def test_delete_status(self):
        client = Client()
        user = create_user(is_staff=True)
        client.force_login(user)
        Status.objects.create(name='old_name')
        old_status = Status.objects.get(name='old_name')
        status_delete_url = reverse('delete_status', args=[str(old_status.pk)])
        response = client.post(status_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Status.objects.all()), 0)


class TestLabelCRUD(TestCase):

    # Any authenticated user can create tags
    def test_create_label(self):
        client = Client()
        user = create_user(is_staff=False)
        client.force_login(user)
        response = client.post(reverse('create_label'), LABEL_DATA)
        label_in_db = Label.objects.get(name=LABEL_DATA['name'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LABEL_DATA['name'], label_in_db.name)

    # Any authenticated user can update tags
    def test_update_label(self):
        client = Client()
        user = create_user(is_staff=False)
        client.force_login(user)
        Label.objects.create(name='old_name')
        old_label = Label.objects.get(name='old_name')
        label_update_url = reverse('update_label', args=[str(old_label.pk)])
        response = client.post(label_update_url, LABEL_DATA)
        label_in_db = Label.objects.get(pk=old_label.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LABEL_DATA['name'], label_in_db.name)

    # Any authenticated user can delete tags
    def test_delete_label(self):
        client = Client()
        user = create_user(is_staff=False)
        client.force_login(user)
        Label.objects.create(name='old_name')
        old_label = Label.objects.get(name='old_name')
        label_delete_url = reverse('delete_label', args=[str(old_label.pk)])
        response = client.post(label_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Label.objects.all()), 0)


class TestTaskCRUD(TestCase):

    # Any authenticated user can create tasks
    def test_create_task(self):
        client = Client()
        status, label, user = prepare_db()
        task_data = create_task_data(status, label, user)
        client.force_login(user)
        response = client.post(reverse('create_task'), task_data)
        task_in_db = Task.objects.get(name=task_data[TASK_NAME])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(task_data[TASK_NAME], task_in_db.name)

    # Any authenticated user can update tasks
    def test_update_task(self):
        client = Client()
        status, label, user = prepare_db()
        client.force_login(user)
        old_task = create_and_get_task()
        task_update_data = create_task_data(status, label, user)
        task_url = reverse('update_task', args=[str(old_task.pk)])
        response = client.post(task_url, task_update_data)
        task_in_db = Task.objects.get(pk=old_task.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(task_update_data[TASK_NAME], task_in_db.name)

    # Any authenticated user can delete tasks
    def test_delete_task(self):
        client = Client()
        status, label, user = prepare_db()
        client.force_login(user)
        task = create_and_get_task()
        task_delete_url = reverse('delete_task', args=[str(task.pk)])
        response = client.post(task_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Task.objects.all()), 0)


class URLSTests(TestCase):

    #  All resources are available for the authenticated staff user
    def test_200_ok(self):
        client = Client()
        status, label, user = prepare_db(staff_user=True)
        client.force_login(user)
        # task = create_and_get_task()
        urls_200_ok = (
            reverse('tasks'), reverse('statuses'), reverse('labels'),
            reverse('create_task'), reverse('create_label'), reverse('login'), reverse('create'),
        )
        for url in urls_200_ok:
            response = client.get(url)
            self.assertEqual(response.status_code, 200)
