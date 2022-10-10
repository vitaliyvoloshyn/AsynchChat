import logging

from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler


class Logging:


    def create_logger(self):
        format = logging.Formatter("%(asctime)-10s [%(levelname)s] %(module)s %(message)s ")
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        self.handler.setFormatter(format)
        logger.addHandler(self.handler)
        return logger

class ClientLog(Logging):
    handler = TimedRotatingFileHandler(
        filename='client.log', when="midnight", encoding='utf-8'
    )


class ServerLog(Logging):
    handler = logging.FileHandler(
        filename='server.log', encoding='utf-8'
    )


class FunctionCallLog(Logging):

    # Logging.logger.propagate = False
    handler = logging.FileHandler(filename='function_call.log', encoding='utf-8')
