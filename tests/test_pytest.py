from tests import generate_random_bases
from tests import t_br2d, t_brlll
import  pytest

@pytest.mark.parametrize("bases", generate_random_bases(10, 2))
def test_pytest_br2d(bases):
    test_n = t_br2d([bases], False)

    assert test_n[0]["result"] == 1


@pytest.mark.parametrize("bases", generate_random_bases(10, 2))
def test_pytest_brlll(bases):
    test_n = t_brlll([bases], False)

    assert test_n[0]["result"] == 1

