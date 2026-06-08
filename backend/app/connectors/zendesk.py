from app.connectors.base import ConnectorTicket, TicketConnector


class ZendeskConnector(TicketConnector):
    name = "zendesk"

    async def fetch_tickets(self) -> list[ConnectorTicket]:
        # MVP skeleton: wire the Zendesk Tickets API here.
        return []
