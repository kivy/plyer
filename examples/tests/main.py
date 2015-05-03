from collections import defaultdict
from recycleview import RecycleView
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.app import App
from kivy.metrics import sp
import random

Builder.load_string("""
<Separator@BoxLayout>:
    module_name: ""
    canvas.before:
        Color:
            rgb: (.5, .5, .5)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        font_size: "14sp"
        color: (0, 1, 0, 1)
        text_size: (self.width, None)
        text: root.module_name

<LogItem@BoxLayout>:
    index: 0
    spacing: "5dp"
    test_result: ""
    canvas.before:
        Color:
            rgb: (0, 0, 0)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        font_size: "14sp"
        text: root.test_result
        color: (0, 1, 0, 1)
        text_size: (self.width, None)
""")

registered_modules = defaultdict(list)


def register_test(function_name):
    def decorator(f):
        module_name = function_name.split('.')[1]
        registered_modules[module_name].append((function_name, f))
        return f
    return decorator


@register_test('plyer.vibrator.vibrate()')
def test_vibrator_vibrate():
    from plyer import vibrator
    vibrator.vibrate()


@register_test('plyer.vibrator.vibrate(2s)')
def test_vibrator_vibrate():
    from plyer import vibrator
    vibrator.vibrate(2)


@register_test('plyer.vibrator.cancel()')
def test_vibrator_vibrate():
    from plyer import vibrator
    vibrator.cancel()


@register_test('plyer.vibrator.pattern([0.5, 0.1, 0.4])')
def test_vibrator_vibrate():
    from plyer import vibrator
    vibrator.pattern([0.5, 0.1, 0.4])


class TestApp(App):

    results = ListProperty()
    rv = RecycleView()

    def try_method(self, f):
        try:
            f()
            return 0
        except ImportError:
            print 'cannot import'
            return -3
        except NotImplementedError:
            print 'Not implemented yet on this platform'
            return -2
        except Exception:
            print 'error'
            return -1

    def run_tests(self):

        for module, functions in registered_modules.iteritems():
            print 'testing module', module
            self._add_separator(module)
            for name, function in functions:
                print 'testing function', name
                result = self.try_method(function)

                self._add_test_result(name, result)

    def _add_separator(self, module_name):
        self.results.append({
            "viewclass": "Separator",
            "height": sp(20),
            "module_name": module_name
        })
        self.rv.refresh_from_data(force=True)

    def _add_test_result(self, test_name, result):
        self.rv.data.append({
            "viewclass": "LogItem",
            "test_result": "{} {}".format(
                result,
                test_name,
            )
        })
        self.rv.refresh_from_data(force=True)

    def build(self):
        self.rv.key_viewclass = "viewclass"
        self.rv.key_height = "height"
        self.rv.data = self.results

        layout = BoxLayout(orientation='vertical')
        refresh_button = Button(text='Run Tests', size_hint=(1, .1))
        refresh_button.bind(on_press=self.run_tests())
        layout.add_widget(self.rv)

        return self.rv

test_app = TestApp()
test_app.run()
test_app.run_tests()
