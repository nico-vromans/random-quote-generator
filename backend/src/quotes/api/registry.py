from .clients import APINinjaQuoteAPIClient, ProgrammingQuoteAPIClient, ZenQuoteAPIClient

API_CLIENTS = {
    'api_ninja_quote_api_client': APINinjaQuoteAPIClient(),
    'programming_quote_api_client': ProgrammingQuoteAPIClient(),
    'zen_quote_api_client': ZenQuoteAPIClient(),
}
