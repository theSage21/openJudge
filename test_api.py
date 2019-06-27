from hypothesis import given
import hypothesis.strategies as st
import requests as R


def api(x):
    return f"http://localhost:8080/{x}"


@given(name=st.text(), pwd=st.text())
def test_register_works(name, pwd):
    r = R.post(api("/register"), json={"name": name, "pwd": pwd})
    assert r.status_code == 200, r.text
