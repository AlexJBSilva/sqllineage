from sqllineage.utils.entities import ColumnQualifierTuple

from ...helpers import assert_column_lineage_equal


def test_procedure_select_column():
    sql = """CREATE PROCEDURE proc1()
BEGIN
INSERT INTO tab2 (col1)
SELECT col1 FROM tab1;
END"""
    assert_column_lineage_equal(
        sql,
        [(ColumnQualifierTuple("col1", "tab1"), ColumnQualifierTuple("col1", "tab2"))],
        dialect="bigquery",
        test_sqlparse=False,
    )


def test_procedure_select_column_rename():
    sql = """CREATE PROCEDURE proc1()
BEGIN
INSERT INTO tab2 (col2)
SELECT col1 AS col2 FROM tab1;
END"""
    assert_column_lineage_equal(
        sql,
        [(ColumnQualifierTuple("col1", "tab1"), ColumnQualifierTuple("col2", "tab2"))],
        dialect="bigquery",
        test_sqlparse=False,
    )


def test_procedure_multiple_columns():
    sql = """CREATE PROCEDURE proc1()
BEGIN
INSERT INTO tab2 (col1, col2)
SELECT a.col1, b.col2 FROM tab1 a, tab1 b;
END"""
    assert_column_lineage_equal(
        sql,
        [
            (ColumnQualifierTuple("col1", "tab1"), ColumnQualifierTuple("col1", "tab2")),
            (ColumnQualifierTuple("col2", "tab1"), ColumnQualifierTuple("col2", "tab2")),
        ],
        dialect="bigquery",
        test_sqlparse=False,
    )