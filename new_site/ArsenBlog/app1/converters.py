class url:
    regex = "^\S+$"

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return f'{value}'
