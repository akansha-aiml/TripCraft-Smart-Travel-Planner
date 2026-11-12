# ✈️ TripCraft — Smart Travel Planner

> Your journey, beautifully planned.

TripCraft is a simple, clean travel planning web app built with **Streamlit** and **SQLite**. It brings everything you need for a trip into one place: your destinations, a day-by-day itinerary, a budget tracker, and a packing checklist.

---

## ✨ Features

| Page | What you can do |
|------|-----------------|
| **Dashboard** | See an overview of your total trips, saved places, combined budget and total expenses |
| **My Trips** | Create trips with a name, destination, dates, estimated budget and number of travelers; view details and delete trips |
| **Destinations** | Save places to visit under a trip, with a category (Sightseeing, Nature, Food, Shopping, Adventure, Accommodation, Other) and notes |
| **Itinerary Planner** | Schedule activities by date and time, with location and notes, sorted chronologically |
| **Budget Planner** | Log expenses by category, track spending against your estimated budget with a progress bar, and get a warning if you go over |
| **Packing Assistant** | Build a per-trip packing checklist, tick items off as you pack, and watch your progress |

Other details:
- Input validation (for example, the end date can't be before the start date)
- Deleting a trip automatically removes its destinations, itinerary, expenses and packing items (`ON DELETE CASCADE`)
- Amounts are shown in Indian Rupees (₹)
- Data is stored locally in a SQLite database, so there is no external setup

---

## 🛠️ Tech Stack

- **Python 3**
- **Streamlit** for the user interface
- **SQLite** (via Python's built-in `sqlite3`) for storage
- **pandas** and **plotly** are listed in `requirements.txt` for data handling and charts

---

## 📁 Project Structure

```
TripCraft/
├── app.py             # Streamlit app: UI, navigation and page logic
├── database.py        # Database connection and table creation
├── requirements.txt   # Python dependencies
├── tripcraft.db       # SQLite database (created automatically on first run)
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone or download the project

```bash
git clone <your-repository-url>
cd TripCraft
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens in your browser, usually at `http://localhost:8501`. The database file `tripcraft.db` is created automatically the first time you run it.

---

## 🧭 How to Use

1. Go to **My Trips** and create your first trip.
2. Add places you want to visit in **Destinations**.
3. Plan your days in **Itinerary Planner**.
4. Record spending in **Budget Planner** to keep an eye on your remaining budget.
5. Build your checklist in **Packing Assistant** and tick items off as you pack.

> Destinations, itinerary, budget and packing all depend on a trip, so create one in **My Trips** first.

---

## 🗄️ Database Schema

All tables are linked to `trips` through `trip_id`.

| Table | Columns |
|-------|---------|
| `trips` | `trip_id`, `trip_name`, `destination`, `start_date`, `end_date`, `budget`, `travelers` |
| `destinations` | `destination_id`, `trip_id`, `place_name`, `category`, `notes` |
| `itinerary` | `itinerary_id`, `trip_id`, `plan_date`, `plan_time`, `activity`, `location`, `notes` |
| `expenses` | `expense_id`, `trip_id`, `category`, `description`, `amount`, `expense_date` |
| `packing_items` | `item_id`, `trip_id`, `item`, `packed` |

---

## 🔮 Future Improvements

- Edit existing trips, activities and expenses
- Expense breakdown charts by category (using Plotly)
- Filter the itinerary and destinations by trip
- Multi-currency support
- Export a trip plan as PDF

---

## 👩‍💻 Author

**<Your Name>**
MCA (AI & ML), Chandigarh University

---

## 📄 License

This project is for learning and personal use. Add a license of your choice here (for example, MIT).
