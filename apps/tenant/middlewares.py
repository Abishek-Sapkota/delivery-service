from django.http import Http404
from django.db import connection, connections, ProgrammingError
from django_tenants.middleware import TenantMainMiddleware
from django.conf import settings

from apps.tenant.models import Client
from utils.helpers import namedtuplefetchall

import logging

logger = logging.getLogger(__name__)


class DibERPTenantMiddleware(TenantMainMiddleware):
    TENANT_NOT_FOUND_EXCEPTION = Http404
    """
    This middleware should be placed at the very top of the middleware stack.
    Selects the proper database schema using the request host. Can fail in
    various ways which is better than corrupting or revealing data.
    """

    def get_schema_name(self, domain_name):

        with connections['service_control'].cursor() as cursor:
            try:
                cursor.execute(
                    f"SELECT client_domain.domain,client_client.schema_name,"
                    f" client_client.name FROM client_domain ,client_client "
                    f"WHERE  client_domain.client_id =client_client.id AND "
                    f"client_domain.domain='{domain_name}';"
                )
            except ProgrammingError as e:
                return False, "Client Doesn't exists"
            client = namedtuplefetchall(cursor)[0]
            if client:
                return client.schema_name, client.name
            return False, "Client Doesn't exists"

    def process_request(self, request):
        connection.set_schema_to_public()
        try:
            hostname = request.META["HTTP_ORIGIN"].split("//")[1]
        except KeyError:
            hostname = settings.HOSTNAME
        if hostname.startswith("www"):
            hostname = hostname[4:]
        logger.info(f"Hostname {hostname}")
        hostname = hostname.split(":")[0]
        schema_name, client_name = "initial_tenant", "dev_client"
        if hostname not in ["localhost", "127.0.0.1", settings.HOSTNAME]:
            schema_name, client_name = self.get_schema_name(hostname)
        if not schema_name:
            self.no_tenant_found(request, hostname)
            return
        try:
            tenant = Client.objects.get(schema_name=schema_name)
        except Client.DoesNotExist:
            tenant = Client.objects.create(schema_name=schema_name, name=client_name)
        request.tenant = tenant
        connection.set_tenant(request.tenant)
        self.setup_url_routing(request)
