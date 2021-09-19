import enum

class StatusEnum(enum.Enum):
    processing = 'processing'
    completed = 'completed'
    canceled = 'canceled'
    failed = 'failed'
    error = 'error'