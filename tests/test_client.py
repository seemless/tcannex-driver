import json
from unittest.mock import MagicMock, patch

import httpx
import pytest

from tcannex import TCAnnexClient
from tcannex.exceptions import APIError, AuthenticationError
from tcannex.models import CPRTResponse

SAMPLE_RESPONSE = {
    "documents": [
        {
            "doc_identifier": "NIST_CSF_2.0",
            "name": "NIST Cybersecurity Framework",
            "version": "2.0",
            "website": "https://www.nist.gov/cyberframework",
        }
    ],
    "elements": [
        {
            "doc_identifier": "NIST_CSF_2.0",
            "element_type": "function",
            "element_identifier": "GV",
            "title": "Govern",
            "text": "Establish and monitor cybersecurity risk management strategy.",
        }
    ],
    "relationship_types": [
        {
            "relationship_identifier": "mapped_to",
            "description": "Maps one element to another",
            "value": "mapped_to",
        }
    ],
    "relationships": [
        {
            "source_element_identifier": "GV",
            "source_doc_identifier": "NIST_CSF_2.0",
            "dest_element_identifier": "ID.AM-1",
            "dest_doc_identifier": "NIST_CSF_2.0",
            "provenance_doc_identifier": "NIST_CSF_2.0",
            "relationship_identifier": "mapped_to",
        }
    ],
}


class TestAuthenticationError:
    def test_missing_api_key_raises_error(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(AuthenticationError, match="TCANNEX_API_KEY"):
                TCAnnexClient()

    def test_api_key_from_env(self):
        with patch.dict("os.environ", {"TCANNEX_API_KEY": "test-key"}):
            client = TCAnnexClient()
            assert client._client.headers["authorization"] == "Bearer test-key"
            client.close()

    def test_api_key_from_param(self):
        client = TCAnnexClient(api_key="param-key")
        assert client._client.headers["authorization"] == "Bearer param-key"
        client.close()


class TestClientMethods:
    @pytest.fixture()
    def client(self):
        c = TCAnnexClient(api_key="test-key")
        yield c
        c.close()

    def _mock_response(self, status_code=200, data=None):
        mock = MagicMock(spec=httpx.Response)
        mock.status_code = status_code
        mock.json.return_value = data or SAMPLE_RESPONSE
        mock.text = json.dumps(data or SAMPLE_RESPONSE)
        return mock

    def test_get_root(self, client):
        with patch.object(client._client, "request", return_value=self._mock_response()) as mock_req:
            result = client.get_root()
            mock_req.assert_called_once_with("GET", "/")
            assert isinstance(result, CPRTResponse)
            assert len(result.documents) == 1
            assert result.documents[0].doc_identifier == "NIST_CSF_2.0"

    def test_get_documents(self, client):
        with patch.object(client._client, "request", return_value=self._mock_response()) as mock_req:
            result = client.get_documents()
            mock_req.assert_called_once_with("GET", "/documents")
            assert isinstance(result, CPRTResponse)

    def test_get_document(self, client):
        with patch.object(client._client, "request", return_value=self._mock_response()) as mock_req:
            result = client.get_document("NIST_CSF_2.0")
            mock_req.assert_called_once_with("GET", "/documents/NIST_CSF_2.0")
            assert isinstance(result, CPRTResponse)

    def test_get_element(self, client):
        with patch.object(client._client, "request", return_value=self._mock_response()) as mock_req:
            result = client.get_element("NIST_CSF_2.0", "GV")
            mock_req.assert_called_once_with("GET", "/elements/NIST_CSF_2.0/GV")
            assert isinstance(result, CPRTResponse)

    def test_api_error_on_non_2xx(self, client):
        with patch.object(client._client, "request", return_value=self._mock_response(status_code=403, data={"detail": "Forbidden"})):
            with pytest.raises(APIError) as exc_info:
                client.get_documents()
            assert exc_info.value.status_code == 403

    def test_context_manager(self):
        with TCAnnexClient(api_key="ctx-key") as client:
            assert client._client.headers["authorization"] == "Bearer ctx-key"


class TestModelParsing:
    def test_empty_response(self):
        resp = CPRTResponse.model_validate({})
        assert resp.documents == []
        assert resp.elements == []
        assert resp.relationship_types == []
        assert resp.relationships == []

    def test_full_response(self):
        resp = CPRTResponse.model_validate(SAMPLE_RESPONSE)
        assert len(resp.documents) == 1
        assert resp.documents[0].name == "NIST Cybersecurity Framework"
        assert len(resp.elements) == 1
        assert resp.elements[0].element_type == "function"
        assert len(resp.relationship_types) == 1
        assert resp.relationship_types[0].value == "mapped_to"
        assert len(resp.relationships) == 1
        assert resp.relationships[0].dest_element_identifier == "ID.AM-1"
