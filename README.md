<p style="text-align: center;">
  <img src="assets/icons/icon.svg" alt="Discord Bot Creator Logo" width="128" height="128">
</p>

<h1 style="text-align: center;">Discord Bot Creator</h1>

<p style="text-align: center;">
  <strong>A powerful, open-source GUI tool to create and manage Discord bots without writing code.</strong>
</p>

<p style="text-align: center;">
  Built with <strong>Python 3.13</strong> and <strong>PySide 6</strong>.
</p>

---

## 📖 About

**Discord Bot Creator** is a desktop application designed to simplify the process of creating Discord bots. It provides
a user-friendly interface to configure commands, automated replies, and moderation actions. Whether you are a beginner
looking to make your first bot or a developer needing a quick GUI solution, this tool utilizes the robust **discord.py**
library and a modern **MVC architecture** to deliver performance and stability.

## ✨ Key Features

* **Interactive Interface:** Clean and responsive GUI built with Qt 6 (PySide 6.10).
* **Logic Builder:** Create complex message triggers using conditions (Equal to, Contains, Starts with, Regex).
* **Automated Responses:** Configure replies, reactions, and delays.
* **Moderation Actions:** Set up auto-kick, auto-ban, pin messages, or delete messages based on triggers.
* **Multi-Language Support:** Fully localized interface (English and Portuguese).
* **Visual Feedback:** Real-time logs and status indicators.

## 🛠️ Tech Stack

This project relies on modern Python libraries to ensure a native and fluid experience:

* **Core:** [Python 3.13+](https://www.python.org/)
* **GUI Framework:** [PySide6](https://pypi.org/project/PySide6/) (
  v6.10.1) & [QtAwesome](https://pypi.org/project/QtAwesome/)
* **Bot Logic:** [discord.py](https://discordpy.readthedocs.io/en/stable/)
* **Widgets:** [QExtraWidgets](https://github.com/gpedrosobernardes/QExtraWidgets)
* **Emojis:** Twemoji API & Emoji Data Python

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.10 or higher installed. This project specifically targets **Python 3.13.3**.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gpedrosobernardes/discord_bot_creator
   cd discord_bot_creator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### ⚠️ Security Note (Windows)

If you are running the compiled version (`.exe`) or launching the script for the first time, Windows SmartScreen may
display a warning: **"Windows protected your PC"**.

This happens because the application is not signed with a paid digital certificate. To run it:

1. Click on **"More info"**.
2. Click on **"Run anyway"**.

## ⚙️ Usage

### 1. Token Setup

Upon launching the application, you will need to provide your Discord Bot Token.

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application and generate a Bot Token.
3. Paste the token into the application's **Token** field.

### 2. Creating Logic

Use the **Editor Window** to define how your bot reacts:

* **Expected Message:** The trigger (e.g., "!hello").
* **Conditions:** Refine the trigger (e.g., *User is not admin* OR *Channel name contains "general"*).
* **Actions:** Define what happens (Reply "Hi there!", React with 😎, etc.).

### 3. Running the Bot

Click the **"Turn on Bot"** button in the interface. You can view real-time logs in the "Logs" window.

Alternatively, you can run the bot process headless (without GUI):

```bash
python bot.py
```

## 📦 Building from Source

To create a standalone executable (`.exe`) for distribution, use the included `setup.py` script which utilizes
`cx_Freeze`.

```bash
python setup.py build
```

The executable will be generated in the `build/` directory, including all necessary assets and translations.

## 💻 For Developers

This project follows a strict **Model-View-Controller (MVC)** architectural pattern to ensure scalability and
maintainability.

### Project Structure

* `source/models`: Data logic, database interactions, and strict typing.
* `source/views`: GUI layouts using Qt Model/View delegates.
* `source/controllers`: Connects models to views and handles business logic.
* `translations/`: Contains `.ts` and compiled `.qm` files for i18n.

### Contributing Translations

To add or update languages, you need **Qt Linguist** tools.

1. **Generate/Update translation files:**

```bash
pyside6-lupdate -extensions py ./source -no-obsolete -ts translations/generated/en_us.ts
```

2. **Edit the `.ts` file** using Qt Linguist.

3. **Compile to `.qm`:**

```bash
pyside6-lrelease translations/generated/en_us.ts -qm translations/build/en_us.qm
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
