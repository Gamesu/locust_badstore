from locust import HttpUser, TaskSet, task, between
from colorama import Fore, Back, Style
import time

class UserBehavior(TaskSet):

    def on_start(self):
        # Inicio de las pruebas siempre cargando la página principal y haciendo login
        print(f'{Back.MAGENTA + Fore.WHITE} --- Create User {self.user} --- {Style. RESET_ALL}')
        self.is_logged_in = False
        self.load_homepage()

    @task(4)
    def load_homepage(self):
        response = self.client.get("/cgi-bin/badstore.cgi")
        if response.status_code == 200:
            print(f"{'HOME':12} {Back.LIGHTCYAN_EX + Fore.BLUE} Load {Style. RESET_ALL}")
            self.login()  # Después de la página principal, ir al login
        else:
            print(f'{'HOME':12} {Back.LIGHTRED_EX + Fore.WHITE} Error {Style. RESET_ALL}')

    #@task(1)
    def login(self):
        response = self.client.post("/cgi-bin/badstore.cgi?action=loginregister", data={"email": "AAA_Test_User", "passwd": "test", "Login": "Login"})
        if response.status_code == 200:
            print(f'{'LOGIN':12} {Back.LIGHTCYAN_EX + Fore.BLUE} Load {Style. RESET_ALL}')
            if 'Welcome' in response.text:
                print(f'{'LOGIN USER':12} {Back.LIGHTMAGENTA_EX + Fore.WHITE} Login {Style. RESET_ALL}')
                self.is_logged_in = True  # Marcar como autenticado
            else:
                print(f'{'LOGIN USER':12} {Back.LIGHTYELLOW_EX + Fore.BLACK} Error login user {Style. RESET_ALL}')
        else:
            print(f'{'LOGIN':12} {Back.LIGHTRED_EX + Fore.WHITE} Error {Style. RESET_ALL}')
        # Después del login, las siguientes tareas serán seleccionadas aleatoriamente

    @task(2)
    def myaccount(self):
        response = self.client.get("/cgi-bin/badstore.cgi?action=myaccount")
        if response.status_code == 200:
            print(f"{'ACCOUNT':12} {Back.LIGHTCYAN_EX + Fore.BLUE} Load {Style. RESET_ALL}")
        else:
            print(f'{'ACCOUNT':12} {Back.LIGHTRED_EX + Fore.WHITE} Error {Style. RESET_ALL}')

    @task(2)
    def viewprevious(self):
        response = self.client.get("/cgi-bin/badstore.cgi?action=viewprevious")
        if response.status_code == 200:
            print(f"{'VIEW':12} {Back.LIGHTCYAN_EX + Fore.BLUE} Load {Style. RESET_ALL}")
        else:
            print(f'{'VIEW':12} {Back.LIGHTRED_EX + Fore.WHITE} Error {Style. RESET_ALL}')

    @task(2)
    def cartadd(self):
        response = self.client.post("/cgi-bin/badstore.cgi", data={"cartitem": ["1003", "1005"], "Add+Items+to+Cart": "Add+Items+to+Cart"})      
        if response.status_code == 200:
            if 'Welcome' in response.text:
                print(f'{'Add Cart':12} {Back.LIGHTMAGENTA_EX + Fore.WHITE} Compra Hecha {Style. RESET_ALL}')
            else:
                print(f'{'Add Cart':12} {Back.LIGHTYELLOW_EX + Fore.BLACK} Error compra {Style. RESET_ALL}')
        else:
            print(f'{'Add Cart':12} {Back.LIGHTRED_EX + Fore.WHITE} Error Add Cart{Style. RESET_ALL}')
        # Después del login, las siguientes tareas serán seleccionadas aleatoriamente

    @task(1)
    def cartview(self):
        response = self.client.get("/cgi-bin/badstore.cgi?action=cartview")
        if response.status_code == 200:
            print(f"{'CART':12} {Back.LIGHTCYAN_EX + Fore.BLUE} Load {Style. RESET_ALL}")
        else:
            print(f'{'CART':12} {Back.LIGHTRED_EX + Fore.WHITE} Error {Style. RESET_ALL}')

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
    host = 'http://0.0.0.0' ## Dominio de url
