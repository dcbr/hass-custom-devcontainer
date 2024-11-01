import yaml

# Custom safe loader and dumper to preserve custom tags
class CustomTagMapping(dict):
    def __init__(self, tag, dct):
        super().__init__(dct)
        self.tag = tag

    @classmethod
    def to_yaml(cls, dumper, obj):
        return dumper.represent_mapping(obj.tag, obj)


class CustomTagSequence(list):
    def __init__(self, tag, lst):
        super().__init__(lst)
        self.tag = tag

    @classmethod
    def to_yaml(cls, dumper, obj):
        return dumper.represent_sequence(obj.tag, obj)


class CustomTagScalar(object):
    def __init__(self, tag, scalar):
        self.scalar = scalar
        self.tag = tag

    @classmethod
    def to_yaml(cls, dumper, obj):
        return dumper.represent_scalar(obj.tag, obj.scalar)


class CustomSafeLoader(yaml.SafeLoader):
    def custom_tag_constructor(self, node):
        if node.id=="mapping":
            return CustomTagMapping(node.tag, self.construct_mapping(node, deep=True))
        elif node.id=="sequence":
            return CustomTagSequence(node.tag, self.construct_sequence(node, deep=True))
        else:
            return CustomTagScalar(node.tag, self.construct_scalar(node))


class CustomSafeDumper(yaml.SafeDumper):
    pass


CustomSafeLoader.add_constructor(None, CustomSafeLoader.custom_tag_constructor)
CustomSafeDumper.add_representer(CustomTagMapping, CustomTagMapping.to_yaml)
CustomSafeDumper.add_representer(CustomTagSequence, CustomTagSequence.to_yaml)
CustomSafeDumper.add_representer(CustomTagScalar, CustomTagScalar.to_yaml)
