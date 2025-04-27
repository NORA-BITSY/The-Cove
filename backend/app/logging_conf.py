from logging.config import dictConfig

dictConfig({
  "version": 1,
  "formatters": {
    "json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"}
  },
  "handlers": {
    "default": {
      "class": "logging.StreamHandler",
      "formatter": "json"
    }
  },
  "root": {"handlers": ["default"], "level": "INFO"}
})
