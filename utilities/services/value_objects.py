import os
from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file

def generate_value_objects(base_path, service_name, entities):
    import re
    vo_path = os.path.join(base_path, "Services", service_name, f"{service_name}.Domain", "ValueObjects")
    create_directory(vo_path)

    vo_defs = {}

    for props in entities.values():
        for prop_def in props.values():
            if isinstance(prop_def, dict) and "valueObject" in prop_def:
                vo_name = prop_def["valueObject"]
                validations = prop_def.get("validations", {})
                vo_defs[vo_name] = validations

    for vo_class, validations in vo_defs.items():
        content = ""
        if vo_class in ["Name", "Description", "EmailAddress", "CustomString"]:
            min_len = validations.get("minLength")
            max_len = validations.get("maxLength")
            regex = validations.get("regex")

            conditions = []
            if regex:
                conditions.append("!System.Text.RegularExpressions.Regex.IsMatch(value, @\"{}\")".format(regex.replace('"', '\\"')))
            if min_len is not None:
                conditions.append(f"value.Length < {min_len}")
            if max_len is not None:
                conditions.append(f"value.Length > {max_len}")
            conditions.insert(0, "string.IsNullOrEmpty(value)")

            condition_str = " || ".join(conditions)

            content = f"""using System.Text.RegularExpressions;

namespace {service_name}.Domain.ValueObjects;

public partial record {vo_class}
{{
    public string Value {{ get; init; }}
    private {vo_class}(string value) => Value = value;

    public static {vo_class}? Create(string value)
    {{
        if ({condition_str})
            return null;

        return new {vo_class}(value);
    }}

    public static implicit operator string({vo_class} valueObject) => valueObject.Value;
    public override string ToString() => Value;
}}
"""
        elif vo_class == "ProductPrice":
            min_value = validations.get("min", "0")
            condition = f"value < {min_value}"

            content = f"""namespace {service_name}.Domain.ValueObjects;

public partial record ProductPrice
{{
    public decimal Value {{ get; init; }}
    private ProductPrice(decimal value) => Value = value;

    public static ProductPrice? Create(decimal value)
    {{
        if ({condition})
            return null;

        return new ProductPrice(value);
    }}

    public static implicit operator decimal(ProductPrice price) => price.Value;
    public override string ToString() => Value.ToString("C");
}}
"""
        else:
            continue

        create_file(os.path.join(vo_path, f"{vo_class}.cs"), content)
