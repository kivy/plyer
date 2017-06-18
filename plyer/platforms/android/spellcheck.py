'''
Android Spell Check
-------------------

Note: Spelling Checker Framework works only for Android 4.0 or later
'''

from jnius import autoclass, java_method, PythonJavaClass
from plyer.facades import SpellCheck
from plyer.platforms.android import activity

TextInfo = autoclass('android.view.textservice.TextInfo')
TextServicesManager = autoclass('android.view.textservice.TextServicesManager')
SentenceSuggestionsInfo = autoclass(
    'android.view.textservice.SentenceSuggestionsInfo')
SpellCheckerSession = autoclass('android.view.textservice.SpellCheckerSession')
SpellCheckerSessionListener = autoclass(
    'android.view.textservice.SpellCheckerSession.SpellCheckerSessionListener')
SuggestionsInfo = autoclass('android.view.textservice.SuggestionsInfo')
Context = autoclass('android.content.Context')
Build = autoclass('android.os.Bundle')


class SpellCheckerSessionListener(PythonJavaClass):

    __javainterfaces__ = [
        'android.view.textservice.SpellCheckerSession.\
        SpellCheckerSessionListener']
    __javacontext__ = 'app'

    def __init__(self):
        self.mScs = SpellCheckerSession()
        self.tsm = TextServicesManager()
        self.NOT_A_LENGTH = -1
        self.suggestions = ''

    def isSentenceSpellCheckSupported(self):
        return Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN

    def start(self, text):
        self.tsm = Context.getSystemService(
            Context.TEXT_SERVICES_MANAGER_SERVICE)
        self.mScs = tsm.newSpellCheckerSession(None, None, self, True)
        '''
        Instantiate TextInfo for each query
        TextInfo can be passed a sequence number and a cookie number to
        identify the result
        '''
        if(not(self.mScs)):
            if(self.isSentenceSpellCheckSupported()):
                '''
                Note that getSentenceSuggestions works on JB or later.
                '''
                self.mScs.getSentenceSuggestions(list(TextInfo(str(text))), 3)
            else:
                '''
                Note that getSuggestions() is a deprecated API.
                It is recommended for an application running on Jelly Bean or
                later to call getSentenceSuggestions() only.
                '''
                self.mScs.getSuggestions(TextInfo(str(text)), 3)

    def dumpSuggestionsInfoInternal(self, sb, si, length, offset):
        len_ = si.getSuggestionsCount()
        sb += '\n'
        for j in range(len_):
            if(j != 0):
                sb += ', '
            sb += si.getSuggestionsAt(j)
        sb += ' (' + len_ + ')'
        if(length != self.NOT_A_LENGTH):
            sb += 'length = ' + length + ', offset = ' + offset
        return sb

    @java_method('([Landroid/view/textservice/SuggestionsInfo;)V')
    def onGetSuggestions(self, arg0):
        sb = ''

        for i in range(len(arg0)):
            sb = self.dumpSuggestionsInfoInternal(
                sb, arg0[i], 0, self.NOT_A_LENGTH)
        self.suggestions = sb

    @java_method('([Landroid/view/textservice/SentenceSuggestionsInfo;)V')
    def onGetSentenceSuggestions(self, arg0):
        if(not(isSentenceSpellCheckSupported())):
            return
        sb = ''
        for i in range(len(arg0)):
            ssi = SentenceSuggestionsInfo(arg0[i])
            for j in range(ssi.getSuggestionsCount()):
                sb = dumpSuggestionsInfoInternal(
                        sb, ssi.getSuggestionsInfoAt(j),
                        ssi.getOffsetAt(j), ssi.getLengthAt(j))
        self.suggestions = sb


class AndroidSpellCheck(SpellCheck):

    listener = None

    def _get_suggestions(self, text):
        if not self.listener:
            self.listener = SpellCheckerSessionListener()
            self.listener.start(text)
            suggestions = self.listener.suggestions
            return suggestions


def instance():
    return AndroidSpellCheck()
