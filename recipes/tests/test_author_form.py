from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized
    def test_first_nome_placeholder_is_correct(self):
        form = RegisterForm()
        placeholder = form['first_name'].field.widget.attrs['placeholder']
        self.assertEqual('Ex.: John', placeholder)