from pydantic import BaseModel


class Document(BaseModel):
    doc_identifier: str
    name: str
    version: str
    website: str


class Element(BaseModel):
    doc_identifier: str
    element_type: str
    element_identifier: str
    title: str
    text: str


class Relationship(BaseModel):
    source_element_identifier: str
    source_doc_identifier: str
    dest_element_identifier: str
    dest_doc_identifier: str
    provenance_doc_identifier: str
    relationship_identifier: str


class RelationshipType(BaseModel):
    relationship_identifier: str
    description: str
    value: str


class CPRTResponse(BaseModel):
    documents: list[Document] = []
    elements: list[Element] = []
    relationship_types: list[RelationshipType] = []
    relationships: list[Relationship] = []
