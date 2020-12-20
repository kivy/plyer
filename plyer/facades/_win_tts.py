import sys
import traceback
import weakref
import six


class DriverProxy(object):
    '''
    Proxy to a driver implementation.

    @ivar _module: Module containing the driver implementation
    @type _module: module
    @ivar _engine: Reference to the engine that owns the driver
    @type _engine: L{engine.Engine}
    @ivar _queue: Queue of commands outstanding for the driver
    @type _queue: list
    @ivar _busy: True when the driver is busy processing a command, False when
        not
    @type _busy: bool
    @ivar _name: Name associated with the current utterance
    @type _name: str
    @ivar _debug: Debugging output enabled or not
    @type _debug: bool
    @ivar _iterator: Driver iterator to invoke when in an external run loop
    @type _iterator: iterator
    '''

    def __init__(self, engine, driverName, debug):
        '''
        Constructor.

        @param engine: Reference to the engine that owns the driver
        @type engine: L{engine.Engine}
        @param driverName: Name of the driver module to use under drivers/ or
            None to select the default for the platform
        @type driverName: str
        @param debug: Debugging output enabled or not
        @type debug: bool
        '''

        class Voice(object):
            def __init__(self, id, name=None, languages=[], gender=None, age=None):
                self.id = id
                self.name = name
                self.languages = languages
                self.gender = gender
                self.age = age

            def __str__(self):
                return """<Voice id=%(id)s
                name=%(name)s
                languages=%(languages)s
                gender=%(gender)s
                age=%(age)s>""" % self.__dict__
        if driverName is None:
            # pick default driver for common platforms
            if sys.platform == 'win32':
                import comtypes.client
                # Importing comtypes.client will make the gen subpackage
                try:
                    from comtypes.gen import SpeechLib  # comtypes
                except ImportError:
                    # Generate the SpeechLib lib and any associated files
                    engine = comtypes.client.CreateObject("SAPI.SpVoice")
                    from comtypes.gen import SpeechLib

                import pythoncom
                import time
                import math
                import os

                '''
                Utility functions to help with Python 2/3 compatibility
                '''
                import six

                def toUtf8(value):
                    '''
                    Takes in a value and converts it to a text (unicode) type.  Then decodes that
                    type to a byte array encoded in utf-8.  In 2.X the resulting object will be a
                    str and in 3.X the resulting object will be bytes.  In both 2.X and 3.X any
                    object can be passed in and the object's __str__ will be used (or __repr__ if
                    __str__ is not defined) if the object is not already a text type.
                    '''
                    return six.text_type(value).encode('utf-8')

                def fromUtf8(value):
                    '''
                    Takes in a byte array encoded as utf-8 and returns a text (unicode) type.  In
                    2.X we expect a str type and return a unicde type.  In 3.X we expect a bytes
                    type and return a str type.
                    '''
                    return value.decode('utf-8')

                # common voices
                MSSAM = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\MSSam'
                MSMARY = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\MSMary'
                MSMIKE = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\MSMike'

                # coeffs for wpm conversion
                E_REG = {MSSAM: (137.89, 1.11),
                        MSMARY: (156.63, 1.11),
                        MSMIKE: (154.37, 1.11)}

                def buildDriver(proxy):
                    return SAPI5Driver(proxy)

                class SAPI5Driver(object):
                    def __init__(self, proxy):
                        self._tts = comtypes.client.CreateObject('SAPI.SPVoice')
                        # all events
                        self._tts.EventInterests = 33790
                        self._event_sink = SAPI5DriverEventSink()
                        self._event_sink.setDriver(weakref.proxy(self))
                        self._advise = comtypes.client.GetEvents(self._tts, self._event_sink)
                        self._proxy = proxy
                        self._looping = False
                        self._speaking = False
                        self._stopping = False
                        # initial rate
                        self._rateWpm = 200
                        self.setProperty('voice', self.getProperty('voice'))

                    def destroy(self):
                        self._tts.EventInterests = 0

                    def say(self, text):
                        self._proxy.setBusy(True)
                        self._proxy.notify('started-utterance')
                        self._speaking = True
                        self._tts.Speak(fromUtf8(toUtf8(text)))

                    def stop(self):
                        if not self._speaking:
                            return
                        self._proxy.setBusy(True)
                        self._stopping = True
                        self._tts.Speak('', 3)

                    def save_to_file(self, text, filename):
                        cwd = os.getcwd()
                        stream = comtypes.client.CreateObject('SAPI.SPFileStream')
                        stream.Open(filename, SpeechLib.SSFMCreateForWrite)
                        temp_stream = self._tts.AudioOutputStream
                        self._tts.AudioOutputStream = stream
                        self._tts.Speak(fromUtf8(toUtf8(text)))
                        self._tts.AudioOutputStream = temp_stream
                        stream.close()
                        os.chdir(cwd)

                    def _toVoice(self, attr):
                        return Voice(attr.Id, attr.GetDescription())

                    def _tokenFromId(self, id_):
                        tokens = self._tts.GetVoices()
                        for token in tokens:
                            if token.Id == id_:
                                return token
                        raise ValueError('unknown voice id %s', id_)

                    def getProperty(self, name):
                        if name == 'voices':
                            return [self._toVoice(attr) for attr in self._tts.GetVoices()]
                        elif name == 'voice':
                            return self._tts.Voice.Id
                        elif name == 'rate':
                            return self._rateWpm
                        elif name == 'volume':
                            return self._tts.Volume / 100.0
                        else:
                            raise KeyError('unknown property %s' % name)

                    def setProperty(self, name, value):
                        if name == 'voice':
                            token = self._tokenFromId(value)
                            self._tts.Voice = token
                            a, b = E_REG.get(value, E_REG[MSMARY])
                            self._tts.Rate = int(math.log(self._rateWpm / a, b))
                        elif name == 'rate':
                            id_ = self._tts.Voice.Id
                            a, b = E_REG.get(id_, E_REG[MSMARY])
                            try:
                                self._tts.Rate = int(math.log(value / a, b))
                            except TypeError as e:
                                raise ValueError(str(e))
                            self._rateWpm = value
                        elif name == 'volume':
                            try:
                                self._tts.Volume = int(round(value * 100, 2))
                            except TypeError as e:
                                raise ValueError(str(e))
                        else:
                            raise KeyError('unknown property %s' % name)

                    def startLoop(self):
                        first = True
                        self._looping = True
                        while self._looping:
                            if first:
                                self._proxy.setBusy(False)
                                first = False
                            pythoncom.PumpWaitingMessages()
                            time.sleep(0.05)

                    def endLoop(self):
                        self._looping = False

                    def iterate(self):
                        self._proxy.setBusy(False)
                        while 1:
                            pythoncom.PumpWaitingMessages()
                            yield

                class SAPI5DriverEventSink(object):
                    def __init__(self):
                        self._driver = None

                    def setDriver(self, driver):
                        self._driver = driver

                    def _ISpeechVoiceEvents_StartStream(self, char, length):
                        self._driver._proxy.notify(
                            'started-word', location=char, length=length)

                    def _ISpeechVoiceEvents_EndStream(self, stream, pos):
                        d = self._driver
                        if d._speaking:
                            d._proxy.notify('finished-utterance', completed=not d._stopping)
                        d._speaking = False
                        d._stopping = False
                        d._proxy.setBusy(False)

        # build driver instance
        self._driver = buildDriver(weakref.proxy(self))
        # initialize refs
        self._engine = engine
        self._queue = []
        self._busy = True
        self._name = None
        self._iterator = None
        self._debug = debug

    def __del__(self):
        try:
            self._driver.destroy()
        except (AttributeError, TypeError):
            pass

    def _push(self, mtd, args, name=None):
        '''
        Adds a command to the queue.

        @param mtd: Method to invoke to process the command
        @type mtd: method
        @param args: Arguments to apply when invoking the method
        @type args: tuple
        @param name: Name associated with the command
        @type name: str
        '''
        self._queue.append((mtd, args, name))
        self._pump()

    def _pump(self):
        '''
        Attempts to process the next command in the queue if one exists and the
        driver is not currently busy.
        '''
        while (not self._busy) and len(self._queue):
            cmd = self._queue.pop(0)
            self._name = cmd[2]
            try:
                cmd[0](*cmd[1])
            except Exception as e:
                self.notify('error', exception=e)
                if self._debug:
                    traceback.print_exc()

    def notify(self, topic, **kwargs):
        '''
        Sends a notification to the engine from the driver.

        @param topic: Notification topic
        @type topic: str
        @param kwargs: Arbitrary keyword arguments
        @type kwargs: dict
        '''
        kwargs['name'] = self._name
        self._engine._notify(topic, **kwargs)

    def setBusy(self, busy):
        '''
        Called by the driver to indicate it is busy.

        @param busy: True when busy, false when idle
        @type busy: bool
        '''
        self._busy = busy
        if not self._busy:
            self._pump()

    def isBusy(self):
        '''
        @return: True if the driver is busy, false if not
        @rtype: bool
        '''
        return self._busy

    def say(self, text, name):
        '''
        Called by the engine to push a say command onto the queue.

        @param text: Text to speak
        @type text: unicode
        @param name: Name to associate with the utterance
        @type name: str
        '''
        self._push(self._driver.say, (text,), name)

    def stop(self):
        '''
        Called by the engine to stop the current utterance and clear the queue
        of commands.
        '''
        # clear queue up to first end loop command
        while(True):
            try:
                mtd, args, name = self._queue[0]
            except IndexError:
                break
            if(mtd == self._engine.endLoop):
                break
            self._queue.pop(0)
        self._driver.stop()

    def save_to_file(self, text, filename, name):
        '''
        Called by the engine to push a say command onto the queue.

        @param text: Text to speak
        @type text: unicode
        @param name: Name to associate with the utterance
        @type name: str
        '''
        self._push(self._driver.save_to_file, (text, filename), name)

    def getProperty(self, name):
        '''
        Called by the engine to get a driver property value.

        @param name: Name of the property
        @type name: str
        @return: Property value
        @rtype: object
        '''
        return self._driver.getProperty(name)

    def setProperty(self, name, value):
        '''
        Called by the engine to set a driver property value.

        @param name: Name of the property
        @type name: str
        @param value: Property value
        @type value: object
        '''
        self._push(self._driver.setProperty, (name, value))

    def runAndWait(self):
        '''
        Called by the engine to start an event loop, process all commands in
        the queue at the start of the loop, and then exit the loop.
        '''
        self._push(self._engine.endLoop, tuple())
        self._driver.startLoop()

    def startLoop(self, useDriverLoop):
        '''
        Called by the engine to start an event loop.
        '''
        if useDriverLoop:
            self._driver.startLoop()
        else:
            self._iterator = self._driver.iterate()

    def endLoop(self, useDriverLoop):
        '''
        Called by the engine to stop an event loop.
        '''
        self._queue = []
        self._driver.stop()
        if useDriverLoop:
            self._driver.endLoop()
        else:
            self._iterator = None
        self.setBusy(True)

    def iterate(self):
        '''
        Called by the engine to iterate driver commands and notifications from
        within an external event loop.
        '''
        try:
            next(self._iterator)
        except StopIteration:
            pass


class Engine(object):
    """
    @ivar proxy: Proxy to a driver implementation
    @type proxy: L{DriverProxy}
    @ivar _connects: Array of subscriptions
    @type _connects: list
    @ivar _inLoop: Running an event loop or not
    @type _inLoop: bool
    @ivar _driverLoop: Using a driver event loop or not
    @type _driverLoop: bool
    @ivar _debug: Print exceptions or not
    @type _debug: bool
    """


    def __init__(self, driverName=None, debug=False):
        """
        Constructs a new TTS engine instance.

        @param driverName: Name of the platform specific driver to use. If
            None, selects the default driver for the operating system.
        @type: str
        @param debug: Debugging output enabled or not
        @type debug: bool
        """
        self.proxy = DriverProxy(weakref.proxy(self), driverName, debug)
        # initialize other vars
        self._connects = {}
        self._inLoop = False
        self._driverLoop = True
        self._debug = debug

    def _notify(self, topic, **kwargs):
        """
        Invokes callbacks for an event topic.

        @param topic: String event name
        @type topic: str
        @param kwargs: Values associated with the event
        @type kwargs: dict
        """
        for cb in self._connects.get(topic, []):
            try:
                cb(**kwargs)
            except Exception:
                if self._debug:
                    traceback.print_exc()

    def connect(self, topic, cb):
        """
        Registers a callback for an event topic. Valid topics and their
        associated values:

        started-utterance: name=<str>
        started-word: name=<str>, location=<int>, length=<int>
        finished-utterance: name=<str>, completed=<bool>
        error: name=<str>, exception=<exception>

        @param topic: Event topic name
        @type topic: str
        @param cb: Callback function
        @type cb: callable
        @return: Token to use to unregister
        @rtype: dict
        """
        arr = self._connects.setdefault(topic, [])
        arr.append(cb)
        return {'topic': topic, 'cb': cb}

    def disconnect(self, token):
        """
        Unregisters a callback for an event topic.

        @param token: Token of the callback to unregister
        @type token: dict
        """
        topic = token['topic']
        try:
            arr = self._connects[topic]
        except KeyError:
            return
        arr.remove(token['cb'])
        if len(arr) == 0:
            del self._connects[topic]

    def say(self, text, name=None):
        """
        Adds an utterance to speak to the event queue.

        @param text: Text to sepak
        @type text: unicode
        @param name: Name to associate with this utterance. Included in
            notifications about this utterance.
        @type name: str
        """
        self.proxy.say(text, name)

    def stop(self):
        """
        Stops the current utterance and clears the event queue.
        """
        self.proxy.stop()

    def save_to_file(self, text, filename, name=None):
        '''
        Adds an utterance to speak to the event queue.

        @param text: Text to sepak
        @type text: unicode
        @param filename: the name of file to save.
        @param name: Name to associate with this utterance. Included in
            notifications about this utterance.
        @type name: str
        '''
        self.proxy.save_to_file(text, filename, name)

    def isBusy(self):
        """
        @return: True if an utterance is currently being spoken, false if not
        @rtype: bool
        """
        return self.proxy.isBusy()

    def getProperty(self, name):
        """
        Gets the current value of a property. Valid names and values include:

        voices: List of L{voice.Voice} objects supported by the driver
        voice: String ID of the current voice
        rate: Integer speech rate in words per minute
        volume: Floating point volume of speech in the range [0.0, 1.0]

        Numeric values outside the valid range supported by the driver are
        clipped.

        @param name: Name of the property to fetch
        @type name: str
        @return: Value associated with the property
        @rtype: object
        @raise KeyError: When the property name is unknown
        """
        return self.proxy.getProperty(name)

    def setProperty(self, name, value):
        """
        Adds a property value to set to the event queue. Valid names and values
        include:

        voice: String ID of the voice
        rate: Integer speech rate in words per minute
        volume: Floating point volume of speech in the range [0.0, 1.0]

        Numeric values outside the valid range supported by the driver are
        clipped.

        @param name: Name of the property to fetch
        @type name: str
        @param: Value to set for the property
        @rtype: object
        @raise KeyError: When the property name is unknown
        """
        self.proxy.setProperty(name, value)

    def runAndWait(self):
        """
        Runs an event loop until all commands queued up until this method call
        complete. Blocks during the event loop and returns when the queue is
        cleared.

        @raise RuntimeError: When the loop is already running
        """
        if self._inLoop:
            raise RuntimeError('run loop already started')
        self._inLoop = True
        self._driverLoop = True
        self.proxy.runAndWait()

    def startLoop(self, useDriverLoop=True):
        """
        Starts an event loop to process queued commands and callbacks.

        @param useDriverLoop: If True, uses the run loop provided by the driver
            (the default). If False, assumes the caller will enter its own
            run loop which will pump any events for the TTS engine properly.
        @type useDriverLoop: bool
        @raise RuntimeError: When the loop is already running
        """
        if self._inLoop:
            raise RuntimeError('run loop already started')
        self._inLoop = True
        self._driverLoop = useDriverLoop
        self.proxy.startLoop(self._driverLoop)

    def endLoop(self):
        """
        Stops a running event loop.

        @raise RuntimeError: When the loop is not running
        """
        if not self._inLoop:
            raise RuntimeError('run loop not started')
        self.proxy.endLoop(self._driverLoop)
        self._inLoop = False

    def iterate(self):
        """
        Must be called regularly when using an external event loop.
        """
        if not self._inLoop:
            raise RuntimeError('run loop not started')
        elif self._driverLoop:
            raise RuntimeError('iterate not valid in driver run loop')
        self.proxy.iterate()


_activeEngines = weakref.WeakValueDictionary()


def init(driverName=None, debug=False):
    '''
    Constructs a new TTS engine instance or reuses the existing instance for
    the driver name.

    @param driverName: Name of the platform specific driver to use. If
        None, selects the default driver for the operating system.
    @type: str
    @param debug: Debugging output enabled or not
    @type debug: bool
    @return: Engine instance
    @rtype: L{engine.Engine}
    '''
    try:
        eng = _activeEngines[driverName]
    except KeyError:
        eng = Engine(driverName, debug)
        _activeEngines[driverName] = eng
    return eng


'''
Utility functions to help with Python 2/3 compatibility
'''


def toUtf8(value):
    '''
    Takes in a value and converts it to a text (unicode) type.  Then decodes that
    type to a byte array encoded in utf-8.  In 2.X the resulting object will be a
    str and in 3.X the resulting object will be bytes.  In both 2.X and 3.X any
    object can be passed in and the object's __str__ will be used (or __repr__ if
    __str__ is not defined) if the object is not already a text type.
    '''
    return six.text_type(value).encode('utf-8')


def fromUtf8(value):
    '''
    Takes in a byte array encoded as utf-8 and returns a text (unicode) type.  In
    2.X we expect a str type and return a unicde type.  In 3.X we expect a bytes
    type and return a str type.
    '''
    return value.decode('utf-8')


def speak(text):
    engine = init()
    engine.say(text)
    engine.runAndWait()

# speak('hello') # to speak out loud
