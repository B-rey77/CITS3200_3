from django.test import TestCase
from rest_framework.test import APITestCase
from database.models import Users  
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIRequestFactory
from django.utils.encoding import force_bytes
from database.tokens import account_activation_token


# Create your tests here.
class TestModel(APITestCase):
	def setUp(self):
		self.test_user = Users.objects.create_user(email='test@gmail.com', first_name='Test fname', last_name='Test lname', password='password123')
		self.test_superuser = Users.objects.create_superuser(email='super@gmail.com', first_name='Test fname', last_name='Test lname', password='password123')

	def test_creates_user(self):
		self.assertIsInstance(self.test_user, Users)
		self.assertFalse(self.test_user.is_superuser)
		self.assertEqual(self.test_user.email, 'test@gmail.com')
  
	def test_creates_super_user(self):
		self.assertIsInstance(self.test_superuser, Users)
		self.assertTrue(self.test_superuser.is_superuser)
		self.assertEqual(self.test_superuser.email, 'super@gmail.com')
  
	def test_raises_error_when_email_is_not_supplied(self):
		self.assertRaises(ValueError, Users.objects.create_user, email='', first_name='Test fname', last_name='Test lname', password='password123')
	
	def test_raises_error_when_superuser_is_not_superuser(self):
		with self.assertRaisesMessage(ValueError, 'Superuser must be assigned to is_superuser=True'):
  			Users.objects.create_superuser(email='super@gmail.com', first_name='Test fname', last_name='Test lname', password='password123', is_superuser=False)
 
	def test_raises_error_with_message_when_email_is_not_supplied(self):
		with self.assertRaisesMessage(ValueError, 'You must provide an email address'):
			Users.objects.create_user(email='', first_name='Test fname', last_name='Test lname', password='password123')

	def test_user_str(self):
		self.assertEqual(str(self.test_user.email), 'test@gmail.com')
  
	def test_superuser_has_superuser_permissions(self):
		self.assertTrue(self.test_superuser.has_perm)
  
	def test_superuser_has_superuser_module_perms(self):
		self.assertTrue(self.test_superuser.has_module_perms)
  

class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('signup')
        self.login_url=reverse('login')
        self.factory = APIRequestFactory()
        self.test_user={
            'email':'testemail@gmail.com',
            'first_name':'testfname',
            'last_name':'testlname',
            'password1':'password',
            'password2':'password'
        }
        self.test_user_short_password={
            'email':'testemail@gmail.com',
            'first_name':'testfname',
            'last_name':'testlname',
            'password1':'tes',
            'password2':'tes'
        }
        self.test_user_unmatching_password={
            'email':'testemail@gmail.com',
            'first_name':'testfname',
            'last_name':'testlname',
            'password1':'teslatt',
            'password2':'teslatto'
        }
        self.test_user_invalid_email={
            'email':'test.com',
            'first_name':'testfname',
            'last_name':'testlname',
            'password1':'teslatt',
            'password2':'teslatto'
        }
        return super().setUp()

class RegisterTest(BaseTest):
	def test_can_view_page_correctly(self):
		response=self.client.get(self.register_url)
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'database/signup.html')

	def test_can_register_user(self):
		response=self.client.post(self.register_url,self.test_user,format='text/html')
		self.assertEqual(response.status_code,200)

	def test_cant_register_user_withshortpassword(self):
		response=self.client.post(self.register_url,self.test_user_short_password,format='text/html')
		self.assertEqual(response.status_code,200)

	def test_cant_register_user_with_unmatching_passwords(self):
		response=self.client.post(self.register_url,self.test_user_unmatching_password,format='text/html')
		self.assertEqual(response.status_code,200)

	def test_cant_register_user_with_invalid_email(self):
		response=self.client.post(self.register_url,self.test_user_invalid_email,format='text/html')
		self.assertEqual(response.status_code, 200)

	def test_cant_register_user_with_taken_email(self):
		self.client.post(self.register_url,self.test_user,format='text/html')
		response=self.client.post(self.register_url,self.test_user,format='text/html')
		self.assertEqual(response.status_code, 200)


class LoginTest(BaseTest):
	def test_can_access_page(self):
		response=self.client.get(self.login_url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'database/login.html')

	def test_login_success(self):
		self.client.post(self.register_url,self.test_user,format='text/html')
		response = self.client.post(self.login_url,self.test_user,format='text/html')
		self.assertEqual(response.status_code, 200)

	def test_user_authenticated_redirected_to_profile(self):
		self.client.post(self.register_url,self.test_user,format='text/html')
		
		response_login = self.client.post('/login', {'email': self.test_user['email'], 'password1': self.test_user['password2']})
		self.assertTrue(response_login)

		response = self.client.get('/login')
		self.assertEqual(response.status_code, 301)
		
	def test_cant_login_with_no_email(self):
		response = self.client.post(self.login_url, {'email':'', 'password': self.test_user['password1']}, format='text/html')
		message = list(response.context['messages'])
		self.assertEqual(str(message[0]), 'Email OR Password is incorrect')
		

	def test_user_is_logged_out_permanently(self):
		self.client.post(self.register_url,self.test_user,format='text/html')
		response = self.client.get('/logout')
		self.assertEqual(response.status_code, 301)
	

class UserVerifyTest(BaseTest):
	def test_user_activates_success(self):
		user = Users.objects.create_user(
			email='test@gmail.com', 
			first_name='Test fname', 
			last_name='Test lname', 
			password='password123')
		user.set_password('tetetebvghhhhj')
		user.is_active=False
		user.save()
		uid=urlsafe_base64_encode(force_bytes(user.pk))
		token=account_activation_token.make_token(user)
		response=self.client.get(reverse('activate', kwargs={'uidb64':uid,'token':token}))
		self.assertEqual(response.status_code, 302)
		user=Users.objects.get(email='test@gmail.com')
		self.assertTrue(user.is_active)


class PasswordResetTests(BaseTest):
	def setUp(self):
		self.pword_reset_url=reverse('password_reset')
		self.test_user = Users.objects.create_user(
			email='test@gmail.com', 
			first_name='Test fname', 
			last_name='Test lname', 
			password='password123')

	def test_user_can_view_passwordreset_page_correctly(self):
		response=self.client.get(self.pword_reset_url)
		self.assertEqual(response.status_code, 200)

	def test_user_can_post_passwordreset_form(self):
		response=self.client.post(self.pword_reset_url,{'email':self.test_user.email},format='text/html')
		self.assertEqual(response.status_code, 302)

class EditProfileTests(BaseTest):
	def setUp(self):
		self.editprofile_url=reverse('edit_profile_page')
		self.test_user = Users.objects.create_user(
			email='test@gmail.com', 
			first_name='Test fname', 
			last_name='Test lname',
			profession='',
			institution='',
			country='',
			password='password123')

	def test_user_can_view_edit_profile_page_correctly(self):
		self.client.force_login(self.test_user)
		response=self.client.get(self.editprofile_url)
		self.assertEqual(response.status_code, 200)

	def test_user_can_post_editprofile_form(self):
		self.client.force_login(self.test_user)
		response=self.client.post(self.editprofile_url,{
			'email':self.test_user.email, 
			'first_name':self.test_user.first_name, 
			'last_name':'Chgd lname',
			'profession':'Student',
			'institution':'',
			'country':'Australia'},
			format='text/html')
		self.assertEqual(response.status_code, 302)

