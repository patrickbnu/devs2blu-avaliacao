class PortalIssue(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.message = message
        self.errors = errors

    def __repr__(self):
        return f'PortalIssue("{self.message}","{self.errors}")'

    def __str__(self):
        return f"{self.message}: {self.errors}"
