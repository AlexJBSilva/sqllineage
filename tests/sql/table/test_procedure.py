from ...helpers import assert_table_lineage_equal


def test_procedure_with_select():
    sql = """CREATE PROCEDURE proc1()
BEGIN
SELECT col1 FROM tab1;
END"""
    assert_table_lineage_equal(
        sql, {"tab1"}, {"proc1"}, dialect="bigquery", test_sqlparse=False
    )


def test_procedure_with_insert():
    sql = """CREATE PROCEDURE proc1()
BEGIN
INSERT INTO tab1 (col1) VALUES (1);
END"""
    assert_table_lineage_equal(
        sql, None, {"proc1", "tab1"}, dialect="bigquery", test_sqlparse=False
    )


def test_procedure_with_select_and_insert():
    sql = """CREATE PROCEDURE proc1()
BEGIN
INSERT INTO tab2 (col1)
SELECT col1 FROM tab1;
END"""
    assert_table_lineage_equal(
        sql, {"tab1"}, {"proc1", "tab2"}, dialect="bigquery", test_sqlparse=False
    )
