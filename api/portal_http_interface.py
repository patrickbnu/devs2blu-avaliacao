from abc import abstractmethod, ABCMeta

### TODO no momento não utilizado
class PortalHttpInterface(metaclass=ABCMeta):
    
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'login') and 
                callable(subclass.login) or 
                NotImplemented)


    @abstractmethod
    def login(self) -> str:
        raise NotImplementedError


 