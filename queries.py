import logging
import os
import time
from datetime import datetime, timezone

from SPARQLWrapper import JSON, SPARQLWrapper


logger = logging.getLogger(__name__)

sparql_query = SPARQLWrapper(
    os.environ.get("MU_SPARQL_ENDPOINT"),
    returnFormat=JSON,
)
sparql_query.addCustomHttpHeader("mu-auth-sudo", "true")

sparql_update = SPARQLWrapper(
    os.environ.get("MU_SPARQL_UPDATEPOINT"),
    returnFormat=JSON,
)
sparql_update.method = "POST"
sparql_update.addCustomHttpHeader("mu-auth-sudo", "true")


def query(query_string):
    start = time.time()

    logger.debug(f"started query at {datetime.now(timezone.utc)}")
    logger.debug("execute query:\n" + query_string)

    sparql_query.setQuery(query_string)
    result = sparql_query.query().convert()

    logger.debug(f"query took {time.time() - start} seconds")
    return result


def update(query_string):
    sparql_update.setQuery(query_string)

    if not sparql_update.isSparqlUpdateRequest():
        return

    start = time.time()

    logger.debug(f"started update at {datetime.now(timezone.utc)}")
    logger.debug("execute update:\n" + query_string)

    sparql_update.query()

    logger.debug(f"update took {time.time() - start} seconds")