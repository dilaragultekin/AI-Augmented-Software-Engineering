\# Week 5 — Data Explorer MCP Server Writeup



\## 1. Implementation Summary



I implemented a Data Explorer MCP server using Python, FastMCP, and the open `mledoze/countries` dataset hosted on GitHub.



The server provides two MCP tools:



\- `search\_countries(query, limit=5)`: Searches countries by their common or official names and returns their names, capitals, regions, and subregions.

\- `get\_country\_details(name)`: Retrieves a country's currencies, languages, bordering country codes, and flag URL.



Both tools use the same dataset loader, which caches the downloaded data to avoid unnecessary repeated requests.



\## 2. MCP Client Agent Transcript



I registered the server in Visual Studio Code and tested both tools using GitHub Copilot Chat in Agent mode.



\### Tool Call 1 — search\_countries



\*\*User prompt:\*\*



> Use the data-explorer MCP server's search\_countries tool to search for "Germany" with limit 5. Show the tool's actual response. Do not modify any files.



\*\*Agent response:\*\*



> I’ll call the data-explorer country search with the exact query and limit, then relay its response verbatim.



\*\*Tool invocation:\*\*



```json

{

&#x20; "query": "Germany",

&#x20; "limit": 5

}

```



\*\*Actual MCP tool response:\*\*



```json

{

&#x20; "result": \[

&#x20;   {

&#x20;     "name": "Germany",

&#x20;     "capital": "Berlin",

&#x20;     "region": "Europe",

&#x20;     "subregion": "Western Europe"

&#x20;   }

&#x20; ]

}

```



\### Tool Call 2 — get\_country\_details



\*\*User prompt:\*\*



> Use the data-explorer MCP server's get\_country\_details tool with name "Germany". Show the actual tool response. Do not modify any files.



\*\*Agent response:\*\*



> I’ll request Germany’s country details from the data-explorer tool and show its response exactly as returned.



\*\*Tool invocation:\*\*



```json

{

&#x20; "name": "Germany"

}

```



\*\*Actual MCP tool response (before the flag URL correction):\*\*



```json

{

&#x20; "name": "Germany",

&#x20; "currencies": {

&#x20;   "EUR": {

&#x20;     "name": "Euro",

&#x20;     "symbol": "€"

&#x20;   }

&#x20; },

&#x20; "languages": {

&#x20;   "deu": "German"

&#x20; },

&#x20; "borders": \[

&#x20;   "AUT",

&#x20;   "BEL",

&#x20;   "CZE",

&#x20;   "DNK",

&#x20;   "FRA",

&#x20;   "LUX",

&#x20;   "NLD",

&#x20;   "POL",

&#x20;   "CHE"

&#x20; ],

&#x20; "flag\_url": "https://raw.githubusercontent.com/mledoze/countries/master/data/DEU.svg"

}

```



Both tools were successfully invoked through the MCP client. The original response is preserved above as an accurate record of the agent test. The flag URL formatting was subsequently updated to use lowercase country codes following code review.



\## 3. Error Handling



The implementation includes input validation and exception handling for common failure scenarios.



\*\*Invalid or empty input:\*\* Both tools reject empty strings and invalid input types. The search tool also validates that `limit` is an integer between 1 and 20.



\*\*No matching results:\*\* `search\_countries` returns an empty list, while `get\_country\_details` returns a structured `Country not found` error.



\*\*HTTP failures:\*\* The dataset loader uses `raise\_for\_status()` to detect unsuccessful HTTP responses. The tools catch `httpx.HTTPError` and return structured error messages.



\*\*Timeouts:\*\* The HTTP request has a 30-second timeout. Both tools catch `httpx.TimeoutException`.



\*\*Invalid dataset structures:\*\* The loader checks the downloaded data, and the tools catch relevant data-processing exceptions.



During development, I tested normal country lookups and input validation. I also used Python's `unittest.mock.patch` to simulate an HTTP 500 error and a request timeout without relying on an actual upstream failure.



\## 4. Reflection



This assignment helped me understand how an MCP server exposes selected functionality to an AI coding agent through a structured tool interface. By registering only two country-related tools, I could control which operations the agent was able to perform through my server instead of exposing unrestricted access to the underlying dataset or local environment. Testing the tools in VS Code Copilot Agent mode demonstrated the difference between calling a Python function directly and invoking it through an MCP client. I also learned that input validation, explicit error responses, and a reliable external data source are important for making agent-accessible tools predictable and useful.



