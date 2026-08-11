import threading
import queue
import time

# मैसेज को आपस में भेजने के लिए एक क्यू (Queue) बनाएंगे
message_queue = queue.Queue()

# चैट सर्वर / लॉजिक सिमुलेशन
def chat_simulation(user_name):
    print(f"✅ {user_name} चैट से जुड़ गया है!")
    time.sleep(0.5)
    
    while True:
        try:
            # अगर कोई मैसेज आया है और वह दूसरे यूजर का है, तो दिखाओ
            if not message_queue.empty():
                sender, msg = message_queue.get()
                if sender != user_name:
                    print(f"\n[{sender} का संदेश]: {msg}")
                    print(f"{user_name} (टाइप करें): ", end="", flush=True)
            time.sleep(0.1)
        except:
            break

# यूजर इनपुट और भेजने का काम
def send_loop(user_name):
    while True:
        msg = input(f"{user_name} (टाइप करें): ")
        if msg.lower() == 'exit':
            break
        # मैसेज को क्यू में डाल देंगे ताकि दूसरे यूजर को मिल सके
        message_queue.put((user_name, msg))

# मुख्य प्रोग्राम
if __name__ == "__main__":
    print("--- 💬 मोबाइल चैट टेस्ट मोड (बिना एरर के) ---")
    print("नोट: आप बारी-बारी से User_1 और User_2 की तरह मैसेज भेज सकते हैं।\n")
    
    # दोनों यूजर्स के लिए थ्रेड शुरू कर रहे हैं
    t1 = threading.Thread(target=chat_simulation, args=("User_1",))
    t2 = threading.Thread(target=chat_simulation, args=("User_2",))
    
    t1.daemon = True
    t2.daemon = True
    
    t1.start()
    t2.start()
    
    # मुख्य स्क्रीन पर यूजर_1 से शुरुआत करते हैं
    try:
        send_loop("User_1")
    except KeyboardInterrupt:
        print("\nचैट बंद कर दी गई है।")
import threading
import queue
import time

# डेटा शेयर करने के लिए क्यू और स्टोरेज
message_queue = queue.Queue()
status_storage = {}  # यहाँ यूजर्स के स्टेटस सेव होंगे

def chat_simulation(user_name):
    while True:
        try:
            if not message_queue.empty():
                sender, msg = message_queue.get()
                if sender != user_name:
                    print(f"\n[🔔 नया संदेश - {sender} से]: {msg}")
            time.sleep(0.1)
        except:
            break

def main_app():
    print("--- 📱 आपके अपने चैट ऐप (MVP) में स्वागत है ---")
    user_name = input("अपना नाम दर्ज करें (जैसे User_1 या User_2): ").strip()
    if not user_name:
        user_name = "User_1"

    print(f"\n✅ स्वागत है {user_name}! आप ऐप से जुड़ चुके हैं।")

    # बैकएंड लिसनर थ्रेड शुरू करें
    t = threading.Thread(target=chat_simulation, args=(user_name,))
    t.daemon = True
    t.start()

    while True:
        print("\n--- 📌 मुख्य मेनू ---")
        print("1. चैट भेजें (Send Message)")
        print("2. स्टेटस लगाएं (Upload Status)")
        print("3. स्टेटस देखें (View Status)")
        print("4. कॉल करें (Make a Call)")
        print("5. बाहर निकलें (Exit)")
        
        choice = input("विकल्प चुनें (1-5): ").strip()

        if choice == '1':
            msg = input(f"{user_name} (संदेश लिखें): ")
            message_queue.put((user_name, msg))
            print("📤 संदेश भेज दिया गया!")

        elif choice == '2':
            status_text = input("अपना नया स्टेटस टाइप करें: ")
            status_storage[user_name] = status_text
            print("✨ स्टेटस सफलतापूर्वक अपडेट हो गया!")

        elif choice == '3':
            print("\n--- 👀 सभी यूजर्स के स्टेटस ---")
            if not status_storage:
                print("कोई स्टेटस उपलब्ध नहीं है।")
            else:
                for usr, st in status_storage.items():
                    print(f"• {usr}: \"{st}\"")

        elif choice == '4':
            target = input("आप किसे कॉल करना चाहते हैं (नाम लिखें): ")
            print(f"📞 {target} को ऑडियो कॉल मिलाई जा रही है... (रिंग जा रही है 🎶)")
            time.sleep(2)
            print(f"🔴 {target} ने कॉल नहीं उठाई या कॉल समाप्त हुई।")

        elif choice == '5':
            print("👋 ऐप बंद हो रहा है। अलविदा!")
            break
        else:
            print("⚠️ अमान्य विकल्प, कृपया सही नंबर चुनें।")

if __name__ == "__main__":
    main_app()
import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n[📩 नया संदेश]: {message}")
            print("आप: ", end="", flush=True)
        except:
            break

def start_chat():
    print("--- 🌐 नेटवर्क चैट मोड ---")
    mode = input("क्या आप सर्वर बनना चाहते हैं या क्लाइंट? (server/client): ").strip().lower()

    if mode == 'server':
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 9999))
        server.listen(1)
        print("🚀 सर्वर शुरू हो गया है... दूसरे यूजर के जुड़ने का इंतज़ार है...")
        
        client_sock, address = server.accept()
        print(f"✅ कनेक्शन जुड़ गया है! (IP: {address})")
        
        threading.Thread(target=receive_messages, args=(client_sock,), daemon=True).start()
        
        while True:
            msg = input("आप: ")
            client_sock.send(msg.encode('utf-8'))

    elif mode == 'client':
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = input("सर्वर का IP एड्रेस दर्ज करें (जैसे 127.0.0.1): ").strip()
        
        try:
            client.connect((host_ip, 9999))
            print("✅ सर्वर से सफलतापूर्वक जुड़ गए हैं!")
            
            threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
            
            while True:
                msg = input("आप: ")
                client.send(msg.encode('utf-8'))
        except:
            print("❌ कनेक्शन विफल हो गया। IP एड्रेस चेक करें।")

if __name__ == "__main__":
    start_chat()
import socket
import threading
import sqlite3
from datetime import datetime

# 1. डेटाबेस सेटअप (चैट सेव करने के लिए)
def init_db():
    conn = sqlite3.connect('chat_history.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

conn, cursor = init_db()

# मैसेज डेटाबेस में सेव करने का फंक्शन
def save_message(sender, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO messages (sender, message, timestamp) VALUES (?, ?, ?)", (sender, message, timestamp))
    conn.commit()

# पुराने मैसेज देखने का फंक्शन
def show_chat_history():
    print("\n--- 📜 पुरानी चैट हिस्ट्री (Database History) ---")
    cursor.execute("SELECT sender, message, timestamp FROM messages")
    rows = cursor.fetchall()
    if not rows:
        print("कोई पुराना मैसेज नहीं है।")
    else:
        for row in rows:
            print(f"[{row[2]}] {row[0]}: {row[1]}")
    print("---------------------------------------------")

def receive_messages(sock, user_name):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n[📩 नया संदेश]: {message}")
            # मिले हुए मैसेज को डेटाबेस में सेव करें
            save_message("दूसरा यूजर", message)
            print(f"{user_name}: ", end="", flush=True)
        except:
            break

def start_chat():
    print("--- 📱 प्रोफेशनल डेटाबेस चैट ऐप ---")
    user_name = input("अपना नाम दर्ज करें: ").strip()
    
    # ऐप शुरू होते ही पुरानी चैट दिखाएं
    show_chat_history()

    mode = input("\nक्या आप सर्वर बनना चाहते हैं या क्लाइंट? (server/client): ").strip().lower()

    if mode == 'server':
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 9999))
        server.listen(1)
        print("🚀 सर्वर शुरू हो गया है... दूसरे यूजर के जुड़ने का इंतज़ार है...")
        
        client_sock, address = server.accept()
        print(f"✅ कनेक्शन जुड़ गया है! (IP: {address})")
        
        threading.Thread(target=receive_messages, args=(client_sock, user_name), daemon=True).start()
        
        while True:
            msg = input(f"{user_name}: ")
            if msg.lower() == 'exit':
                break
            client_sock.send(msg.encode('utf-8'))
            save_message(user_name, msg)

    elif mode == 'client':
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = input("सर्वर का IP एड्रेस दर्ज करें (जैसे 127.0.0.1): ").strip()
        
        try:
            client.connect((host_ip, 9999))
            print("✅ सर्वर से सफलतापूर्वक जुड़ गए हैं!")
            
            threading.Thread(target=receive_messages, args=(client, user_name), daemon=True).start()
            
            while True:
                msg = input(f"{user_name}: ")
                if msg.lower() == 'exit':
                    break
                client.send(msg.encode('utf-8'))
                save_message(user_name, msg)
        except:
            print("❌ कनेक्शन विफल हो गया। IP एड्रेस चेक करें।")

if __name__ == "__main__":
    start_chat()
import socket
import threading
import sqlite3
from datetime import datetime

# 1. डेटाबेस सेटअप (चैट सेव करने के लिए)
def init_db():
    conn = sqlite3.connect('chat_history.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

conn, cursor = init_db()

# मैसेज डेटाबेस में सेव करने का फंक्शन
def save_message(sender, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO messages (sender, message, timestamp) VALUES (?, ?, ?)", (sender, message, timestamp))
    conn.commit()

# पुराने मैसेज देखने का फंक्शन
def show_chat_history():
    print("\n--- 📜 पुरानी चैट हिस्ट्री (Database History) ---")
    cursor.execute("SELECT sender, message, timestamp FROM messages")
    rows = cursor.fetchall()
    if not rows:
        print("कोई पुराना मैसेज नहीं है।")
    else:
        for row in rows:
            print(f"[{row[2]}] {row[0]}: {row[1]}")
    print("---------------------------------------------")

def receive_messages(sock, user_name):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n[📩 नया संदेश]: {message}")
            # मिले हुए मैसेज को डेटाबेस में सेव करें
            save_message("दूसरा यूजर", message)
            print(f"{user_name}: ", end="", flush=True)
        except:
            break

def start_chat():
    print("--- 📱 प्रोफेशनल डेटाबेस चैट ऐप ---")
    user_name = input("अपना नाम दर्ज करें: ").strip()
    
    # ऐप शुरू होते ही पुरानी चैट दिखाएं
    show_chat_history()

    mode = input("\nक्या आप सर्वर बनना चाहते हैं या क्लाइंट? (server/client): ").strip().lower()

    if mode == 'server':
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 9999))
        server.listen(1)
        print("🚀 सर्वर शुरू हो गया है... दूसरे यूजर के जुड़ने का इंतज़ार है...")
        
        client_sock, address = server.accept()
        print(f"✅ कनेक्शन जुड़ गया है! (IP: {address})")
        
        threading.Thread(target=receive_messages, args=(client_sock, user_name), daemon=True).start()
        
        while True:
            msg = input(f"{user_name}: ")
            if msg.lower() == 'exit':
                break
            client_sock.send(msg.encode('utf-8'))
            save_message(user_name, msg)

    elif mode == 'client':
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = input("सर्वर का IP एड्रेस दर्ज करें (जैसे 127.0.0.1): ").strip()
        
        try:
            client.connect((host_ip, 9999))
            print("✅ सर्वर से सफलतापूर्वक जुड़ गए हैं!")
            
            threading.Thread(target=receive_messages, args=(client, user_name), daemon=True).start()
            
            while True:
                msg = input(f"{user_name}: ")
                if msg.lower() == 'exit':
                    break
                client.send(msg.encode('utf-8'))
                save_message(user_name, msg)
        except:
            print("❌ कनेक्शन विफल हो गया। IP एड्रेस चेक करें।")

if __name__ == "__main__":
    start_chat()
import flet as ft

def main(page: ft.Page):
    page.title = "मेरा प्रोफेशनल चैट ऐप"
    page.vertical_alignment = ft.MainAxisAlignment.END
    page.window_width = 400
    page.window_height = 600

    # चैट मैसेज दिखाने के लिए लिस्ट व्यू
    chat_list = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)

    # मैसेज टाइप करने का इनपुट बॉक्स
    user_input = ft.TextField(
        hint_text="संदेश टाइप करें...",
        expand=True,
        border_radius=20,
        filled=True,
    )

    # मैसेज भेजने का फंक्शन
    def send_click(e):
        if user_input.value.strip():
            # यूजर का मैसेज स्क्रीन पर जोड़ें
            chat_list.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(user_input.value, color=ft.colors.WHITE),
                            bgcolor=ft.colors.BLUE_700,
                            padding=10,
                            border_radius=10,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                )
            )
            
            # ऑटोमैटिक रिप्लाई सिमुलेशन (ताकि ऐप जीवित लगे)
            msg_text = user_input.value
            user_input.value = ""
            page.update()

            # थोड़ी देर बाद उत्तर आना
            import time
            time.sleep(0.5)
            chat_list.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(f"मिला: {msg_text}", color=ft.colors.BLACK),
                            bgcolor=ft.colors.GREY_300,
                            padding=10,
                            border_radius=10,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            )
            page.update()

    # भेजने का बटन
    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color=ft.colors.BLUE_700,
        on_click=send_click,
    )

    # नीचे का बार (इनपुट और बटन)
    input_bar = ft.Row([user_input, send_button])

    # पेज पर सब कुछ जोड़ें
    page.add(chat_list, input_bar)

if __name__ == "__main__":
    ft.app(target=main)
Receive occasional product updates and announcements
