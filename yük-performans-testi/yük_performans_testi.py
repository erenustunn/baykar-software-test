from locust import HttpUser, task, between

class BaykarKariyer(HttpUser):
    wait_time = between(1, 5)  # Her istek arasında 1-5 saniye bekle

    @task(1)
    def home_page(self):
        self.client.get("/")

    @task(2)
    def kariyer(self):
        self.client.get("/#kariyer")

    @task(3)
    def baykarda_yasam(self):
        self.client.get("/#baykar-da-yasam")

    @task(4)
    def acık_pozisyonlar(self):
        self.client.get("/#acik-pozisyonlar")

    @task(5)
    def yerleskelerimiz(self):
        self.client.get("/#yerleskelerimiz")

    @task(6)
    def selcuk_bayraktar(self):
        self.client.get("/#selcuk-bayraktar")

    @task(7)
    def haluk_bayraktar(self):
        self.client.get("/#haluk-bayraktar")

    @task(8)
    def ozdemir_bayraktar(self):
        self.client.get("/#ozdemir-bayraktar")

    @task(9)
    def iletisim(self):
        self.client.get("/#iletisim")

    @task(10)
    def staj(self):
        self.client.get("/#staj")

    @task(11)
    def giriş(self):
        """
        Giriş sayfasına post request atma senaryosu
        """
        self.client.post("/tr/hesaplar/login/", data={
            "E-mail Giriniz": "kızılelmabaykar123@hotmail.com",
            "Şifre Giriniz": "BaykarTech", #### Giriş sayfasına reCAPTHCA bulunduğu için locust bu işlemi yapamaz. Sunucu tarafından doğrulanması gerektiği için backend tarafında bu kısmı doğrudan geçebilecek bir flag yazılabilir!

        })

