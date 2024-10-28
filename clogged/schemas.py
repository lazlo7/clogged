from typing import Annotated
from annotated_types import Lt
from pydantic import NonNegativeInt


# Non-negative integer type up to 2**31 - 1, following postgres' integer upper limit. 
# Used for representing ids for posts, posters, etc.
IdType = Annotated[NonNegativeInt, Lt(2**31)]
