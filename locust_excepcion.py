from locust import HttpUser, TaskSet, task, between
from colorama import Fore, Back, Style

class UserBehavior(TaskSet):

    def on_start(self):
        # Inicializar contadores solo una vez
        if not hasattr(self.user, 'load_count'):
            self.user.load_count = 0
            self.user.error_count = 0
        self.is_logged_in = False
        
        # Imprimir el ID del usuario cuando se crea
        print(f"{Back.MAGENTA + Fore.WHITE} User {self.user.user_id} created. {Style.RESET_ALL}")
        
        self.load_homepage()

    @task  # 16.7%
    def load_homepage(self):
        response = self.client.get("/")
        if response.status_code == 200:
            self.user.load_count += 1  # Incrementar contador de carga
            print(f"{Back.LIGHTCYAN_EX + Fore.BLUE} User {self.user.user_id} loaded homepage successfully. {Style.RESET_ALL}")
        else:
            self.user.error_count += 1  # Incrementar contador de errores
            print(f"{Back.LIGHTRED_EX + Fore.WHITE} User {self.user.user_id} failed to load homepage. {Style.RESET_ALL}")

    @task(1)  # 16.7%
    def load_home(self):
        response = self.client.get("/cgi-bin/badstore.cgi")
        if response.status_code == 200:
            self.user.load_count += 1  # Incrementar contador de carga
            print(f"{Back.LIGHTCYAN_EX + Fore.BLUE} User {self.user.user_id} loaded home successfully. {Style.RESET_ALL}")
        else:
            self.user.error_count += 1  # Incrementar contador de errores
            print(f"{Back.LIGHTRED_EX + Fore.WHITE} User {self.user.user_id} failed to load home. {Style.RESET_ALL}")

    @task(4)  # 66.7%
    def login(self):
        response = self.client.post("/cgi-bin/badstore.cgi?action=loginregister", data={"email": "test_user", "passwd": "user", "Login": "Login"})
        if response.status_code == 200:
            self.user.load_count += 1  # Incrementar contador de carga para login
            print(f"{Back.LIGHTCYAN_EX + Fore.BLUE} User {self.user.user_id} logged in successfully. {Style.RESET_ALL}")
        else:
            self.user.error_count += 1  # Incrementar contador de errores para login
            print(f"{Back.LIGHTRED_EX + Fore.WHITE} User {self.user.user_id} failed to log in. {Style.RESET_ALL}")

    def on_stop(self):
        # Imprimir resultados al final de la ejecución
        if hasattr(self.user, 'load_count'):
            print(f"{'Total Loads:':<12} {Back.LIGHTCYAN_EX + Fore.BLUE}{self.user.load_count}{Style.RESET_ALL}")
            print(f"{'Total Errors:':<12} {Back.LIGHTRED_EX + Fore.WHITE}{self.user.error_count}{Style.RESET_ALL}")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
    host = 'http://192.168.20.56'  # Dominio de URL
