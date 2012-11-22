"""
An event class which allows events to be registered and called
Based on http://www.valuedlessons.com/2008/04/events-in-python.html
"""
class Event(object):
    
    # A set of handlers for the event
    handlers = None
    
    """
    Initialises the event
    """
    def __init__(self):
        self.handlers = set()

    """
    Add a function to be called when the event is called
    """
    def __iadd__(self, handler):
        self.handler.add(handler)
        return self

    """
    Unregister a function call from the event
    """
    def __isub__(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("This handler is not registered to this event")
        return self

    """
    When called, fire the event, i.e. call the functions in the order they were added
    """
    def __call__(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    """
    When length called, return how many listeners we have
    """
    def __len__(self):
        return len(self.handlers)