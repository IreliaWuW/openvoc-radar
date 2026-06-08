from app.connectors.base import ConnectorTicket, TicketConnector


class IntercomConnector(TicketConnector):
    name = "intercom"

    async def fetch_tickets(self) -> list[ConnectorTicket]:
        # MVP skeleton: wire the Intercom Conversations API here.
        return []
