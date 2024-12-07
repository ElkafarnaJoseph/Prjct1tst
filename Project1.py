import telebot
from telebot import types

bot = telebot.TeleBot('7645291466:AAHFAUYG0qEdMi5Q6VX-Bnpd-6KhnEiUij8')

# URLs and Resources
website_url = 'https://duikt.edu.ua/'
contact_email = 'elkafarnayousef@gmail.com'
admin_id = 713850421

# Sample Products
products = {
    1: {'name': 'Product 1', 'description': 'Description for Product 1', 'price': 100},
    2: {'name': 'Product 2', 'description': 'Description for Product 2', 'price': 200},
    3: {'name': 'Product 3', 'description': 'Description for Product 3', 'price': 300},
    4: {'name': 'Product 4', 'description': 'Description for Product 4', 'price': 400},
}

# User Carts
user_carts = {}

# Handlers
@bot.message_handler(commands=['start', 'welcome'])
def welcome(message):
    """Welcome message for new users."""
    first_name = message.from_user.first_name
    bot.send_message(
        message.chat.id,
        f"Welcome, {first_name}! I'm here to assist you.\n"
        f"Use the commands below or click the buttons to get started."
    )
    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('/help', '/info', '/catalog')
    keyboard.row('/feedback', '/checkout')
    bot.send_message(chat_id, "Choose an option below:", reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help_command(message):
    """List all commands."""
    bot.send_message(
        message.chat.id,
        "Here are the available commands:\n"
        "/start - Start the bot and view the main menu\n"
        "/catalog - Browse our products\n"
        "/checkout - Review your cart and proceed to payment\n"
        "/feedback - Share your feedback\n"
        "/admin - Admin-specific commands (restricted)\n"
        "/help - Show this help message\n"
        "/info - Learn more about this bot and its services"
    )

@bot.message_handler(commands=['info'])
def info_command(message):
    """Provide information about the bot."""
    bot.send_message(
        message.chat.id,
        f"This bot helps you explore our catalog, place orders, and connect with our team. "
        f"For more details, visit our website: {website_url} or contact us at: {contact_email}"
    )

@bot.message_handler(commands=['catalog'])
def catalog(message):
    """Show the catalog of products."""
    for product_id, product in products.items():
        keyboard = types.InlineKeyboardMarkup()
        add_to_cart_button = types.InlineKeyboardButton(
            text="Add to Cart", callback_data=f"add_{product_id}"
        )
        keyboard.add(add_to_cart_button)
        bot.send_message(
            message.chat.id,
            f"**{product['name']}**\n{product['description']}\nPrice: ${product['price']}",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
def add_to_cart(call):
    """Add a product to the user's cart."""
    product_id = int(call.data.split('_')[1])
    user_id = call.message.chat.id
    product = products.get(product_id)

    if user_id not in user_carts:
        user_carts[user_id] = []

    user_carts[user_id].append(product)
    bot.send_message(
        user_id,
        f"{product['name']} has been added to your cart."
    )
    # Notify the admin
    bot.send_message(
        admin_id,
        f"User {call.message.chat.username or user_id} added {product['name']} to their cart."
    )

@bot.message_handler(commands=['checkout'])
def checkout(message):
    """Review the user's cart and proceed to payment."""
    user_id = message.chat.id
    if user_id not in user_carts or not user_carts[user_id]:
        bot.send_message(user_id, "Your cart is empty. Use /catalog to add products.")
        return

    cart = user_carts[user_id]
    total = sum(item['price'] for item in cart)
    cart_details = "\n".join([f"{item['name']} - ${item['price']}" for item in cart])

    bot.send_message(
        user_id,
        f"Here are the items in your cart:\n{cart_details}\n\nTotal: ${total}"
    )

    keyboard = types.InlineKeyboardMarkup()
    confirm_button = types.InlineKeyboardButton("Confirm Order", callback_data="confirm_order")
    cancel_button = types.InlineKeyboardButton("Cancel Order", callback_data="cancel_order")
    keyboard.add(confirm_button, cancel_button)

    bot.send_message(user_id, "Do you want to proceed with the order?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_order')
def confirm_order(call):
    """Handle order confirmation."""
    user_id = call.message.chat.id
    cart = user_carts.pop(user_id, [])
    total = sum(item['price'] for item in cart)
    bot.send_message(
        user_id,
        f"Thank you for your order! Your total is ${total}. Our team will contact you soon."
    )
    # Notify admin
    bot.send_message(
        admin_id,
        f"New order from {call.message.chat.username or user_id}:\n"
        f"Items:\n" +
        "\n".join([f"{item['name']} - ${item['price']}" for item in cart]) +
        f"\nTotal: ${total}"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'cancel_order')
def cancel_order(call):
    """Handle order cancellation."""
    user_id = call.message.chat.id
    user_carts.pop(user_id, None)
    bot.send_message(user_id, "Your order has been cancelled.")

@bot.message_handler(commands=['feedback'])
def feedback(message):
    """Handle user feedback."""
    bot.send_message(
        message.chat.id,
        "Please share your feedback with us. We appreciate your input!"
    )
    bot.register_next_step_handler(message, save_feedback)

def save_feedback(message):
    feedback_text = message.text
    bot.send_message(message.chat.id, "Thank you for your feedback!")
    bot.send_message(
        admin_id,
        f"New feedback from {message.chat.username or message.chat.id}:\n{feedback_text}"
    )

bot.polling(non_stop=True)
