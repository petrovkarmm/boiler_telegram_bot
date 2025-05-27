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
