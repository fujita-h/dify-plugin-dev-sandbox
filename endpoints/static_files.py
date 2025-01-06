import os
from typing import Mapping

from dify_plugin import Endpoint
from werkzeug import Request, Response


class StaticFilesEndpoint(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        p1 = values.get("p1", "index.html")
        p2 = values.get("p2", "")
        p3 = values.get("p3", "")
        p4 = values.get("p4", "")
        p5 = values.get("p5", "")

        paths = [p for p in [p1, p2, p3, p4, p5] if p]
        base_path = os.path.join(os.path.dirname(__file__), "static")

        requested_path = os.path.join(*paths)
        full_requested_path = os.path.join(base_path, requested_path)

        # check if file exists
        if not os.path.exists(full_requested_path):
            return Response("Not found", status=404, content_type="text/html")

        # check if file is a directory
        if os.path.isdir(full_requested_path):
            return Response("Forbidden", status=403, content_type="text/html")

        # check directory traversal
        if not full_requested_path.startswith(base_path):
            return Response("Forbidden", status=403, content_type="text/html")

        # read file
        with open(full_requested_path, "rb") as f:
            content = f.read()

        # get file extension
        _, extension = os.path.splitext(full_requested_path)
        extension = extension[1:]

        # set content type
        content_type = "application/octet-stream"
        if extension == "html" or extension == "htm":
            content_type = "text/html"
        elif extension == "css":
            content_type = "text/css"
        elif extension == "js":
            content_type = "application/javascript"
        elif extension == "png":
            content_type = "image/png"
        elif extension == "jpg" or extension == "jpeg":
            content_type = "image/jpeg"
        elif extension == "gif":
            content_type = "image/gif"
        elif extension == "svg":
            content_type = "image/svg+xml"
        elif extension == "ico":
            content_type = "image/x-icon"

        return Response(content, status=200, content_type=content_type)
