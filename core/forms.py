class RequestKwargModelFormMixin(object):
    """
    Generic model form mixin for popping request out of the kwargs and
    attaching it to the instance.

    This mixin must precede forms.ModelForm/forms.Form. The form is not
    expecting these kwargs to be passed in, so they must be popped off before
    anything else is done.
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)  # Pop the request off the passed in kwargs.
        super(RequestKwargModelFormMixin, self).__init__(*args, **kwargs)