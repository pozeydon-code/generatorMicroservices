import os
from utilities.filesystem.create_file import create_file


def generate_db_initializer(service_name, persistence_path, entities):
    lines = [
        "using Microsoft.EntityFrameworkCore;",
        f"using {service_name}.Domain.Entities;",
        f"using {service_name}.Domain.ValueObjects;",
        "",
        f"namespace {service_name}.Infrastructure.Persistence",
        "{",
        "    public static class DbInitializer",
        "    {",
        "        public static async Task InitializeAsync(AppDbContext context)",
        "        {",
        "            await context.Database.MigrateAsync();",
        ""
    ]

    if "Category" in entities and "Product" in entities:
        lines += [
            "            if (!context.Categorys.Any())",
            "            {",
            "                var defaultCategory = new Category",
            "                {",
            "                    Id = Guid.NewGuid(),",
            '                    Name = Name.Create("Tecnología")!,',
            '                    Description = Description.Create("Productos electrónicos")!,',
            "                    Products = new List<Product>()",
            "                };",
            "",
            "                var product = new Product",
            "                {",
            "                    Id = Guid.NewGuid(),",
            '                    Name = Name.Create("Laptop HP")!,',
            '                    Description = Description.Create("Portátil con 16GB RAM")!,',
            "                    Price = ProductPrice.Create(999.99m)!,",
            "                    Stock = 10,",
            "                    CategoryId = defaultCategory.Id,",
            "                    CategoryNavigation = defaultCategory",
            "                };",
            "",
            "                context.Categorys.Add(defaultCategory);",
            "                context.Products.Add(product);",
            "                await context.SaveChangesAsync();",
            "            }"
        ]

    lines += [
        "        }",
        "    }",
        "}"
    ]

    create_file(os.path.join(persistence_path, "DbInitializer.cs"), "\n".join(lines))
