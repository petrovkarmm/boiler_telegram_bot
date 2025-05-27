from boiler_telegram_bot.db_configuration.db_connection import get_connection


class FirmInfoLegalEntity:
    @staticmethod
    def add_info(firm_id: int, organization_name: str, representative_name: str,
                 organization_itn: str, phone: str):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO firm_info_legal_entity (
                    firm_id, organization_name, organization_representative_name,
                    organization_itn, phone
                ) VALUES (?, ?, ?, ?, ?)
            """, (firm_id, organization_name, representative_name, organization_itn, phone))
            conn.commit()
