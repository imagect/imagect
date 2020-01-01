from rx import operators as ops
from rx.subject import Subject
from traits.api import UUID, Bool, Instance
from .ImageStack import ImageStack
import uuid


class ImagePlus(object):
    """
    wrapper for image stack
        event
        update
        read
    """

    id = UUID(can_init=True)

    locked = Bool()

    sub_stack_updated = Instance(Subject)

    sub_slice_updated = Instance(Subject)

    stack = Instance(ImageStack)

    def __init__(self):
        self.stack = None
        self.id = uuid.uuid4()
        self.locked = False
        self.sub_slice_updated = Subject()
        self.sub_stack_updated = Subject()

    def update_stack(self, stack):
        self.stack = stack
        self.sub_stack_updated.on_next(self.stack)

    def update_slice(self, index, sslice):
        if self.stack.updateStack(index, sslice) :
            self.sub_slice_updated.on_next((index, sslice))



