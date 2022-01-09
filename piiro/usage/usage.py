from piiro import EventEmitter

ee = EventEmitter()

ee.on('ev')


def call_me():
    print('yes')


@ee.on('ev')
def call_me2(args):
    print(args)


ee.once('ev', call_me)

ee.emit('ev', 1)
