from dataclasses import fields

# Ref: https://stackoverflow.com/a/51737200
def validate(instance):
    for field in fields(instance):
        attr = getattr(instance, field.name)
        if not isinstance(attr, field.type):
            msg = "Field {0.name} is of type {1}, should be {0.type}".format(field, type(attr))
            raise ValueError(msg)