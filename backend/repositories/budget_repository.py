from db import query


class BudgetRepository:

    # Income
    def create_income(self, user_id, data):
        return query(
            """
            INSERT INTO income_records
            (user_id, source, amount, income_date)
            SELECT user_id, %s, %s, %s
            FROM users WHERE user_id = %s
            RETURNING *
            """,
            (data["source"], data["amount"],
             data["income_date"], user_id)
        )

    def get_incomes(self, user_id):
        return query(
            "SELECT * FROM income_records WHERE user_id = %s",
            (user_id,), True
        )

    def delete_income(self, user_id, income_id):
        return query(
            """
            DELETE FROM income_records
            WHERE user_id = %s AND income_id = %s
            RETURNING income_id
            """,
            (user_id, income_id)
        )

    # Expense categories
    def create_category(self, user_id, data):
        return query(
            """
            INSERT INTO expense_categories
            (user_id, category_name)
            SELECT user_id, %s
            FROM users WHERE user_id = %s
            RETURNING *
            """,
            (data["category_name"], user_id)
        )

    def get_categories(self, user_id):
        return query(
            "SELECT * FROM expense_categories WHERE user_id = %s",
            (user_id,), True
        )

    # Expenses
    def create_expense(self, user_id, data):
        return query(
            """
            INSERT INTO expense_records
            (user_id, category_id, description, amount, expense_date)
            SELECT user_id, category_id, %s, %s, %s
            FROM expense_categories
            WHERE user_id = %s AND category_id = %s
            RETURNING *
            """,
            (data["description"], data["amount"],
             data["expense_date"], user_id, data["category_id"])
        )

    def get_expenses(self, user_id):
        return query(
            """
            SELECT e.*, c.category_name
            FROM expense_records e
            JOIN expense_categories c
                ON e.category_id = c.category_id
            WHERE e.user_id = %s
            """,
            (user_id,), True
        )

    def delete_expense(self, user_id, expense_id):
        return query(
            """
            DELETE FROM expense_records
            WHERE user_id = %s AND expense_id = %s
            RETURNING expense_id
            """,
            (user_id, expense_id)
        )

    # Savings targets
    def create_savings_target(self, user_id, data):
        return query(
            """
            INSERT INTO savings_targets
            (user_id, target_name, target_amount)
            SELECT user_id, %s, %s
            FROM users WHERE user_id = %s
            RETURNING *
            """,
            (data["target_name"], data["target_amount"], user_id)
        )

    def get_savings_targets(self, user_id):
        return query(
            "SELECT * FROM savings_targets WHERE user_id = %s",
            (user_id,), True
        )

    def update_savings_target(self, user_id, target_id, data):
        return query(
            """
            UPDATE savings_targets
            SET target_name = %s, target_amount = %s
            WHERE user_id = %s AND target_id = %s
            RETURNING *
            """,
            (data["target_name"], data["target_amount"],
             user_id, target_id)
        )

    # Savings contributions
    def create_contribution(self, user_id, data):
        return query(
            """
            INSERT INTO savings_contributions
            (target_id, amount, contribution_date)
            SELECT target_id, %s, %s
            FROM savings_targets
            WHERE user_id = %s AND target_id = %s
            RETURNING *
            """,
            (data["amount"], data["contribution_date"],
             user_id, data["target_id"])
        )

    def get_contributions(self, user_id, target_id):
        return query(
            """
            SELECT c.*
            FROM savings_contributions c
            JOIN savings_targets t ON c.target_id = t.target_id
            WHERE t.user_id = %s AND t.target_id = %s
            """,
            (user_id, target_id), True
        )