import matplotlib.pyplot as plt
from src.getraenkeabrechnung.backend.main import (
    _get_sql,
    _get_list_from_sql,
    get_gesamtbetrag
)

class Piechart:
    def __init__(self, name):
        plt.figure(num=name)

        self.users = _get_list_from_sql(_get_sql("SELECT UserName FROM user"))
        self.drinks = _get_list_from_sql(_get_sql("SELECT DrinkName FROM drinks"))
        self.ges = round(_get_sql(
            "SELECT sum(Price) FROM entry AS e, drinks AS d WHERE e.DrinkID = d.DrinkID;"
        )[0][0], 2)

        self.filters = ["Drink", "User"]

        print(f"{self.users = }, \n{self.drinks = }, \n{self.ges = }, \n{self.filters = }\n")

        self.a_users = _get_sql("SELECT COUNT(*) FROM user")[0][0]
        self.rows = 2
        self.columns = 1
        if self.a_users % self.rows == 0:
            self.columns = int(self.a_users / self.rows)
        else:
            self.columns = self.a_users

    def command_for_user(self, user):
        return f"""
        SELECT  
            DrinkName,    
            count(DrinkName) AS Anzahl,
            sum(Price) AS Gesamtpreis
        FROM
            entry AS e, 
            user AS u, 
            drinks AS d
        WHERE 
            e.UserID = u.UserID AND
            e.DrinkID = d.DrinkID AND
            UserName = '{user}'
        GROUP BY DrinkName
        ORDER BY Gesamtpreis DESC
        ;
        """

    def command_with_filters(self, filters):
        return f"""
        SELECT  
            {filters}Name,
            count({filters}Name) AS Anzahl,
            sum(Price) AS Gesamtpreis
        FROM
            entry AS e, 
            user AS u, 
            drinks AS d
        WHERE 
            e.UserID = u.UserID AND
            e.DrinkID = d.DrinkID
        GROUP BY {filters}Name
        ORDER BY Gesamtpreis DESC
        ;
        """

    def create_pie_plot(self):
        self.create_plot_filters()
        self.create_plot_user(len(self.filters))

    def create_plot_whole(self, offset, a_plots = None, dif = None):
        if (dif and a_plots) is None:
            for i, filteri in enumerate(self.filters):
                df = _get_sql(self.command_with_filters(filteri))
                items = _get_list_from_sql(df)
                prices = _get_list_from_sql(df, 1)
    
                labels = [f"{items[i]} ({round(prices[i], 2)} €)" for i in range(len(prices))]
                print(f"{filteri}: {labels}")
    
                plt.subplot(
                    self.rows + int(len(self.filters) / self.columns), 
                    self.columns, 
                    i + offset + 1
                )
                plt.pie(x=prices, labels=labels)
                plt.title(f"{filteri}s ({self.ges} €)")
        else:
            df = _get_sql(self.command_with_filters(dif))
            items = _get_list_from_sql(df)
            prices = _get_list_from_sql(df, 1)

            labels = [f"{items[i]} ({round(prices[i], 2)} €)" for i in range(len(prices))]
            print(f"{dif}: {labels}")

            plt.subplot(
                self.rows + int(len(self.filters) / self.columns), 
                self.columns, 
                i + offset + 1
            )
            plt.pie(x=prices, labels=labels)
            plt.title(f"{filteri}s ({self.ges} €)")
        return dif

    def create_plot_filters(self, offset = 0):
        for i, filteri in enumerate(self.filters):
            df = _get_sql(self.command_with_filters(filteri))
            items = _get_list_from_sql(df)
            amount = _get_list_from_sql(df, 1)
            prices = _get_list_from_sql(df, 2)

            labels = [f"{items[i]} ({amount[i]}, {round(prices[i], 2)} €)" for i in range(len(prices))]
            print(f"{filteri}: {labels}")

            plt.subplot(
                self.rows + int(len(self.filters) / self.columns), 
                self.columns, 
                i + offset + 1
            )
            plt.pie(x=prices, labels=labels)
            plt.title(f"{filteri}s ({self.ges} €)")

        print()

    def create_plot_user(self, offset = 0):
        for i, user in enumerate(self.users):
            df = _get_sql(self.command_for_user(user))
            items = _get_list_from_sql(df)
            amount = _get_list_from_sql(df, 1)
            prices = _get_list_from_sql(df, 2)
            user_ges = get_gesamtbetrag(user)

            labels = [f"{items[i]} ({amount[i]}, {round(prices[i], 2)} €)" for i in range(len(prices))]
            print(f"{user}: {labels}")

            plt.subplot(
                self.rows + int(len(self.filters) / self.columns), 
                self.columns, 
                i + offset + 1
            )
            plt.pie(x=prices, labels=labels)
            plt.title(f"{user} ({user_ges} €)")

        print()

pie = Piechart("Ausgaben nach verschiedenen Filtern")
pie.create_pie_plot()
plt.show()