import telebot
from telebot import types

bot = telebot.TeleBot('7645291466:AAHFAUYG0qEdMi5Q6VX-Bnpd-6KhnEiUij8')

# URLs and Resources
website_url = 'https://duikt.edu.ua/'
conact_email = 'elkafarnayousef@gmail.com'


# Handlers 
@bot.message_handler(commands=['start', 'welcome'])
def welcome(message):
    """Welcome message for new users."""
    first_name = message.from_user.first_name
    bot.send_message(
        message.chat.id,
        f"Welcome, {first_name}. Im here to help you! "
        f"You can get more help by checking out our links below :"
    )

    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('/help - to check our bot commands ', '/info - about our service and contact')
    keyboard.row('/catalog - check our products')
    bot.send_message(chat_id, "Choose an option below:", reply_markup=keyboard)

products = {
    1: {'name': 'Product 1', 'description': 'Description for product 1', 'price': 100},
    2: {'name': 'Product 2', 'description': 'Description for product 2', 'price': 200},
}

@bot.message_handler(commands=['catalog'])
def catalog(message):
    """Show the catalog of products."""
    for product_id, product in products.items():
        keyboard = types.InlineKeyboardMarkup()
        order_button = types.InlineKeyboardButton(
            text="Order Now", callback_data=f"order_{product_id}"
        )
        keyboard.add(order_button)
        bot.send_message(
            message.chat.id,
            f"**{product['name']}**\n{product['description']}\nPrice: ${product['price']}",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
@bot.callback_query_handler(func=lambda call: call.data.startswith('order_'))
def order_product(call):
    """Handle ordering a product."""
    product_id = int(call.data.split('_')[1])
    product = products.get(product_id)
    if product:
        bot.send_message(
            call.message.chat.id,
            f"Thank you for ordering {product['name']}! Our team will contact you shortly."
        )
        # Notify admin about the order
        admin_id = 713850421
        bot.send_message(
            admin_id,
            f"New order:\nProduct: {product['name']}\nUser: {call.message.chat.username or call.message.chat.id}"
        )
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    """Show admin commands."""
    if message.chat.id != 713850421:
        bot.send_message(message.chat.id, "You are not authorized to use admin commands.")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('/add_item', '/delete_item', '/list_orders')
    bot.send_message(message.chat.id, "Admin commands:", reply_markup=keyboard)

@bot.message_handler(commands=['add_item'])
def add_item(message):
    """Admin adds a new item."""
    # Implement the logic for adding a new product (e.g., ask for details step-by-step)
    pass

@bot.message_handler(commands=['delete_item'])
def delete_item(message):
    """Admin deletes an item."""
    # Implement the logic for deleting a product
    pass

@bot.message_handler(commands=['list_orders'])
def list_orders(message):
    """Admin views all orders."""
    # Implement logic to show the list of orders
    pass
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    """Show admin commands."""
    if message.chat.id != 713850421:
        bot.send_message(message.chat.id, "You are not authorized to use admin commands.")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('/add_item', '/delete_item', '/list_orders')
    bot.send_message(message.chat.id, "Admin commands:", reply_markup=keyboard)

@bot.message_handler(commands=['add_item'])
def add_item(message):
    """Admin adds a new item."""
    # Implement the logic for adding a new product (e.g., ask for details step-by-step)
    pass

@bot.message_handler(commands=['delete_item'])
def delete_item(message):
    """Admin deletes an item."""
    # Implement the logic for deleting a product
    pass

@bot.message_handler(commands=['list_orders'])
def list_orders(message):
    """Admin views all orders."""
    # Implement logic to show the list of orders
    pass

@bot.message_handler(commands=['feedback'])
def feedback(message):
    """Handle user feedback."""
    bot.send_message(
        message.chat.id,
        "Please share your feedback with us. We appreciate your time!"
    )
    bot.register_next_step_handler(message, save_feedback)

def save_feedback(message):
    # Save the feedback and respond to the user
    feedback = message.text
    bot.send_message(message.chat.id, "Thank you for your feedback!")
    admin_id = 713850421
    bot.send_message(admin_id, f"New feedback from {message.chat.username or message.chat.id}:\n{feedback}")

# block of code :  function about catalog command that shows a list of products and their description 
# block of code : make the user able to order products in chat you can make it inline buttons with successfull order
# block of code : create a /order command that sends the admin an information about the order and the user which he used.
# block of code : make a func for admins to check by user id using /admin command adming can do add new products in the catalog by using /add_item /delete_item /list_order
# Block of code : create a func that answer to the user if he asks which products are available and how to order 
# block of code : • Додати Reply Keyboard для команд /start, /catalog, /info, щоб
# користувачі могли взаємодіяти з ботом за допомогою кнопок.
# Інлайн-кнопки мають бути використані для перегляду деталей товару та підтвердження замовлень.
# block of code : make a /feedback that can add a feed back and thank them privatly for ordering if they have ordered and rating about the bot 
# • Валідувати введені дані (наприклад, ціни товарів під час додавання товару адміністратором).
# • Реалізувати базову перевірку на коректність введених команд і даних від користувачів.
# • Створення рахунку для користувача.• Обробка доставки (за необхідністю)• Обробка попереднього замовлення• Підтвердження / відміна оплати.
# im using DigitalOcean i want to download my project to the server and get the access by SSH than i have python usage 
# installing the viruatl env and the requirement libraries in the server
# installing the code on server copy the files uploading the bot on the server setting auto uploading or auto running the bot 
bot.polling(non_stop=True)