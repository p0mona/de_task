from src.helpers import DBManager
import os
import pytest


@pytest.fixture()
def mock_db(mocker):
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()

    mock_connection.cursor.return_value = mock_cursor
    mock_connect = mocker.patch(
        "psycopg2.connect",
        return_value=mock_connection)

    db = DBManager()
    db.conn_db()
    yield mock_connect, mock_connection, mock_cursor, db


class TestDBManager:
    def test_conn_db(self, mock_db):
        mock_connect, mock_connection, mock_cursor, db = mock_db

        mock_connect.assert_called_once_with(
            dbname=os.getenv("PGDBNAME"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASS"),
            host=os.getenv("PGHOST"),
            port=os.getenv("PGPORT"),
        )

        assert db.conn == mock_connection
        assert db.cursor == mock_cursor

    @pytest.mark.parametrize(
        "table_name, test_data, expectation",
        [
            (
                "test_tab",
                [(1, "Polina", "Bezukladnova")],
                "INSERT INTO test_tab VALUES (%s, %s, %s);",
            ),
            (
                "test_tab",
                [(2, "Vasya", "Pupkin", "foo")],
                "INSERT INTO test_tab VALUES (%s, %s, %s, %s);",
            ),
            (
                "test_tab",
                [(3, "Michail", "Krug", "boo", 65)],
                "INSERT INTO test_tab VALUES (%s, %s, %s, %s, %s);",
            ),
        ],
    )
    def test_insert_data(self, mock_db, table_name, test_data, expectation):
        *_, mock_cursor, db = mock_db

        db.insert_data(table_name, test_data)
        mock_cursor.executemany.assert_called_once_with(expectation, test_data)

    @pytest.mark.parametrize(
        "path, table_name, json_data, parsed_data",
        [
            (
                "test1.json",
                "test_tab1",
                [{"id": 1, "name": "Qwe"}],
                [(1, "Qwe")]
            ),
            (
                "test2.json",
                "test_tab2",
                [{"age": 34, "name": "Katarzyna", "surname": "Rybarczyk"}],
                [(34, "Katarzyna", "Rybarczyk")],
            ),
        ],
    )
    def test_load_data(
            self,
            mocker,
            mock_db,
            path,
            table_name,
            json_data,
            parsed_data
    ):
        *_, db = mock_db

        mock_open_json = mocker.patch(
            "src.helpers.db_manager.open_json", return_value=json_data
        )
        mock_insert_data = mocker.patch.object(db, "insert_data")

        mock_instance = mocker.Mock()
        mock_instance.parse.return_value = parsed_data
        mock_parser_class = mocker.Mock(return_value=mock_instance)

        db.load_data(path, mock_parser_class, table_name)

        mock_open_json.assert_called_once_with(path)
        mock_parser_class.assert_called_once_with()
        mock_instance.parse.assert_called_once_with(json_data)
        mock_insert_data.assert_called_once_with(table_name, parsed_data)

    @pytest.mark.parametrize(
        "test_query, cols, rows, expectation",
        [
            (
                "SELECT id FROM users",
                [("id",)],
                [(1,), (2,), (3,)],
                [{"id": 1}, {"id": 2}, {"id": 3}],
            ),
            (
                "SELECT COUNT(*) FROM users",
                [("count",)],
                [(3,)],
                [{"count": 3}]
            ),
        ],
    )
    def test_execute_query(self, mock_db, test_query, cols, rows, expectation):
        *_, mock_cursor, db = mock_db

        mock_cursor.description = cols
        mock_cursor.fetchall.return_value = rows

        result = db.execute_query(test_query)
        mock_cursor.execute.assert_called_once_with(test_query)
        assert result == expectation
