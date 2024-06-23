import logging
from logging.handlers import RotatingFileHandler


class DiscordHandler(logging.handlers.HTTPHandler):
    def __init__(self, url):
        super().__init__('discord.com', '/api/webhooks/'+url, method="POST", secure=True, credentials=None)

    def mapLogRecord(self, record: logging.LogRecord) -> dict:
        self.format(record)
        extraUrl = record.__dict__.get("url")
        result = record.__dict__.get("result")
        fields = [
                        {
                            "name": "Logger Name",
                            "value": record.name,
                            "inline": True
                        },
                        {
                            "name": "Time",
                            "value": record.asctime,
                            "inline": True
                        }
                    ]
        if extraUrl != None:
            fields.append({
                "name": "Download At",
                "value": extraUrl
            })
        
        if result != None:
            fields.append({
                "name": "Status",
                "value": result
            })
        return {
            'embeds': [{
                    'title': record.levelname,
                    'description': record.message[:2048],
                    "color": self.getColor(record.levelname),
                    "fields": fields,
                }]
        }

    def getColor(self, level: str) -> int:
        if level == 'DEBUG':
            return 15258703
        elif level == 'INFO':
            return 15774873
        elif level == 'WARNING':
            return 15105570
        elif level == 'ERROR':
            return 16711680
        elif level == 'CRITICAL':
            return 15158332
        else:
            return 15258703

    def emit(self, record):
        """
        Emit a record.
        Send the record to discord server
        """
        try:
            host = self.host
            h = self.getConnection(host, self.secure)
            import json
            data = json.dumps(self.mapLogRecord(record))
            h.putrequest(self.method, self.url)
            h.putheader("Content-type",
                        "application/json")
            h.putheader("Content-length", str(len(data)))
            h.endheaders()
            h.send(data.encode('utf-8'))
            h.getresponse()  # can't do anything with the result
        except Exception:
            self.handleError(record)

class Filter(logging.Filter):
    def __init__(self, level):
        self.__level = level

    def filter(self, record):
        return record.levelno < self.__level


def config_logger(config: dict) -> None:
    logger = logging.getLogger('chngNotify')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    dh = RotatingFileHandler(
        config['DEBUG_LOG_FILE'], maxBytes=10*1024*1024, backupCount=5)
    dh.setLevel(logging.DEBUG)
    dh.setFormatter(formatter)
    dh.addFilter(Filter(logging.INFO))
    logger.addHandler(dh)

    ih = RotatingFileHandler(
        config['INFO_LOG_FILE'], maxBytes=10*1024*1024, backupCount=5)
    ih.setLevel(logging.INFO)
    ih.setFormatter(formatter)
    ih.addFilter(Filter(logging.ERROR))
    logger.addHandler(ih)

    eh = RotatingFileHandler(
        config['ERROR_LOG_FILE'], maxBytes=10*1024*1024, backupCount=5)
    eh.setLevel(logging.ERROR)
    eh.setFormatter(formatter)
    logger.addHandler(eh)

    discord_silent = DiscordHandler(config['DISCORD_LOG_SILENT'])
    discord_silent.setLevel(logging.DEBUG)
    discord_silent.setFormatter(formatter)
    discord_silent.addFilter(Filter(logging.INFO))
    logger.addHandler(discord_silent)

    discord_verbose = DiscordHandler(config['DISCORD_LOG_ERROR'])
    discord_verbose.setLevel(logging.INFO)
    discord_verbose.setFormatter(formatter)
    logger.addHandler(discord_verbose)
