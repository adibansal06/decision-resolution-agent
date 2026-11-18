# Building a Decision-Making Resolution Agent

An AI-powered customer support agent that investigates damaged-item orders and selects an appropriate resolution: exchange or refund. The project uses a ReAct-style tool-calling loop, a Groq-hosted LLM, Python, and SQLite.

## Project overview

When a customer reports that an item arrived damaged, the agent:

1. Looks up the order and retrieves the customer, item, amount, eligibility, and current status.
2. Checks whether the order is eligible for an exchange.
3. If eligible, inspects warehouse inventory.
4. If the item is eligible and stock is available, processes an exchange.
5. If the item is ineligible or stock is unavailable, records a refund against the original payment method.
6. Records a customer notification after a successful resolution.
7. Returns a clear summary of the outcome.

The agent uses model-directed tool calls, while the application controls which functions can actually execute through a whitelist-based dispatcher.

## Technology stack

- **Python** — application and tool implementation
- **Groq API** — LLM inference through an OpenAI-compatible client
- **SQLite** — local persistence for orders, inventory, exchanges, refunds, and notifications
- **Pydantic / JSON-style tool schemas** — structured tool definitions and argument contracts
- **python-dotenv** — environment variable loading

## Architecture

```text
Customer request
      |
      v
   agent.py
      |
      v
Groq LLM (ReAct / tool-calling loop)
      |
      +---- tool call ----+
      |                   |
      v                   v
 tool_schemas.py     dispatcher.py
                          |
                    Whitelist registry
                          |
          +---------------+----------------+
          |               |                |
          v               v                v
     Order tools    Inventory tools   Resolution tools
                                      /             \
                               Refund tools     Exchange tools
          |               |                |
          +---------------+----------------+
                          |
                          v
                    database.py
                      SQLite
                          |
                          v
                Notification tool
                          |
                          v
                  Final response
```

### Main files

| File / folder | Responsibility |
|---|---|
| `agent.py` | Runs the LLM conversation and ReAct tool-calling loop |
| `tool_schemas.py` | Defines the tools and their parameter schemas for the model |
| `dispatcher.py` | Validates tool names and arguments, then invokes whitelisted functions |
| `database.py` | Creates the SQLite tables and inserts sample records |
| `tools/order_tools.py` | Looks up an order |
| `tools/inventory_tools.py` | Checks product stock |
| `tools/refund_tools.py` | Records a refund and updates the order status |
| `tools/exchange_tools.py` | Reserves stock, records an exchange, and updates order status |
| `tools/notification_tools.py` | Records a simulated customer notification |
| `test_*.py` | Tests individual tools and dispatcher behavior |

## Requirements

- Python 3.10 or later
- A Groq API key
- Git (for version control and GitHub publishing)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/decision-resolution-agent.git
cd decision-resolution-agent
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```cmd
venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a file named `.env` in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Do not commit `.env` or share your API key.

### 5. Initialize the database

```bash
python database.py
```

This creates `resolution.db` and initializes the tables and sample data. The database is local to your machine and is intentionally excluded from Git.

### 6. Run the agent

```bash
python agent.py
```

When prompted, enter an order ID, for example:

```text
ORD101
```

The agent will investigate the order and attempt the appropriate resolution.

## Testing

Run the available test scripts from the project root. For example:

```bash
python test_dispatcher.py
python test_order_tool.py
python test_inventory_tool.py
python test_refund_tool.py
python test_exchange_tool.py
python test_notification_tool.py
```

Some tests may change the local database state. The database initializer uses `INSERT OR IGNORE`, so running it again does not reset previously changed order statuses or stock quantities. Use a fresh sample order or recreate the local database if you need a clean test environment.

### Scenarios to demonstrate

| Scenario | Expected decision |
|---|---|
| Valid, eligible order; stock available | Exchange |
| Valid, eligible order; stock unavailable | Refund |
| Valid, ineligible order | Refund |
| Unknown order ID | Explain that the order was not found |
| Already-refunded or exchanged order | Report existing status; do not resolve it again |

Use order IDs that are still in `PLACED` status in your local database when demonstrating successful resolution. Previously processed orders cannot be processed again.

## Safety and reliability measures

- **Whitelisted tools:** the dispatcher only executes registered functions.
- **Argument validation:** missing, malformed, unexpected, or invalid arguments are rejected.
- **Database transactions:** refund and exchange operations use transactions to protect state changes.
- **Duplicate protection:** resolved orders cannot be refunded or exchanged again; notifications are protected against duplicates.
- **Iteration limit:** the agent has a maximum tool-calling loop count to prevent unbounded execution.
- **Graceful errors:** invalid orders and tool failures return controlled messages rather than intentionally crashing the workflow.
- **Secret protection:** the API key is loaded from `.env`, which should remain untracked.

## Current implementation scope and limitations

This is an academic proof-of-concept, not a production payment or email system.

- **Refunds are simulated:** the application records a refund amount and reference/state in SQLite. It does not contact a bank, payment gateway, or payment processor, and no money is transferred.
- **Notifications are simulated:** the application records a notification in SQLite. It does not send an actual email.
- **Inventory and orders are local:** SQLite sample data is used rather than a live order-management or warehouse system.
- **LLM availability:** agent responses depend on access to the configured Groq model and its API limits.

The agent must describe a simulated notification as recorded/simulated, not as an email that was sent.

## Environment and Git hygiene

The repository should include source code, tests, `requirements.txt`, `.gitignore`, and this README. It should **not** include:

- `.env`
- `venv/`
- `resolution.db` or other local database files
- Python cache files such as `__pycache__/` and `*.pyc`

Before publishing, check that `.gitignore` includes at least:

```gitignore
venv/
.env
__pycache__/
*.pyc
*.db
```

Never put API keys, passwords, or other credentials in source code or Git history.

## Future improvements

- Integrate a payment provider's sandbox API for refund workflows.
- Integrate an email service for real customer notifications.
- Add authentication, authorization, audit logs, and stronger operational monitoring.
- Move from local SQLite to a managed relational database for multi-user deployment.
- Add automated tests for transaction rollback, duplicate requests, and concurrent inventory updates.

## Author

**Aditya Bansal**  
Thapar Institute of Engineering & Technology, Patiala

---

*This README describes the current prototype. Update the repository URL, author details, and implementation notes if the project changes.*
