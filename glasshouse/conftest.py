import pytest
import glasshouse

# ovewriting the default test db settings since we use postgres
@pytest.fixture(scope='session')
def django_db_setup():
    glasshouse.settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgres',
        'HOST': 'localhost',
        'NAME': 'postgres',
}
