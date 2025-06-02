from db_configuration.db_connection import get_connection


class FirmInfoIndividual:
    @staticmethod
    def add_info(firm_id: int, name: str, phone: str):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO firm_info_individual (
                    firm_id, name, phone
                ) VALUES (?, ?, ?)
            """, (firm_id, name, phone))
            conn.commit()

    @staticmethod
    def update_field(firm_id: int, field: str, new_value: str):
        allowed_fields = {
            "name",
            "phone",
        }

        if field not in allowed_fields:
            raise ValueError(f"Field '{field}' is not allowed for update.")

        with get_connection() as conn:
            cursor = conn.cursor()
            query = f"""
                UPDATE firm_info_individual
                SET {field} = ?
                WHERE firm_id = ?
            """
            cursor.execute(query, (new_value, firm_id))
            conn.commit()
