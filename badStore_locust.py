from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):

    def on_start(self):
        """Inicio de las pruebas siempre cargando la página principal y haciendo login"""
        self.is_logged_in = False
        self.load_homepage()

    @task
    def load_homepage(self):
        response = self.client.get("/")
        if response.status_code == 200:
            print("Página principal cargada correctamente.")
            self.login()  # Después de la página principal, ir al login

    @task(2)  # Peso mayor para esta tarea
    def login(self):
        response = self.client.post("/login", data={"username": "test_user", "password": "password"})
        if response.status_code == 200:
            print("Inicio de sesión exitoso.")
            self.is_logged_in = True  # Marcar como autenticado
        # Después del login, las siguientes tareas serán seleccionadas aleatoriamente

    @task(3)  # Peso mayor para esta tarea
    def load_profile(self):
        if self.is_logged_in:
            response = self.client.get("/profile")
            if response.status_code == 200:
                print("Perfil cargado correctamente.")

    @task(1)  # Peso menor para esta tarea
    def load_reports(self):
        if self.is_logged_in:
            response = self.client.get("/reports")
            if response.status_code == 200:
                print("Reportes cargados correctamente.")

    @task(1)  # Peso menor para esta tarea
    def load_consultation(self):
        if self.is_logged_in:
            response = self.client.get("/consultation")
            if response.status_code == 200:
                print("Consulta cargada correctamente.")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
