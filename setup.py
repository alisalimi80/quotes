from os import walk, environ, sep
from os.path import basename, exists
from django import setup
from logging import getLogger
from django.conf import settings
from subprocess import run, STDOUT, PIPE
from traceback import format_exc

environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
setup()




class SetUp:
    def __init__(self):
        self.name_of_apps_in_base_dir = []
        self.name_of_installed_apps_in_base_dir = []
        self.name_of_installed_apps_which_have_migrations = []

    def perform(self):
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ perform')
        self._get_name_of_apps_in_base_dir()
        self._get_name_of_installed_app_in_base()
        self._make_migrations_for_each_app()
        self._make_migrations()
        self._get_name_of_apps_which_have_migrations()
        self._do_migrate_for_each_app()
        self._do_migrate()
        self._create_super_user()
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ perform is finished.')

    def _get_name_of_apps_in_base_dir(self):
        print('----------------------------------------------------------------- _get_name_of_apps_in_base_dir')
        
        for root, dirs, files in walk(settings.BASE_DIR_STR, topdown=False):
            if 'site-packages' not in root:
                if 'apps.py' in files:
                    self.name_of_apps_in_base_dir.append(basename(root))

    def _get_name_of_installed_app_in_base(self):
        print('------------------------------------------------------------ _get_name_of_installed_app_in_base')
        
        for name_of_app in settings.INSTALLED_APPS:
            if name_of_app in self.name_of_apps_in_base_dir:
                self.name_of_installed_apps_in_base_dir.append(name_of_app)

    def _make_migrations_for_each_app(self):
        print('------------------------------------------------------------------ _make_migrations_for_each_app')
        
        for name_of_app in self.name_of_installed_apps_in_base_dir:
            self._run_command(['python',
                               f'{settings.BASE_DIR_STR}/manage.py',
                               'makemigrations',
                               f'{name_of_app}',
                               '--no-input'])

    def _make_migrations(self):
        print('------------------------------------------------------------------------------ _make_migrations')
        
        self._run_command(['python',
                           f'{settings.BASE_DIR_STR}/manage.py',
                           'makemigrations',
                           '--no-input'])

    def _get_name_of_apps_which_have_migrations(self):
        print('-------------------------------------------------------- _get_name_of_apps_which_have_migrations')
        
        for name_of_app in self.name_of_installed_apps_in_base_dir:
            if exists(f"{settings.BASE_DIR_STR}{sep}{name_of_app}{sep}migrations"):
                self.name_of_installed_apps_which_have_migrations.append(name_of_app)

    def _do_migrate_for_each_app(self):
        print('----------------------------------------------------------------------- _do_migrate_for_each_app')
        
        for name_of_app in self.name_of_installed_apps_which_have_migrations:
            self._run_command(['python',
                               f'{settings.BASE_DIR_STR}/manage.py',
                               'migrate',
                               f'{name_of_app}',
                               '--no-input'])  #

    def _do_migrate(self):
        print('----------------------------------------------------------------------------------- _do_migrate')
        
        self._run_command(['python',
                           f'{settings.BASE_DIR_STR}/manage.py',
                           'migrate',
                           '--no-input'])

    @staticmethod
    def _create_super_user():
        print('-----------------------------------------------------------------------------------')
        from django.contrib.auth.models import User

        try:
            u = User(username='admin')
            u.set_password('12345678910')
            u.is_superuser = True
            u.is_staff = True
            u.save()
        except Exception:
            print(format_exc())

    @staticmethod
    def _run_command(command, raise_error=True):
        completed_process = run(command,
                                shell=False,
                                # capture_output=True,
                                text=True,
                                stdout=PIPE,
                                stderr=STDOUT)

        if raise_error:
            completed_process.check_returncode()

if __name__ == "__main__":
    my_setup = SetUp()
    my_setup.perform()
