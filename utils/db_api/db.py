import sqlite3

from utils.misc.logging import logger


class Base():

    def con(self, name):
        con = sqlite3.connect(f'{name}.db')
        return con

    def create_table_tasks(self, name):
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS `main` (chat_id INTEGER, photo TEXT, cheker BOOLEAN)")
            con.commit()
            cur.close()

    def add_task(self, name, chat_id, photo, cheker):
        self.create_table_tasks(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.executemany(f"INSERT INTO `main` VALUES (?,?,?)", [(chat_id, photo, cheker)])
            con.commit()
            cur.close()
            logger.info(f'[--] {chat_id} || ADD TASK')

    def read_tasks(self, name):
        self.create_table_tasks(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM `main`")
            data = cur.fetchone()
        return data

    def read_tasks_id(self, name, chat_id):
        self.create_table_tasks(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM `main` WHERE chat_id=?", [(chat_id)])
            data = cur.fetchall()
            logger.info('[--] READ TASKS')
        return data

    def update_task_id(self, name, cheker, chat_id):
        self.create_table_tasks(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute(f"UPDATE `main` SET cheker=? WHERE chat_id=?", [(cheker), (chat_id)])
            con.commit()
            cur.close()


    def delete_task(self, name, chat_id):
        self.create_table_tasks(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM `main` WHERE chat_id=?", [(chat_id)])
            logger.debug(f'DELETE TASK {chat_id}')
            con.commit()
            cur.close()
            logger.info(f'[--] {chat_id} || DELETE TASK')



    def create_table_user_pay(self, name):
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS `main` (chat_id INTEGER, count INTEGER)")
            con.commit()

    def add_user_pay(self, name, chat_id, count):
        self.create_table_user_pay(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO `main` VALUES (?,?)", [(chat_id), (count)])
            con.commit()
            cur.close()
            logger.info(f'[--] {chat_id} || ADD USER PAY')

    def read_user_pay_id(self, name, chat_id):
        self.create_table_user_pay(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM `main` WHERE chat_id=?", [(chat_id)])
            data = cur.fetchall()
            logger.info('[--] READ USER PAY')
        return data[0]

    def read_user_pay(self, name):
        self.create_table_user_pay(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM `main`")
            data = cur.fetchall()
            logger.info('[--] READ USER PAY')
        return data


    def update_user_pay(self, name, chat_id, count):
        self.create_table_user_pay(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute(f"UPDATE `main` SET count=? WHERE chat_id=?", [(count),(chat_id)])
            con.commit()
            cur.close()






    def create_admins(self, name):
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS `main` (chat_id INTEGER, cheker BOOLEAN, name TEXT)")
            con.commit()


    def add_admin(self, name, chat_id, cheker, name_admin):
        self.create_admins(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO `main` VALUES (?,?,?)", [(chat_id),(cheker),(name_admin)])
            con.commit()
            cur.close()


    def update_admin(self, name, cheker, name_admin):
        self.create_admins(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute(f"UPDATE `main` SET cheker=? WHERE name=?", [(cheker),(name_admin)])
            con.commit()
            cur.close()

    # проверяется статус админа (активный, не активный)
    def read_admin(self, name, chat_id):
        self.create_admins(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM `main` WHERE chat_id=?", [(chat_id)])
            data = cur.fetchall()
            return data[0]

    #  выгружается база админов всех
    def read_admin_p2p(self, name):
        self.create_admins(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM `main`")
            data = cur.fetchall()
            return data

    # выгрузка имен админов для кнопок
    def read_admin_name(self, name, admin_name):
        self.create_admins(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM `main` WHERE name=?",[(admin_name)])
            data = cur.fetchone()
            return data[0]



    def create_table_promo(self, name):
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS `main` (chat_id INTEGER, promo INTEGER)")
            con.commit()

    def add_promocod(self, name, chat_id, code):
        self.create_table_promo(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO `main` VALUES (?,?)", [(chat_id), (code)])
            con.commit()
            cur.close()

    def read_promocod(self, name, chat_id):
        self.create_table_promo(name)
        con = self.con(name)
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM `main` WHERE chat_id=?", [(chat_id)])
            data = cur.fetchall()
            code = []
            for dt in data:
                code.append(dt[1])
            return code
