import os

from utilities.filesystem.create_directory import create_directory
from utilities.filesystem.create_file import create_file
from utilities.services.parser import parse_csharp_type
from utilities.services.validator import pluralize


def generate_entity_configurations(base_path, service_name, entities):
    config_path = os.path.join(
        base_path, "Services", service_name,
        f"{service_name}.Infrastructure", "Persistence", "Configuration"
    )
    create_directory(config_path)
    for entity_name, props in entities.items():
        table_name = pluralize(entity_name)
        lines = [
            "using Microsoft.EntityFrameworkCore;",
            "using Microsoft.EntityFrameworkCore.Metadata.Builders;",
            f"using {service_name}.Domain.Entities;",
            f"using {service_name}.Domain.ValueObjects;",
            "",
            f"namespace {service_name}.Infrastructure.Persistence.Configuration",
            "{",
            f"    public class {entity_name}Configuration : IEntityTypeConfiguration<{entity_name}>",
            "    {",
            f"        public void Configure(EntityTypeBuilder<{entity_name}> builder)",
            "        {",
            f"            builder.ToTable(\"{table_name}\");",
            f"            builder.HasKey(e => e.Id);",
            ""
        ]

        added_props = set()
        nav_relations = []

        # 1) Detectar navegación y FKs
        for prop_name, prop_def in props.items():
            if isinstance(prop_def, dict) and prop_def.get("navigation"):
                foreign_key = prop_def.get("foreignKey", f"{prop_name}Id")
                nav_relations.append((prop_name, foreign_key, prop_def))
                continue

            # Es FK de navegación: lo omitimos aquí
            if prop_name in [fk for (_, fk, _) in nav_relations]:
                continue

            # Mapeo normal o VO
            if isinstance(prop_def, dict) and "valueObject" in prop_def:
                vo = prop_def["valueObject"]
                max_len = prop_def.get("validations", {}).get("maxLength")
                line = f'builder.Property(e => e.{prop_name})' \
                       f'.HasConversion(v => v.Value, v => {vo}.Create(v)!)'
                if max_len:
                    line += f".HasMaxLength({max_len});"
                else:
                    line += ";"
            else:
                line = f"builder.Property(e => e.{prop_name});"

            lines.append("            " + line)
            added_props.add(prop_name)

        # 2) Configurar relaciones (solo desde el lado FK)
        for nav_name, fk_name, nav_def in nav_relations:
            if not nav_def.get("foreignKey"):
                continue  # ⚠️ omitir navegación inversa, se configura desde el otro lado
            # Nombre de la propiedad de navegación en código
            nav_prop = f"{nav_name}Navigation"
            # Buscar inverso bidireccional
            inverse = None
            related = parse_csharp_type(nav_def["type"])
            for rp, rd in entities.get(related, {}).items():
                if isinstance(rd, dict) and rd.get("navigation"):
                    inverse = f"{rp}Navigation"
            if inverse:
                line = f'builder.HasOne(e => e.{nav_prop})' \
                       f'.WithMany(c => c.{inverse})' \
                       f'.HasForeignKey(e => e.{fk_name});'
            else:
                line = f'builder.HasOne(e => e.{nav_prop})' \
                       f'.WithMany()' \
                       f'.HasForeignKey(e => e.{fk_name});'
            lines.append("")
            lines.append("            " + line)

        lines.append("        }")
        lines.append("    }")
        lines.append("}")

        create_file(
            os.path.join(config_path, f"{entity_name}Configuration.cs"),
            "\n".join(lines)
        )


# import os
# from utilities.filesystem.create_directory import create_directory
# from utilities.filesystem.create_file import create_file
# from utilities.services.parser import parse_csharp_type
# from utilities.services.validator import pluralize


# def generate_entity_configurations(base_path, service_name, entities):
#     config_path = os.path.join(base_path, "Services", service_name, f"{service_name}.Infrastructure", "Persistence", "Configuration")
#     create_directory(config_path)

#     for entity_name, props in entities.items():
#         # calcula el nombre de tabla con pluralización básica en inglés
#         table_name = pluralize(entity_name)
#         lines = [
#             "using Microsoft.EntityFrameworkCore;",
#             "using Microsoft.EntityFrameworkCore.Metadata.Builders;",
#             f"using {service_name}.Domain.Entities;",
#             f"using {service_name}.Domain.ValueObjects;",
#             "",
#             f"namespace {service_name}.Infrastructure.Persistence.Configuration",
#             "{",
#             f"    public class {entity_name}Configuration : IEntityTypeConfiguration<{entity_name}>",
#             "    {",
#             f"        public void Configure(EntityTypeBuilder<{entity_name}> builder)",
#             "        {",
#             f"            builder.ToTable(\"{table_name}\");",
#             f"            builder.HasKey(e => e.Id);",
#             ""
#         ]

#         added_props = set()
#         nav_relations = []

#         for prop_name, prop_def in props.items():
#             # Evitar duplicados
#             if prop_name in added_props:
#                 continue

#             if isinstance(prop_def, dict) and prop_def.get("navigation"):
#                 nav_relations.append((prop_name, prop_def))
#                 continue

#             csharp_type = parse_csharp_type(prop_def)

#             if csharp_type in ["Category", "Product"]:
#                 # navegación mal definida
#                 continue

#             if isinstance(prop_def, dict) and "valueObject" in prop_def:
#                 vo_class = prop_def["valueObject"]
#                 max_len = prop_def.get("validations", {}).get("maxLength")
#                 line = f'builder.Property(e => e.{prop_name}).HasConversion(v => v.Value, v => {vo_class}.Create(v)!)'
#                 if max_len:
#                     line += f".HasMaxLength({max_len});"
#                 else:
#                     line += ";"
#                 lines.append("            " + line)
#             else:
#                 lines.append(f"            builder.Property(e => e.{prop_name});")

#             added_props.add(prop_name)

#         # Relaciones
#         for nav_name, nav_def in nav_relations:
#             if not nav_def.get("foreignKey"):
#                 continue  # ⚠️ omitir navegación inversa, se configura desde el otro lado
#             related_entity = parse_csharp_type(nav_def["type"])
#             foreign_key = nav_def.get("foreignKey", f"{related_entity}Id")

#             # Nombre navigation con sufijo
#             # nav_prop = f"{nav_name}Navigation"
#             nav_prop = nav_name
#             # Inverso
#             inverse = None
#             # buscar si la entidad relacionada tiene una navegación de vuelta
#             # for related_prop, related_def in entities.get(related_entity, {}).items():
#             #     if isinstance(related_def, dict) and related_def.get("navigation"):
#             #         rel_type = parse_csharp_type(related_def["type"]).replace("[]", "")
#             #         if rel_type == entity_name:
#             #             inverse = f"{related_prop}Navigation"
#             for related_prop, related_def in entities.get(related_entity, {}).items():
#                 if isinstance(related_def, dict) and related_def.get("navigation"):
#                     type_str = related_def["type"]
#                     # si es ICollection<Producto>, extrae el interior
#                     if "ICollection<" in type_str:
#                         inner = type_str[type_str.find("<")+1:type_str.rfind(">")]
#                         if inner == entity_name:
#                             inverse = related_prop

#             # if inverse:
#             #     lines.append(f'            builder.HasOne(e => e.{nav_prop}).WithMany(e => e.{inverse}).HasForeignKey(e => e.{foreign_key});')
#             # else:
#             #     lines.append(f'            builder.HasOne(e => e.{nav_prop}).WithMany().HasForeignKey(e => e.{foreign_key});')
#             if inverse:
#                 lines.append(
#                     f'builder.HasOne(e => e.{nav_prop})'
#                     f'.WithMany(c => c.{inverse})'
#                     f'.HasForeignKey(e => e.{foreign_key});'
#                 )
#             else:
#                 lines.append(
#                     f'builder.HasOne(e => e.{nav_prop})'
#                     f'.WithMany()'
#                     f'.HasForeignKey(e => e.{foreign_key});'
#                 )
#         lines.append("        }")
#         lines.append("    }")
#         lines.append("}")

#         config_file = os.path.join(config_path, f"{entity_name}Configuration.cs")
#         create_file(config_file, "\n".join(lines))
