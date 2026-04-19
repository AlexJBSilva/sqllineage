import pytest

from ...helpers import assert_table_lineage_equal


@pytest.mark.parametrize("dialect", ["bigquery"])
def test_procedure_bigquery(dialect: str):
    sql = """CREATE PROCEDURE db1.proc1()
BEGIN
INSERT INTO tab2 (col1)
SELECT col1 FROM tab1;
END"""
    assert_table_lineage_equal(
        sql,
        {"tab1"},
        {"db1.proc1", "tab2"},
        dialect,
        test_sqlparse=False,
    )


@pytest.mark.parametrize("dialect", ["bigquery"])
def test_procedure_multiple_statements_bigquery(dialect: str):
    sql = """CREATE PROCEDURE proc1()
BEGIN
INSERT INTO tab2 (col1)
SELECT col1 FROM tab1;
INSERT INTO tab3 (col2)
SELECT col2 FROM tab2;
END"""
    assert_table_lineage_equal(
        sql,
        {"tab1", "tab2"},
        {"proc1", "tab2", "tab3"},
        dialect,
        test_sqlparse=False,
    )