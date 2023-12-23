class DataPreprocessor:
    """
    Separating out the transformation functions and the parameters that control them allows
    us to re-use the same transforms in many different contexts without duplicating the
    code.
    """
    def __init__(self, data, processor):
        self.data = data
        self.processor = processor

    def _key_exists(self, key):
        return key in self.data

    def remove_unwanted_keys(self):
        for key in self.processor:
            if self._key_exists(key):
                self.data.pop(key)

