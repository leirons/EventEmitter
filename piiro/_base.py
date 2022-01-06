"utf-8"
from threading import Lock
from collections import defaultdict
__all__ = ['BaseEventEmitter', "EventEmitter", 'PiiroBaseException']


class PiiroBaseException(Exception):
    pass


class BaseEventEmitter():

    def __init__(self):
        self._events = defaultdict(dict)
        self.lock = Lock()

    def _call_handlers(self, event, args, kwargs):
        handled = False
        with self.lock:
            for f in self._events[event].values():
                self._emit_run(f, args, kwargs)
                handled = True
        return handled

    def _remove_listeners(self, event):
        with self.lock:
            for f in self._events[event]:
                pass

    def _remove_listener(self,event,listener):
        pass

    def _subscribe(self):
        ...

    def _unsubscribe(self):
        ...

    def _emit_run(self, f, args, kwargs) -> None:
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

        with self.lock:
            count_of_listeners = len(self._events[event].values())
            return count_of_listeners

    def _handle_potential_error(self):
        pass

    def _handle_error(self, exc, args, kwargs):
        pass


class EventEmitter(BaseEventEmitter):

    def __init__(self):
        super().__init__()

    def on(self, event, f=None):

        def _wrapper(f):
            self._add_handler(event, f, f)

        if f is None:
            return _wrapper
        else:
            return _wrapper(f)

    def emit(self, event, *args, **kwargs) -> bool:
        called = self._call_handlers(event, args, kwargs)
        return called

    def listeners_count(self, event):
        self.listeners_count(event)


em = BaseEventEmitter()
ee = EventEmitter()
@ee.on('query_params')
def function_for_checking(message):
    print(message)


ee.emit('query_params','s')




















class A:
    def __init__(self):
        print('Initializing: class A')

    def sub_method(self, b):
        print('sub_method from class A:', b)


class B(A):
    def __init__(self):
        print('Initializing: class B')
        super().__init__()

    def sub_method(self, b):
        print('sub_method from class B:', b)
        super().sub_method(b + 1)

class X(B):
    def __init__(self):
        print('Initializing: class X')
        super().__init__()

    def sub_method(self, b):
        print('sub_method from class X:', b)
        super().sub_method(b + 1)


class Y(X):
    def __init__(self):
        print('Initializing: class Y')
        # super() с параметрами
        super(X,self).__init__()

    def sub_method(self, b):
        print('sub_method from class Y:', b)
        super().sub_method(b + 1)



y = Y()