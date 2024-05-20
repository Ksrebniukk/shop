from settings.message import MESSAGES
from settings import config, order_calculator
from handlers.handler import Handler


class HandlerAllText(Handler):

    def __init__(self, bot):
        super().__init__(bot)
        self.step = 0

    def pressed_btn_category(self, message):
        self.bot.send_message(message.chat.id, "Оберіть жанр книги",
                              reply_markup=self.keybords.remove_menu())
        self.bot.send_message(message.chat.id, "Зробіть свій вибір",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_info(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.info_menu())

    def pressed_btn_settings(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.settings_menu())

    def pressed_btn_back(self, message):
        self.bot.send_message(message.chat.id, "Ви повернулись назад",
                              reply_markup=self.keybords.start_menu())

    def pressed_btn_product(self, message, product):
        self.bot.send_message(message.chat.id, 'Категорія ' +
                              config.KEYBOARD[product],
                              reply_markup=self.keybords.set_select_category(
                                  config.CATEGORY[product]))

    def pressed_btn_order(self, message):
        self.step = 0
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])

        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        self.bot.send_message(message.chat.id,MESSAGES['order_number'].format(
            self.step+1), parse_mode="HTML")
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].
                              format(self.BD.select_single_product_name(
                                  product_id),
                                     self.BD.select_single_product_author(
                                         product_id),
                                     self.BD.select_single_product_price(
                                         product_id),
                                     self.BD.select_order_quantity(
                                         product_id)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.orders_menu(
                                  self.step, quantity))

    def pressed_btn_up(self, message):
        count = self.BD.select_all_product_id()
        quantity_order = self.BD.select_order_quantity(count[self.step])
        quantity_product = self.BD.select_single_product_quantity(
            count[self.step])
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            self.BD.update_order_value(count[self.step],
                                       'quantity', quantity_order)
            self.BD.update_product_value(count[self.step],
                                         'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_douwn(self, message):
        count = self.BD.select_all_product_id()
        quantity_order = self.BD.select_order_quantity(count[self.step])
        quantity_product = self.BD.select_single_product_quantity(
            count[self.step])
        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            self.BD.update_order_value(count[self.step],
                                       'quantity', quantity_order)
            self.BD.update_product_value(count[self.step],
                                         'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_x(self, message):
        count = self.BD.select_all_product_id()

        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(count[self.step])
            quantity_product = self.BD.select_single_product_quantity(
                count[self.step])
            quantity_product += quantity_order
            self.BD.delete_order(count[self.step])
            self.BD.update_product_value(count[self.step],
                                         'quantity', quantity_product)
            self.step -= 1

        count = self.BD.select_all_product_id()
        if count.__len__() > 0:

            quantity_order = self.BD.select_order_quantity(count[self.step])
            self.send_message_order(count[self.step], quantity_order, message)

        else:
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.category_menu())

    def pressed_btn_back_step(self, message):
        if self.step > 0:
            self.step -= 1
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])

        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_next_step(self, message):
        if self.step < self.BD.count_rows_order() - 1:
            self.step += 1
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])

        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_apllay(self, message):
        self.bot.send_message(message.chat.id, config.KEYBOARD['DATA'])

        total_cost = order_calculator.get_total_coas(self.BD)
        total_quantity = order_calculator.get_total_quantity(self.BD)
        order_data = {
            'total_cost': total_cost,
            'total_quantity': total_quantity
        }

        self.BD.save_order_data(order_data)

        self.bot.send_message(message.chat.id, config.KEYBOARD['THANKS'])

    def handle(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['ORDER']:
                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode="HTML",
                                          reply_markup=self.keybords.
                                          category_menu())

            if message.text == config.KEYBOARD['CLASIC_LITERATURE']:
                self.pressed_btn_product(message, 'CLASIC_LITERATURE')

            if message.text == config.KEYBOARD['FICTION']:
                self.pressed_btn_product(message, 'FICTION')

            if message.text == config.KEYBOARD['FANTASY']:
                self.pressed_btn_product(message, 'FANTASY')

            if message.text == config.KEYBOARD['ROMANTIC_PROSE']:
                self.pressed_btn_product(message, 'ROMANTIC_PROSE')

            if message.text == config.KEYBOARD['Thriller']:
                self.pressed_btn_product(message, 'Thriller')

            if message.text == config.KEYBOARD['Mystery']:
                self.pressed_btn_product(message, 'Mystery')

            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            if message.text == config.KEYBOARD['DOUWN']:
                self.pressed_btn_douwn(message)

            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)

            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)

            if message.text == config.KEYBOARD['APPLAY']:
                self.pressed_btn_apllay(message)
            else:
                self.bot.send_message(message.chat.id, message.text)