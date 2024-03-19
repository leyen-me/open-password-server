class KeyUtil:

    def pad_key(key):
        if len(key) > 0 and len(key) <= 16:
            padding_length = 16 - len(key)
        if len(key) > 16:
            padding_length = 32 - len(key)
        padded_key = key + '0' * padding_length
        return padded_key
