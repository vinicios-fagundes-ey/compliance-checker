class ComplianceError(Exception):
    pass


class RetrievalError(ComplianceError):
    pass


class LLMServiceError(ComplianceError):
    pass