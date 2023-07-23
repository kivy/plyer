'''
Example of an !! Android specific !! filechooser.
'''

from textwrap import dedent

from plyer import filechooser

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.button import Button


class FileChoose(Button):
    '''
    Button that triggers 'filechooser.open_file()' and processes
    the data response from filechooser Activity.
    '''

    selection = ListProperty([])

    def choose(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        self.selection = selection

    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        App.get_running_app().root.ids.result.text = str(self.selection)


class FileSave(Button):
    '''
    Button that triggers 'filechooser.save_file()' and processes
    the data response from filechooser Activity.
    '''

    def save(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        filechooser.save_file(
            callback=self.handle_save,
            title=str(App.get_running_app().root.ids.savefilename.text)
        )

    def handle_save(self, fileOutputStream):
        '''
        Callback function for handling the selection response from Activity.
        No need to close the stream here, it will be closed internally.
        '''
        fileOutputStream.write(str(
            App.get_running_app().root.ids.savefilecontent.text
        ).encode('utf-8'))


class ChooserApp(App):
    '''
    Application class with root built in KV.
    '''

    def build(self):
        return Builder.load_string(dedent('''
            <FileChoose>:

            BoxLayout:

                BoxLayout:
                    orientation: 'vertical'

                    TextInput:
                        id: result
                        text: ''
                        hint_text: 'selected path'

                    FileChoose:
                        size_hint_y: 0.1
                        on_release: self.choose()
                        text: 'Select a file'

                    TextInput:
                        id: savefilename
                        text: 'filechooser-example.txt'
                        hint_text: 'default name of the file to write (optional)'

                    TextInput:
                        id: savefilecontent
                        text: 'Hello, Android!'
                        hint_text: 'content (text only here) to write'

                    FileSave:
                        size_hint_y: 0.1
                        on_release: self.save()
                        text: 'Save text as'
        '''))


if __name__ == '__main__':
    ChooserApp().run()
