from kivy.app import App
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListItemLabel, CompositeListItem, ListView

from plyer import contacts
contacts.reload()

class ContactsInterface(GridLayout):

    def __init__(self, **kwargs):
        kwargs['cols'] = 3
        super(ContactsInterface, self).__init__(**kwargs)

        args_converter = \
            lambda row_index, rec: {
                'text': rec['display_name'],
                'size_hint_y': None,
                'height': 35,
                'cls_dicts': [
                    {'cls': ListItemLabel,
                        'kwargs': {
                            'text': rec['id'],
                            'size_hint_x': 0.2
                        }},
                    {'cls': ListItemLabel,
                        'kwargs': {
                            'text': rec['display_name'],
                            'size_hint_x': 0.5
                        }},
                    {'cls': ListItemLabel,
                        'kwargs': {
                            'text': ', '.join([
                                p['number'] for p in rec['phone_numbers']
                            ])
                        }},
                ]}

        integers_dict = {int(contact['id']): contact for contact in contacts}

        dict_adapter = DictAdapter(sorted_keys=sorted(integers_dict.keys()),
                                   data=integers_dict,
                                   args_converter=args_converter,
                                   selection_mode='single',
                                   allow_empty_selection=False,
                                   cls=CompositeListItem)

        # Use the adapter in our ListView:
        list_view = ListView(adapter=dict_adapter)

        self.add_widget(list_view)


class ContactsApp(App):

    def build(self):
        return ContactsInterface()

    def on_pause(self):
        return True


if __name__ == "__main__":
    ContactsApp().run()
