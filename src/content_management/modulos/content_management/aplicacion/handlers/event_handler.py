"""Event Handler Port for Hexagonal Architecture

This file defines the port (interface) for handling events in the application layer.
This follows hexagonal architecture principles by defining the contract that
infrastructure adapters must implement.

"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class EventHandler(ABC):
    """Port for handling domain events"""
    
    @abstractmethod
    def handle_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """
        Handle a domain event
        
        Args:
            event_type: The type of event being handled
            event_data: The event payload data
            
        Raises:
            Exception: If event handling fails
        """
        raise NotImplementedError()
