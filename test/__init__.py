"""Testing infrastructure for NFL-Stats.
Right now this "package" really only exists to create a test specific logger.
"""

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
