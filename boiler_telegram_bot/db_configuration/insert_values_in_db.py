from db_configuration.crud import TechnicalProblem, Feedback

if __name__ == '__main__':
    problems = [
        'Не работает кофемашина',
        'Не работает кофемолка',
        'Сбились настройки'
    ]

    feedbacks = [
        {
            'tg_user_id': 123456,
            'user_firstname': 'Иван',
            'user_lastname': 'Иванов',
            'user_username': 'ivivanov',
            'feedback_text': 'Отличный сервис, спасибо!'
        },
        {
            'tg_user_id': 789012,
            'user_firstname': 'Ольга',
            'user_lastname': 'Петрова',
            'user_username': 'olgapet',
            'feedback_text': 'Очень долго ждали мастера.'
        }
    ]

    for problem in problems:
        TechnicalProblem.add_technical_problem(problem)

    for fb in feedbacks:
        Feedback.add_feedback(**fb)
