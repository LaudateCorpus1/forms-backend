"""
Index route for the forms API.
"""
from pydantic import BaseModel
from pydantic.fields import Field
from spectree import Response
from starlette.requests import Request
from starlette.responses import JSONResponse

from backend.route import Route
from backend.validation import api


class IndexResponse(BaseModel):
    message: str = Field(description="A hello message")
    client: str = Field(
        description=(
            "The connecting client, in production this will"
            " be an IP of our internal load balancer"
        )
    )


class IndexRoute(Route):
    """
    Return a generic hello world message with some information to the client.

    Can be used as a healthcheck for Kubernetes or a frontend connection check.
    """

    name = "index"
    path = "/"

    @api.validate(resp=Response(HTTP_200=IndexResponse))
    def get(self, request: Request) -> JSONResponse:
        """
        Return a hello from Python Discord forms!
        """
        response_data = {
            "message": "Hello, world!",
            "client": request.client.host,
            "user": {
                "authenticated": False
            }
        }

        if request.user.is_authenticated:
            response_data["user"] = {
                "authenticated": True,
                "user": request.user.payload,
                "scopes": request.auth.scopes
            }

        return JSONResponse(response_data)
