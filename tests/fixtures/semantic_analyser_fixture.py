"""Fixture for semantic analysis"""
import pandas as pd
import pytest

from data.models.basic_models import Document
from data.services.semantic import SemanticAnalyser


@pytest.fixture(name="_load_semantic_document_fixture")
def load_semantic_document_fixture():
    """
    Fixture to upload a document
    """
    document = Document.objects.create(
        name="semantic_analyser_source", document_path="semantic_analyser_source.csv"
    )
    return document


@pytest.fixture(name="_read_semantic_document_fixture")
def read_semantic_document_fixture(_load_semantic_document_fixture):
    """
    Fixture to load a document into a dataframe
    """
    document = _load_semantic_document_fixture
    df = (pd.read_csv("tests\\data\\data_test\\semantic_analyser_source.csv", sep=";"),)
    data = pd.DataFrame(*df)
    return (data, document)


@pytest.fixture(name="_semantic_doc_analyser_fixture")
def semantic_doc_analyser_fixture(_read_semantic_document_fixture):
    """
    Fixture to create a Semantic Analyser instance
    """
    data, doc = _read_semantic_document_fixture
    doc = SemanticAnalyser(data, doc.id)
    return doc
