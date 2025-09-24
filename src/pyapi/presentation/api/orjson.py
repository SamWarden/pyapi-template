import logging
from uuid import UUID

import orjson
import pydantic
from fastapi.responses import ORJSONResponse as _ORJSONResponse

logger = logging.getLogger(__name__)


def additionally_serialize(obj: object) -> object:
    match obj:
        case UUID() as obj:
            return str(obj)
        case pydantic.BaseModel() as obj:
            return obj.dict()

    logger.warning("Type is not JSON serializable: %s", type(obj), extra={"obj": repr(obj)})
    return repr(obj)


class ORJSONResponse(_ORJSONResponse):
    def render(self, content: object) -> bytes:
        result: bytes = orjson.dumps(
            content,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_DATACLASS | orjson.OPT_SERIALIZE_UUID,
            default=additionally_serialize,
        )
        return result
