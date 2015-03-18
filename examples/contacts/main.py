from kivy.app import App
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListItemLabel, CompositeListItem, ListView

from plyer import contacts


class ContactsInterface(GridLayout):

    def __init__(self, **kwargs):
        kwargs['cols'] = 3
        super(ContactsInterface, self).__init__(**kwargs)

        args_converter = \
            lambda row_index, rec: \
                {'text': rec['display_name'],
                 'size_hint_y': None,
                 'height': 35,
                 'cls_dicts': [{'cls': ListItemLabel,
                                'kwargs': {
                                    'text': rec['contact_id'],
                                    'size_hint_x': 0.2
                                }},
                               {'cls': ListItemLabel,
                                'kwargs': {
                                    'text': rec['display_name'],
                                    'size_hint_x': 0.5
                                }},
                               {'cls': ListItemLabel,
                                'kwargs': {
                                    'text': ', '.join(rec['phone_numbers'])
                                }},
                               ]}

        item_strings = [str(index) for index in range(len(contacts))]

        integers_dict = {
            str(i): contact for i, contact in enumerate(contacts)
        }

        dict_adapter = DictAdapter(sorted_keys=item_strings,
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

