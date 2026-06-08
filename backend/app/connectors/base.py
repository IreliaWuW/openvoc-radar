from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConnectorTicket:
    source: str
    ticket_id: str
    user_id: str
    user_email: str | None
    created_at: datetime
    subject: str
    body: str
    product_area: str | None = None
    tags: str | None = None


class TicketConnector(ABC):
    name: str

    @abstractmethod
    async def fetch_tickets(self) -> list[ConnectorTicket]:
        """Fetch tickets from a source system."""
