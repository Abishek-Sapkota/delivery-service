from django.utils.deprecation import MiddlewareMixin
from django.db import connections, connection as con


class SetupSchemaNameMiddleware(MiddlewareMixin):
    def process_request(self, request):
        for alias in connections:
            if alias not in ["service_control", "default"]:
                connection = connections[alias]
                connection_options = connection.settings_dict.get("OPTIONS", {})
                connection_options["options"] = f"-c search_path={con.schema_name}"
                connection.settings_dict["OPTIONS"] = connection_options


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        with connections["service_control"].cursor() as cursor:
            cursor.execute(
                "SELECT timezone FROM client_client WHERE schema_name = %s",
                [request.tenant.schema_name]
            )
            try:
                row = cursor.fetchone()
                if row:
                    tz = row[0]
                else:
                    from pytz import timezone
                    tz = timezone('UTC')
            except Exception as e:
                from pytz import timezone
                tz = timezone('UTC')
            import django.utils.timezone
            if tz:
                django.utils.timezone.activate(tz)
            else:
                django.utils.timezone.deactivate()
