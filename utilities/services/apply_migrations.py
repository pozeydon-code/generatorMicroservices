import os

from utilities.system.run_command import run_command

def add_and_apply_migrations(base_path, service_name):
    try:
        """
        Genera la migración inicial y aplica la actualización de BD
        para el microservicio dado, usando EF Core CLI.
        """
        # Ruta al proyecto Infrastructure
        infra_path = os.path.join(
            base_path,
            "Services",
            service_name,
            f"{service_name}.Infrastructure"
        )
        infra_csproj = f"{service_name}.Infrastructure.csproj"
        migrations_dir = "Persistence/Migrations"

        run_command(
            f'dotnet ef migrations add InitialCreate '
            f'--project {infra_csproj} '
            f'--startup-project ../{service_name}.API/{service_name}.API.csproj '
            f'--output-dir {migrations_dir}',
            cwd=infra_path
        )

        # 2) Aplicar todas las migraciones pendientes a la base de datos
        run_command(
            f'dotnet ef database update '
            f'--project {infra_csproj} '
            f'--startup-project ../{service_name}.API/{service_name}.API.csproj',
            cwd=infra_path
        )
    except Exception as e:
        print(f"Error al aplicar migraciones: {e}")
