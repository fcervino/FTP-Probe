# -*- coding: utf-8 -*-

import os

INFLUXDB_BACKEND_SETTINGS = {
    "host": os.getenv("EVIDENCEDB_HOST", "localhost"),
    "port": os.getenv("EVIDENCEDB_PORT", 8086),
    "database_name": os.getenv("EVIDENCEDB_NAME", "mooncloud_evidence"),
    "username": os.getenv("EVIDENCEDB_USERNAME", "mooncloud"),
    "password": os.getenv("EVIDENCEDB_PASSWORD", "mooncloud"),
    "use_udp": os.getenv("EVIDENCEDB_UDP_ENABLED", None),
    "udp_port": os.getenv("EVIDENCEDB_UDP_PORT", None),
    "use_ssl": os.getenv("EVIDENCEDB_SSL_ENABLED", None),
    "verify_ssl": os.getenv("EVIDENCEDB_SSL_VERIFY", None),

    "short_retention": os.getenv("SHORT_RETENTION", "short"),
    "long_retention": os.getenv("LONG_RETENTION", None)
}
TEST_ID = os.getenv("TEST_ID", '0')
REDIS_SERVER = os.getenv("REDIS_SERVER", "localhost")
