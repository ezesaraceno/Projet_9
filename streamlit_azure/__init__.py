import logging

import azure.functions as func


def main(req: func.HttpRequest,recommendation: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if not recommendation or len(recommendation) == 0:
        logging.warning("Recommendation item not found")
        return func.HttpResponse(
            "Recommendation item not found",
            status_code=404,
        )

    return func.HttpResponse(
        recommendation[0].to_json(),
        mimetype="application/json",
        status_code=200,
    )
