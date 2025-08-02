import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.metrics import dp

kivy.require('1.0.6')

class MainScreen(Screen):
    """ Ana gösterge paneli ekranı """
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Başlık ve bilgilendirici metin
        header = Label(text="Sağlıklı Yaşam Paneli", font_size='24sp', size_hint_y=None, height=dp(50))
        layout.add_widget(header)

        # Günlük Hedefler alanı
        goals_label = Label(text="Günlük Hedefler", font_size='18sp', size_hint_y=None, height=dp(40), halign='left')
        layout.add_widget(goals_label)
        
        goals_list = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        goals_list.bind(minimum_height=goals_list.setter('height'))
        
        # Hedeflerinizi buradan ekleyebilirsiniz
        goals_list.add_widget(Label(text="• 8 bardak su iç.", size_hint_y=None, height=dp(30), halign='left'))
        goals_list.add_widget(Label(text="• 30 dakika yürüyüş yap.", size_hint_y=None, height=dp(30), halign='left'))
        
        layout.add_widget(goals_list)

        # Ekranlar arası geçiş butonları
        button_layout = GridLayout(cols=3, spacing=dp(10), size_hint_y=None, height=dp(60))
        
        calculator_button = Button(text="Kalori Hesapla", on_press=self.go_to_calculator)
        recipes_button = Button(text="Yemek Tarifleri", on_press=self.go_to_recipes)
        layout.add_widget(Label(text="")) # Boşluk için
        button_layout.add_widget(calculator_button)
        button_layout.add_widget(recipes_button)
        layout.add_widget(button_layout)
        
        self.add_widget(layout)

    def go_to_calculator(self, instance):
        self.manager.current = 'calculator'

    def go_to_recipes(self, instance):
        self.manager.current = 'recipes'


class CalorieCalculatorScreen(Screen):
    """ Günlük kalori ihtiyacı hesaplama ekranı """
    def __init__(self, **kwargs):
        super(CalorieCalculatorScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # Başlık
        title = Label(text="Kalori Hesaplayıcı", font_size='24sp', size_hint_y=None, height=dp(50))
        layout.add_widget(title)

        # Form elemanları
        self.age_input = TextInput(hint_text="Yaş", multiline=False)
        self.weight_input = TextInput(hint_text="Kilo (kg)", multiline=False)
        self.height_input = TextInput(hint_text="Boy (cm)", multiline=False)
        self.activity_input = TextInput(hint_text="Aktivite Seviyesi (örn: 1.2)", multiline=False)

        form_grid = GridLayout(cols=1, spacing=dp(10))
        form_grid.add_widget(Label(text="Yaş:"))
        form_grid.add_widget(self.age_input)
        form_grid.add_widget(Label(text="Kilo (kg):"))
        form_grid.add_widget(self.weight_input)
        form_grid.add_widget(Label(text="Boy (cm):"))
        form_grid.add_widget(self.height_input)
        form_grid.add_widget(Label(text="Aktivite Seviyesi:"))
        form_grid.add_widget(self.activity_input)
        layout.add_widget(form_grid)
        
        calculate_button = Button(text="Hesapla", size_hint_y=None, height=dp(50), on_press=self.calculate_calories)
        layout.add_widget(calculate_button)

        self.result_label = Label(text="", font_size='18sp')
        layout.add_widget(self.result_label)

        back_button = Button(text="Geri", on_press=self.go_to_main, size_hint_y=None, height=dp(40))
        layout.add_widget(back_button)

        self.add_widget(layout)

    def calculate_calories(self, instance):
        # Burada kalori hesaplama mantığı yer alacak
        # Bu sadece bir yer tutucudur. Gerçek formüllerle doldurulmalıdır.
        try:
            age = int(self.age_input.text)
            weight = float(self.weight_input.text)
            height = float(self.height_input.text)
            
            # Basit bir BMR hesaplaması
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
            self.result_label.text = f"Günlük kalori ihtiyacınız: {int(bmr * 1.55)} kcal"
        except ValueError:
            self.result_label.text = "Lütfen geçerli değerler girin."
        

    def go_to_main(self, instance):
        self.manager.current = 'main'

class RecipesScreen(Screen):
    """ Yemek tarifleri ekranı """
    def __init__(self, **kwargs):
        super(RecipesScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        title = Label(text="Sağlıklı Yemek Tarifleri", font_size='24sp', size_hint_y=None, height=dp(50))
        layout.add_widget(title)

        scrollview = ScrollView()
        recipe_list = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        recipe_list.bind(minimum_height=recipe_list.setter('height'))
        
        # Tariflerinizi buraya ekleyin
        tarifler = [
            {"ad": "Avokadolu Tost", "kalori": "350 kcal", "tarif": "Avokadoyu ezin, limon sıkın, tuz ve karabiber ekleyin. Tost ekmeğine sürün."},
            {"ad": "Yeşil Mercimek Çorbası", "kalori": "250 kcal", "tarif": "Mercimekleri haşlayın, sebzeleri kavurun, hepsini birleştirin. Blenderdan geçirin."},
        ]

        for tarif in tarifler:
            recipe_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), padding=dp(10), spacing=dp(5))
            recipe_box.add_widget(Label(text=tarif["ad"], font_size='18sp', halign='left', bold=True))
            recipe_box.add_widget(Label(text=f"Kalori: {tarif['kalori']}", halign='left'))
            recipe_box.add_widget(Label(text=f"Tarif: {tarif['tarif']}", halign='left', text_size=(Window.width - dp(40), None)))
            
            recipe_list.add_widget(recipe_box)
            
        scrollview.add_widget(recipe_list)
        layout.add_widget(scrollview)

        back_button = Button(text="Geri", on_press=self.go_to_main, size_hint_y=None, height=dp(40))
        layout.add_widget(back_button)
        
        self.add_widget(layout)
        
    def go_to_main(self, instance):
        self.manager.current = 'main'


class HealthApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CalorieCalculatorScreen(name='calculator'))
        sm.add_widget(RecipesScreen(name='recipes'))
        return sm

if __name__ == '__main__':
    HealthApp().run()
  
