"""add_trigger_to_trigger_time

Revision ID: 3f18e5fecca6
Revises: 2577b8c3fcf5
Create Date: 2023-09-01 13:10:24.604420

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3f18e5fecca6'
down_revision: Union[str, None] = '2577b8c3fcf5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создастся функция, которая будет вызываться перед каждой операцией вставки данных
    # в таблицу "value". Если значение value больше 9, она выполнит вставку текущего
    # времени в таблицу "trigger_time".
    op.execute("""
        CREATE OR REPLACE FUNCTION trigger_insert_value_greater_than_9()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.value > 9 THEN
                INSERT INTO trigger_time (time) VALUES (NOW());
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Создается триггер, который срабатывает перед вставкой данных
    # в таблицу value. Триггер вызывает функцию trigger_insert_value_greater_than_9()
    # перед каждой операцией вставки данных.
    op.execute("""
        CREATE TRIGGER insert_value_greater_than_9_trigger
        BEFORE INSERT ON value
        FOR EACH ROW
        EXECUTE FUNCTION trigger_insert_value_greater_than_9();
    """)


def downgrade():
    op.execute("DROP TRIGGER insert_value_greater_than_9_trigger ON value;")
    op.execute("DROP FUNCTION trigger_insert_value_greater_than_9();")
