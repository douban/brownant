from brownant import Brownant, BrownAnt


def test_deprecation(recwarn):
    app = BrownAnt()
    warning = recwarn.pop(DeprecationWarning)

    assert isinstance(app, Brownant)
    assert issubclass(warning.category, DeprecationWarning)
    assert "Brownant" in str(warning.message)
    assert "app.py" in warning.filename
    assert warning.lineno
