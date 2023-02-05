from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_string('''
#:import maps plyer.maps
<MainScreen>:
    GridLayout:
        cols: 1
        size_hint_y: None
        size: root.width, root.height

        TextInput:
            id: saddr
            hint_text: "Enter Start Address"
            background_color: 1,1,1,1

        TextInput:
            id: daddr
            hint_text: "Destination address (or leave blank for sliders)"
            background_color: 1,1,1,1

        Label:
            text: "Destination by Latitude/Longitude:"
            font_size: 40
            color: 0.12156862745098039, 0.9176470588235294, 0, 1

        GridLayout:
            cols: 2

            Label:
                id: lat
                text: "Latitude: 0.0"
                font_size: 40
                color: 0.12156862745098039, 0.9176470588235294, 0, 1

            Slider:
                id: lat_slider
                min: -90
                max: 90
                step: 0.00001
                orientation: "horizontal"
                on_value:
                    lat.text = f"Latitude: {self.value:.5f}"

            Label:
                id: long
                text: "Longitude: 0.0"
                font_size: 40
                color: 0.12156862745098039, 0.9176470588235294, 0, 1

            Slider:
                id: long_slider
                min: -180
                max: 180
                step: 0.00001
                orientation: "horizontal"
                on_value:
                    long.text = f"Longitude: {self.value:.5f}"

        FloatLayout:
            Button:
                text: "Open Maps"
                font_name: 'Roboto-Bold'
                color: 0.12156862745098039, 0.9176470588235294, 0, 1
                background_color: 1,1,1,1
                background_normal: ''
                pos_hint: {'center_x': 0.5, "top": .6}
                size_hint: (.6, .4)
                on_press:
                    end = daddr.text if daddr.text != '' \
                        else f"{lat_slider.value},{long_slider.value}"
                    start = saddr.text if saddr.text != '' else 'Here'
                    maps.route(start, end)

        GridLayout:
            cols: 2
            padding: 0, 10

            TextInput:
                id: query
                hint_text: "Enter Search Term (e.g. Mexican Restaurants)"
                background_color: 1,1,1,1

            FloatLayout:
                Button:
                    text: "Search on Maps"
                    font_name: 'Roboto-Bold'
                    color: 0.12156862745098039, 0.9176470588235294, 0, 1
                    background_color: 1,1,1,1
                    background_normal: ''
                    pos_hint: {'center_x': 0.5, "top": .7}
                    size_hint: (.6, .4)
                    on_press:
                        maps.search(query.text)
''')


class MainScreen(Widget):
    pass


class MapsApp(App):
    def build(self):
        return MainScreen()


MapsApp().run()
