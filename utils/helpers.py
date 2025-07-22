import uuid


class Helpers:
    """Utility class for various helper functions"""
    @staticmethod
    def guid():
        """Generate a unique identifier"""
        return str(uuid.uuid4())