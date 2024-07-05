msg_user_exist = "Ты уже в системе, можешь работать"
msg_send_mail = "Отправь свою почту"


def msg_err_send_mail(error):
    return "Ошибка: " + error + "\n" + msg_send_mail
