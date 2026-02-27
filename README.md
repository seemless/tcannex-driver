# tcannex

A Python driver for the TCAnnex CPRT (Cybersecurity and Privacy Reference Tool) API.

## Installation

```bash
pip install tcannex
```

## Quick Start

Set your API key as an environment variable:

```bash
export TCANNEX_API_KEY="your-api-key"
```

Use the client:

```python
from tcannex import TCAnnexClient

with TCAnnexClient() as client:
    # List all documents
    response = client.get_documents()
    for doc in response.documents:
        print(f"{doc.name} (v{doc.version})")

    # Get a specific document with its elements and relationships
    response = client.get_document("NIST_CSF_2.0")
    for element in response.elements:
        print(f"  {element.element_identifier}: {element.title}")

    # Get a specific element
    response = client.get_element("NIST_CSF_2.0", "GV")
    print(response.elements[0].text)
```

You can also pass the API key directly:

```python
client = TCAnnexClient(api_key="your-api-key")
```

## API Reference

### Client

**`TCAnnexClient(api_key=None, base_url="https://api.tcannex.com")`**

| Method | Description |
|---|---|
| `get_root()` | Read API root |
| `get_documents()` | List all documents |
| `get_document(document_identifier)` | Get a document with its elements, relationships, and relationship types |
| `get_element(document_identifier, element_identifier)` | Get an element with its document, relationships, and relationship types |
| `close()` | Close the HTTP client |

All methods return a `CPRTResponse`.

### Models

- **`CPRTResponse`** — `documents`, `elements`, `relationship_types`, `relationships`
- **`Document`** — `doc_identifier`, `name`, `version`, `website`
- **`Element`** — `doc_identifier`, `element_type`, `element_identifier`, `title`, `text`
- **`Relationship`** — `source_element_identifier`, `source_doc_identifier`, `dest_element_identifier`, `dest_doc_identifier`, `provenance_doc_identifier`, `relationship_identifier`
- **`RelationshipType`** — `relationship_identifier`, `description`, `value`

### Exceptions

- **`TCAnnexError`** — Base exception
- **`AuthenticationError`** — Missing or invalid API key
- **`APIError`** — Non-2xx response (has `status_code` and `body` attributes)

## License

MIT
