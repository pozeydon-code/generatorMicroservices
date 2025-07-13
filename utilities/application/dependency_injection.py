
import os
from utilities.filesystem.create_file import create_file

def generate_di_application(app_base, service_name, entities):
    lines = [
        f"using {service_name}.Application.Common.Behaviors;",
        "using Microsoft.Extensions.DependencyInjection;",
        "",
        f"namespace {service_name}.Application;",
        "public static class DependencyInjection",
        "{",
        "    public static IServiceCollection AddApplication(this IServiceCollection services)",
        "    {",
        "        services.AddMediatR(cfg => {",
        "            cfg.RegisterServicesFromAssemblyContaining<ApplicationAssemblyReference>();",
        "        });",
        "",
        "        services.AddScoped(",
        "            typeof(IPipelineBehavior<,>),",
        "            typeof(ValidationBehavior<,>)",
        "        );",
        "",
        "        services.AddValidatorsFromAssemblyContaining<ApplicationAssemblyReference>();",
        '        return services;',
        '    }',
        "",
    ]
    lines.append("}")

    create_file(os.path.join(app_base, "DependencyInjection.cs"), "\n".join(lines))
