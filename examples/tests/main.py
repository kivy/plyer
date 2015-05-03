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
from plyer.utils import platform

import logging

log = logging.getLogger()

kv = """
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

# app example
BoxLayout:
    orientation: "vertical"
    BoxLayout:
        padding: "2sp"
        spacing: "2sp"
        size_hint_y: None
        height: "48sp"

        Button:
            text: "Sort data"
            on_release: app.sort_data()

        Button:
            text: "Generate new data"
            on_release: app.generate_new_data()

    RecycleView:
        id: rv

"""

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


class State:

    Ok = 'Ok'
    NotImplemented = 'Not Implemented'
    Error = 'Error'


class TestViewApp(App):

    results = ListProperty()
    rv = RecycleView()

    def build(self):
        self.root = Builder.load_string(kv)
        self.rv = self.root.ids.rv
        self.rv.key_viewclass = "viewclass"
        self.rv.key_size = "height"
        self.rv.data = self.results
        self.run_tests()

    def try_method(self, f):
        try:
            f()
            log.info(State.Ok)
            return State.Ok
        except NotImplementedError:
            log.info(State.NotImplemented)
            return State.NotImplemented
        except Exception:
            log.info(State.Error)
            return State.Error

    def run_tests(self):

        for module, functions in registered_modules.iteritems():
            log.info('Testing module %s', module)
            try:
                __import__('plyer.platforms.%s.%s' % (platform, module))
            except ImportError:
                self._add_separator(module, State.NotImplemented)

            total = len(functions)
            passed = 0
            for name, function in functions:
                log.info('Testing function %s', name)
                result = self.try_method(function)
                if result == State.Ok:
                    passed += 1
                self._add_test_result(name, result)

    def _add_separator(self, module_name, state=None):
        self.results.append({
            "viewclass": "Separator",
            "height": sp(20),
            "index": len(self.results),
            "module_name": '%25s %s' % (module_name, state)
        })
        self.rv.refresh_from_data(force=True)

    def _add_test_result(self, test_name, state):
        self.rv.data.append({
            "viewclass": "LogItem",
            "index": len(self.results),
            "test_result": "{} {}".format(
                state,
                test_name,
            )
        })
        self.rv.refresh_from_data(force=True)

TestViewApp().run()

