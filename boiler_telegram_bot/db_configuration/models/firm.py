from boiler_telegram_bot.db_configuration.db_connection import get_connection


class Firm:
    @staticmethod
    def add_firm(user_id: int, firm_type: str) -> int:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Добавляем новую фирму
            cursor.execute("""
                INSERT INTO firm (user_id, firm_type)
                VALUES (?, ?)
            """, (user_id, firm_type))

            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def delete_firm(firm_id: int) -> bool | None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            cursor.execute("SELECT user_id FROM firm WHERE id = ?", (firm_id,))
            result = cursor.fetchone()
            if result is None:
                return None  # Фирма не найдена, нельзя удалить

            user_id = result[0]

            cursor.execute("SELECT COUNT(*) FROM firm WHERE user_id = ?", (user_id,))
            firm_count = cursor.fetchone()[0]

            if firm_count <= 1:
                return None  # Нельзя удалить последнюю фирму

            cursor.execute("DELETE FROM firm_info_legal_entity WHERE firm_id = ?", (firm_id,))
            cursor.execute("DELETE FROM firm_info_individual WHERE firm_id = ?", (firm_id,))

            cursor.execute("DELETE FROM firm WHERE id = ?", (firm_id,))

            conn.commit()

            return True

    @staticmethod
    def get_firms_by_telegram_id(telegram_id: str) -> list[dict]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    f.id AS firm_id,
                    f.firm_type,
                    COALESCE(le.organization_name, ind.name) AS name
                FROM firm f
                JOIN user u ON f.user_id = u.id
                LEFT JOIN firm_info_legal_entity le ON le.firm_id = f.id
                LEFT JOIN firm_info_individual ind ON ind.firm_id = f.id
                WHERE u.telegram_id = ?
            """, (telegram_id,))

            rows = cursor.fetchall()

            return [
                {
                    "firm_id": row[0],
                    "firm_type": row[1],
                    "name": row[2]
                }
                for row in rows
            ]

    @staticmethod
    def get_firm_info_by_id(firm_id: int) -> dict | None:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT firm_type FROM firm WHERE id = ?", (firm_id,))
            result = cursor.fetchone()
            if not result:
                return None

            firm_type = result[0]

            if firm_type == 'legal_entity':
                cursor.execute("""
                    SELECT
                        f.id AS firm_id,
                        f.user_id,
                        'legal_entity' AS firm_type,
                        le.organization_name,
                        le.organization_representative_name,
                        le.organization_itn,
                        le.phone
                    FROM firm f
                    JOIN firm_info_legal_entity le ON le.firm_id = f.id
                    WHERE f.id = ?
                """, (firm_id,))
                row = cursor.fetchone()
                if row:
                    return {
                        "firm_id": row[0],
                        "user_id": row[1],
                        "firm_type": row[2],
                        "organization_name": row[3],
                        "representative_name": row[4],
                        "itn": row[5],
                        "phone": row[6],
                    }

            elif firm_type == 'individual':
                cursor.execute("""
                    SELECT
                        f.id AS firm_id,
                        f.user_id,
                        'individual' AS firm_type,
                        ind.name,
                        ind.phone
                    FROM firm f
                    JOIN firm_info_individual ind ON ind.firm_id = f.id
                    WHERE f.id = ?
                """, (firm_id,))
                row = cursor.fetchone()
                if row:
                    return {
                        "firm_id": row[0],
                        "user_id": row[1],
                        "firm_type": row[2],
                        "name": row[3],
                        "phone": row[4],
                    }

            return None
