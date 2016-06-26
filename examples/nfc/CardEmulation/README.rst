Card Emulation
====

Fully supported API for Card Emulation is not provided yet.

For now, only the reference API is availabe.
To use these api's you need to add `card` or `f-card` in the action_list during the nfc_register method in your build method.

Example:

    nfc.nfc_register(tech_list={'all'},
                     action_list={'card', 'f-card'},
                     data_type="*/*")

Some methods require activity as one of their parameters.
Don't forget to pass the same instance of Python activity to all the methods.

Example.

`self.j_context = PythonActivity.mActivity`

Same goes for services:

 - OffHostApduService
 - HostNfcFService
 - HostApduService.
