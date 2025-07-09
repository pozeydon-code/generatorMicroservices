def parse_csharp_type(prop_def):
    # Si es un string plano
    if isinstance(prop_def, str):
        type_str = prop_def
        return {
            "Guid": "Guid",
            "string": "string",
            "int": "int",
            "decimal": "decimal",
            "DateTime": "DateTime",
            "ICollection<Product>": "ICollection<Product>"
        }.get(type_str, type_str)

    # Si es un dict con valueObject
    if isinstance(prop_def, dict):
        return prop_def.get("valueObject") or parse_csharp_type(prop_def.get("type"))

    return "object"
