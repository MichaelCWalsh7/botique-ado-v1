# pylint: disable=missing-module-docstring,invalid-name
# Tell django the name of the default config class for the app.
# Without this line django wouldn't know about our custom ready method (
# in the checkout apps.py) so
# our signals wouldn't work.
default_app_config = 'checkout.apps.CheckoutConfig'
