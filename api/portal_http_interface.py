from abc import abstractmethod, ABCMeta

class PortalHttpInterface(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'validate_credentials') and 
                callable(subclass.validate_credentials) or 
                NotImplemented)


    @abstractmethod
    def validate_credentials(self) -> str:
        raise NotImplementedError


 