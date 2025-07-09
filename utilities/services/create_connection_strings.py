import os


def add_connection_string_to_appsettings(base_path, service_name, connection_strings):
    api_path = os.path.join(base_path, "Services", service_name, f"{service_name}.API")
    appsettings_path = os.path.join(api_path, "appsettings.json")

    config = {
        "ConnectionStrings": connection_strings
    }

    import json
    if os.path.exists(appsettings_path):
        with open(appsettings_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = {}

    existing.update(config)

    with open(appsettings_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4)
        print(f"[+] ConnectionStrings añadidas a: {appsettings_path}")
