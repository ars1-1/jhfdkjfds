import flet
from flet import *
from time import *


#chat_msgs = []
online_users = set()\

MAX_MESSAGES_COUNT = 100

def main(page: Page):
    page.title = "Социальная сеть"
    page.add(flet.Text(f"🧊 Добро пожаловать в онлайн чат!"))
    page.vertical_alignment = "center"

    lv = flet.ListView(expand=True, spacing=10)
    
    page.add(lv)

    txt_name = flet.TextField(label="Сообщение")

    def btn_click(e):
        if not txt_name.value:
            txt_name.error_text = "Введите сообщение"
            page.update()
        else:
            name = txt_name.value
#            page.clean()
#            page.add(flet.Text(f"Hello, {name}!"))
            lv.controls.append(flet.Text(txt_name.value))
            page.update()
    print(lv)
    page.add(txt_name, flet.ElevatedButton("Отправить", on_click=btn_click))


flet.app(target=main, view=flet.WEB_BROWSER)








async def main():
    global chat_msgs
    
    put_markdown("## 🧊 Добро пожаловать в онлайн чат!\nИсходный код данного чата укладывается в 100 строк кода!")

    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)

    nickname = await input("Войти в чат", required=True, placeholder="Ваше имя", validate=lambda n: "Такой ник уже используется!" if n in online_users or n == '📢' else None)
    online_users.add(nickname)

    chat_msgs.append(('📢', f'`{nickname}` присоединился к чату!'))
    msg_box.append(put_markdown(f'📢 `{nickname}` присоединился к чату'))

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        data = await input_group("💭 Новое сообщение", [
            input(placeholder="Текст сообщения ...", name="msg"),
            actions(name="cmd", buttons=["Отправить", {'label': "Выйти из чата", 'type': 'cancel'}])
        ], validate = lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)

        if data is None:
            break

        msg_box.append(put_markdown(f"`{nickname}`: {data['msg']}"))
        chat_msgs.append((nickname, data['msg']))

    refresh_task.close()

    online_users.remove(nickname)
    toast("Вы вышли из чата!")
    msg_box.append(put_markdown(f'📢 Пользователь `{nickname}` покинул чат!'))
    chat_msgs.append(('📢', f'Пользователь `{nickname}` покинул чат!'))

    put_buttons(['Перезайти'], onclick=lambda btn:run_js('window.location.reload()'))

async def refresh_msg(nickname, msg_box):
    global chat_msgs
    last_idx = len(chat_msgs)

    while True:
        await asyncio.sleep(1)
        
        for m in chat_msgs[last_idx:]:
            if m[0] != nickname: # if not a message from current user
                msg_box.append(put_markdown(f"`{m[0]}`: {m[1]}"))
        
        # remove expired
        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]
        
        last_idx = len(chat_msgs)
