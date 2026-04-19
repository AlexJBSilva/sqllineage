import pytest

from sqllineage.utils.entities import ColumnQualifierTuple

from ...helpers import assert_column_lineage_equal


@pytest.mark.parametrize("dialect", ["bigquery"])
def test_procedure_bigquery_column(dialect: str):
    sql = """CREATE PROCEDURE db1.proc1()
BEGIN
INSERT INTO tab2 (col1)
SELECT col1 FROM tab1;
END"""
    assert_column_lineage_equal(
        sql,
        [(ColumnQualifierTuple("col1", "tab1"), ColumnQualifierTuple("col1", "tab2"))],
        dialect,
        test_sqlparse=False,
    )


@pytest.mark.parametrize("dialect", ["mysql"])
def test_procedure_mysql_column(dialect: str):
    sql = """CREATE PROCEDURE proc1()
BEGIN
INSERT INTO tab2 (col1)
SELECT col1 FROM tab1;
END"""
    assert_column_lineage_equal(
        sql,
        [(ColumnQualifierTuple("col1", "tab1"), ColumnQualifierTuple("col1", "tab2"))],
        dialect,
        test_sqlparse=False,
    )


@pytest.mark.parametrize("dialect", ["oracle"])
def test_procedure_oracle_column(dialect: str):
    sql = """CREATE OR REPLACE PROCEDURE proc1
IS
BEGIN
INSERT INTO tab2 (col1)
SELECT col1 FROM tab1;
END;"""
    assert_column_lineage_equal(
        sql,
        [(ColumnQualifierTuple("col1", "tab1"), ColumnQualifierTuple("col1", "tab2"))],
        dialect,
        test_sqlparse=False,
    )


@pytest.mark.parametrize("dialect", ["bigquery"])
def test_procedure_bigquery_multiple_statements_column(dialect: str):
    sql = """CREATE PROCEDURE proc1()
BEGIN
INSERT INTO tab2 (col1)
SELECT col1 FROM tab1;
INSERT INTO tab3 (col2)
SELECT col2 FROM tab2;
END"""
    assert_column_lineage_equal(
        sql,
        [
            (
                ColumnQualifierTuple("col1", "tab1"),
                ColumnQualifierTuple("col1", "tab2"),
            ),
            (
                ColumnQualifierTuple("col2", "tab2"),
                ColumnQualifierTuple("col2", "tab3"),
            ),
        ],
        dialect,
        test_sqlparse=False,
    )
