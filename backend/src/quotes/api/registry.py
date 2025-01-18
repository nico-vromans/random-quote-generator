from .clients import APINinjaQuoteAPIClient, ProgrammingQuoteAPIClient, ZenQuoteAPIClient

API_CLIENTS = {
    APINinjaQuoteAPIClient().api_client_key: APINinjaQuoteAPIClient(),
    ProgrammingQuoteAPIClient().api_client_key: ProgrammingQuoteAPIClient(),
    ZenQuoteAPIClient().api_client_key: ZenQuoteAPIClient(),
}
