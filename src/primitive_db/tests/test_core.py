from primitive_db.core import insert_row


def test_insert_id():
    data = insert_row({"users": ["ID:int", "age:int"]}, [], "users", {"age": "25"})
    row = data[0]
    assert row["ID"] == 1 and row["age"] == 25
