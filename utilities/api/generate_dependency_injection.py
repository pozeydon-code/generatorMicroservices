import os
from utilities.filesystem.create_file import create_file


def generate_di_api(base_path, service_name):
    lines = [
        f"using {service_name}.API.Middlewares;",
        "",
        f"namespace {service_name}.API;",
        "public static class DependencyInjection",
        "{",
        "    public static IServiceCollection AddPresentation(this IServiceCollection services)",
        "    {",
        '        services.AddControllers();',
        '        services.AddEndpointsApiExplorer();',
        '        services.AddSwaggerGen();',
        '        services.AddTransient<GlobalExceptionHandlingMiddleware>();',
        '        return services;',
        '    }',
        '}',
    ]

    create_file(os.path.join(base_path, "DependencyInjection.cs"), "\n".join(lines))
