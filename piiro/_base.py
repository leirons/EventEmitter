# -*- coding: utf-8 -*-

import copy
from threading import Lock
from collections import defaultdict

__all__ = ['BaseEventEmitter', "EventEmitter"]


# TODO add priority to the listeners
# TODO add celery support

class BaseEventEmitter:
    def __init__(self):
        self._events = defaultdict(dict)
        self.lock = Lock()

    def _call_handlers(self, event, args, kwargs) -> bool:
        """

        Function calls all event listeners

        :param event:
        :param args:
        :param kwargs:
        :return bool:
        """
        handled = False
        with self.lock:
            for f in self._events[event].values():
                try:
                    self._emit_run(f, args, kwargs)
                except Exception as exc:
                    raise exc
                handled = True
        return handled

    def _remove_listeners(self, event):
        with self.lock:
            self._events[event].clear()

    def _remove_listener(self, event, listener):
        with self.lock:
            return self._events[event].pop(listener)  # Not save

    @staticmethod
    def _emit_run(f, args, kwargs) -> None:
        """

        The purpose of exception here is to call functions that have no parameters.
        The function itself is used to call all the functions in the event

        :param f: function
        :param args: (tuple) arguments
        :param kwargs: {dict} key:value
        :return:None
        """
        try:
            f(*args, **kwargs)
        except TypeError:
            f()

    def _add_handler(self, event, f1, f2) -> None:
        """

        Serves to add a handler to the list of events

        :param event: name of event
        :param f1: first function
        :param f2: second function
        :return: None
        """
        with self.lock:
            self._events[event][f1] = f2

    def _listeners_count(self, event) -> int:
        count_of_listeners = len(self._events[event].values())
        return count_of_listeners

    def _raw_listeners(self, event):
        with self.lock:
            return copy.copy(self._events[event])


class EventEmitter(BaseEventEmitter):
    """
    Copy of Node JS EventEmitter

    First usage:
        ee = EventEmitter()

        @ee.on('event_name')
        def call_me():
            pass

        calling all listeners that listen event_name
        ee.emit('event_name')

    Second usage:
        ee = EventEmitter()

        def call_me():
            pass

        ee.on('event_name',call_me)
        ee.emit('event_name')

    Third usage:
        ee = EventEmitter()

        @ee.on('event_name')
        def call_me(*args):
            print(args)

        def call_me_too():
            print('something')

        ee.on('event_name',call_me_too)

        ee.emit('event_name',1)

        There are not be any errors because args for function without params will be ignored

    Methods:
        on - listen function until it is removed from the event

        once - listens to a function only once, then deletes it

        emit - calls all event listeners

        listeners_count - return the number of listeners on event

        get_events - return all events

        remove_listeners - remove all listeners of event

        remove_listener - remove single listener of event ( Not save )

    There is one difference between once and on,
    On after the call will be immediately deleted,
    You should take this into account, but once will always be happy.

    Listeners in which there are no parameters, and you pass them there, then nothing terrible will happen,
    you can pass as many values as you like, if the listener does not accept anything and belongs to this event,
    then it will be called

    """

    def __init__(self):
        super().__init__()

    def on(self, event, f=None):

        def _wrapper(f):
            self._add_handler(event, f, f)

        if f is None:
            return _wrapper
        else:
            return _wrapper(f)

    def once(self, event, f=None):

        def _wrapper(f):
            def f2(*args, **kwargs):
                self._emit_run(f, args, kwargs)
                self.remove_listener(event, f2)

            self._add_handler(event, f, f2)

        if f is None:
            return _wrapper
        else:
            return _wrapper(f)

    def emit(self, event, *args, **kwargs) -> bool:
        called = self._call_handlers(event, args, kwargs)
        return called

    def listeners_count(self, event):
        return self._listeners_count(event)

    @property
    def get_events(self):
        return self._events

    def remove_listeners(self, event):
        self._remove_listeners(event)

    def remove_listener(self, event, listener):
        return self._remove_listener(event, listener)

    def raw_listeners(self, event):
        return self._raw_listeners(event)
