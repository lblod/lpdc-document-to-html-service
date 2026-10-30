from utils.constants import TASK_STATUSES


ADMS_STATUS = "http://www.w3.org/ns/adms#status"


class InvalidDeltaError(ValueError):
    pass


def extract_scheduled_task_uris(delta):
    if not isinstance(delta, list):
        raise InvalidDeltaError(
            "Expected delta payload to be a list"
        )

    task_uris = []

    for changeset in delta:
        if not isinstance(changeset, dict):
            raise InvalidDeltaError(
                "Expected each changeset to be an object"
            )

        inserts = changeset.get("inserts", [])

        if not isinstance(inserts, list):
            raise InvalidDeltaError(
                "Expected changeset inserts to be a list"
            )

        for insert in inserts:
            if _is_scheduled_task_status(insert):
                task_uris.append(
                    insert["subject"]["value"]
                )

    return list(dict.fromkeys(task_uris))


def _is_scheduled_task_status(insert):
    try:
        return (
            insert["subject"]["type"] == "uri"
            and insert["predicate"]["value"] == ADMS_STATUS
            and insert["object"]["type"] == "uri"
            and insert["object"]["value"]
            == TASK_STATUSES["SCHEDULED"]
        )
    except (KeyError, TypeError):
        return False