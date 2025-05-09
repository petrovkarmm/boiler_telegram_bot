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
            'firstname': 'Иван',
            'lastname': 'Иванов',
            'username': '@ivivanov',
            'text': 'Отличный сервис, спасибо!'
        },
        {
            'tg_user_id': 789012,
            'firstname': 'Ольга',
            'lastname': 'Петрова',
            'username': '@olgapet',
            'text': 'Очень долго ждали мастера.'
        }
    ]

    for problem in problems:
        TechnicalProblem.add_technical_problem(problem)

    for fb in feedbacks:
        Feedback.add_feedback(**fb)
