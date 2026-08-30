from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Category, MenuItem


class LittleLemonAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.manager_group, _ = Group.objects.get_or_create(name='Managers')
        self.delivery_group, _ = Group.objects.get_or_create(name='Delivery crew')

        self.customer = User.objects.create_user(username='customer', password='testpass123')
        self.manager = User.objects.create_user(username='manager', password='testpass123')
        self.manager.groups.add(self.manager_group)

    def test_menu_items_list_returns_200_for_authenticated_user(self):
        category = Category.objects.create(slug='drinks', title='Drinks')
        MenuItem.objects.create(title='Lemonade', price='3.50', featured=False, category=category)

        self.client.force_authenticate(user=self.customer)
        response = self.client.get('/api/menu-items')

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json().get('results', response.json())), 1)

    def test_manager_can_assign_user_to_manager_group(self):
        user_to_assign = User.objects.create_user(username='new-manager', password='testpass123')

        self.client.force_authenticate(user=self.manager)
        response = self.client.post('/api/groups/manager/users', {'username': 'new-manager'}, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.manager_group.user_set.filter(username='new-manager').exists())

    def test_admin_can_create_category_and_menu_item(self):
        admin = User.objects.create_superuser(username='admin', password='adminpass123', email='admin@example.com')
        self.client.force_authenticate(user=admin)

        category_response = self.client.post('/api/categories', {'slug': 'desserts', 'title': 'Desserts'}, format='json')
        self.assertEqual(category_response.status_code, 201)

        category_id = category_response.json()['id']
        menu_response = self.client.post('/api/menu-items', {
            'title': 'Ice Cream',
            'price': '4.50',
            'featured': True,
            'category': category_id,
        }, format='json')

        self.assertEqual(menu_response.status_code, 201)
        self.assertEqual(menu_response.json()['title'], 'Ice Cream')

    def test_manager_can_update_featured_flag_and_customer_can_order(self):
        category = Category.objects.create(slug='desserts', title='Desserts')
        menu_item = MenuItem.objects.create(title='Ice Cream', price='4.50', featured=False, category=category)

        self.client.force_authenticate(user=self.manager)
        patch_response = self.client.patch(f'/api/menu-items/{menu_item.id}', {'featured': True}, format='json')
        self.assertEqual(patch_response.status_code, 200)
        self.assertTrue(patch_response.json()['featured'])

        self.client.force_authenticate(user=self.customer)
        cart_response = self.client.post('/api/cart/menu-items', {'menu_item_id': menu_item.id, 'quantity': 2}, format='json')
        self.assertEqual(cart_response.status_code, 201)

        order_response = self.client.post('/api/cart/orders', {'date': '2026-08-30'}, format='json')
        self.assertEqual(order_response.status_code, 201)
        self.assertIn('total', order_response.json())

    def test_auth_routes_and_menu_pagination_match_rubric(self):
        category = Category.objects.create(slug='drinks', title='Drinks')
        MenuItem.objects.create(title='Lemonade', price='3.50', featured=False, category=category)
        MenuItem.objects.create(title='Espresso', price='2.50', featured=False, category=category)

        self.client.force_authenticate(user=self.customer)
        response = self.client.get('/api/menu-items?ordering=-price&page=1')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json().get('results', response.json())), 1)

        token_response = self.client.post('/auth/token/login/', {'username': 'customer', 'password': 'testpass123'}, format='json')
        self.assertEqual(token_response.status_code, 200)
