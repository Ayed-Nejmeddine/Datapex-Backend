"""Here test abstracts"""
import numpy as np
import pytest

from data.models import M106_9
from data.models import M107_10
from data.models.basic_models import SyntacticResult
from data.services.syntactic import StringAnalyser


@pytest.mark.django_db
def test_get_model_data_frequency(_element_fixture):
    """Test get model data frequency"""
    service, document = _element_fixture(
        name="test_string.csv", path="test_string.csv", service=StringAnalyser
    )
    res_model, res_percentage, res_occ = service.model_data_frequency()
    # Testing the result of model data frequency
    assert res_model[0][0][0] == "AAAA"
    assert res_model[0][0][1] == "AAAAAA"
    assert res_model[0][0][2] == "AAA"
    assert res_model[0][0][3] == "AAAAAAAA"
    assert res_model[1] == "None"
    assert res_model[2][0][0] == "AAAAAA"
    assert res_model[2][0][1] == "AAAA"
    assert res_model[3][0][0] == "AAAAAAA"
    assert res_model[3][0][1] == "AAA AAAA"
    assert res_model[3][0][2] == "AAA AAAAAAA"
    assert res_model[3][0][3] == "AAAAAAAAAAAA"
    assert res_model[4] == "None"

    # Check if the result was saved in the database
    syntactic_result1 = SyntacticResult.objects.get(document=document, rule=M107_10)
    assert syntactic_result1.result == {
        "Name": [["AAAA", "AAAAAA", "AAA", "AAAAAAAA"]],
        "Age": "None",
        "Gender": [["AAAAAA", "AAAA"]],
        "City": [["AAAAAAA", "AAA AAAA", "AAA AAAAAAA", "AAAAAAAAAAAA"]],
        "Salary": "None",
    }

    # Testing the result of data frequency
    assert res_percentage[0][0] == 40.0
    assert res_percentage[0][1] == 30.0
    assert res_percentage[0][2] == 20.0
    assert res_percentage[0][3] == 10.0
    assert res_percentage[1] == 0
    assert res_percentage[2][0] == 60.0
    assert res_percentage[2][1] == 40.0
    assert res_percentage[3][0] == 40.0
    assert res_percentage[3][1] == 30.0
    assert res_percentage[3][2] == 20.0
    assert res_percentage[3][3] == 10.0
    assert res_percentage[4] == 0

    assert res_occ[0][0] == 4
    assert res_occ[0][1] == 3
    assert res_occ[0][2] == 2
    assert res_occ[0][3] == 1
    assert res_occ[1] == 0
    assert res_occ[2][0] == 6
    assert res_occ[2][1] == 4
    assert res_occ[3][0] == 4
    assert res_occ[3][1] == 3
    assert res_occ[3][2] == 2
    assert res_occ[3][3] == 1
    assert res_occ[4] == 0

    # Check if the result was saved in the database
    syntactic_result2 = SyntacticResult.objects.get(document=document, rule=M106_9)
    assert syntactic_result2.result == {
        "Name": [[4, 3, 2, 1], [40.0, 30.0, 20.0, 10.0]],
        "Age": [0, 0],
        "Gender": [[6, 4], [60.0, 40.0]],
        "City": [[4, 3, 2, 1], [40.0, 30.0, 20.0, 10.0]],
        "Salary": [0, 0],
    }


@pytest.mark.django_db
def test_count_null_type_values(_abstract_document_fixture):
    """Test count null type values"""
    result = _abstract_document_fixture.count_null_values_by_type()
    expected_result = np.array([0, 0, 0, 2], dtype=object)
    assert np.array_equal(result, expected_result)
