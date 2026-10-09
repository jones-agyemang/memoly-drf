class Dig():
    @classmethod
    def dig(cls, data, *keys, default=None):

        if not keys: return data

        head, *tail = keys

        if not isinstance(data, dict): return default

        result = data.get(head, default)

        return cls.dig(result, *tail) if tail else result