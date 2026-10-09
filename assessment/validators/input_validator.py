class InputValidator():
    MIN_WORD_COUNT = 4
    MIN_CHAR_COUNT = 10

    @classmethod
    def has_minimum_word_count(cls, text):
        return isinstance(text, str) and len(text.split()) >= cls.MIN_WORD_COUNT

    @classmethod
    def has_minimum_char_count(cls, text):
        return isinstance(text, str) and len(text) >= cls.MIN_CHAR_COUNT
