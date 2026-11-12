
import streamlit as st
from database import connect_db, create_tables
from datetime import date

# ==========================================
# TRIPCRAFT - SMART TRAVEL PLANNER
# ==========================================

st.set_page_config(
    page_title="TripCraft - Smart Travel Planner",
    page_icon="✈️",
    layout="wide"
)

create_tables()

# ==========================================
# DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #F4F7FB;
    color: #183B56;
}

h1, h2, h3 {
    color: #183B56 !important;
}

.stApp p, .stApp label {
    color: #334E68;
}

[data-testid="stSidebar"] {
    background-color: #E5EDF7;
}

[data-testid="stSidebar"] * {
    color: #183B56 !important;
}

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #D9E2EC;
}

[data-testid="stMetricLabel"] {
    color: #486581 !important;
}

[data-testid="stMetricValue"] {
    color: #102A43 !important;
}

.stButton > button {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# DATABASE HELPER FUNCTIONS
# ==========================================

def get_trips():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT trip_id, trip_name, destination, budget
        FROM trips
        ORDER BY trip_id DESC
    """)

    trips = cursor.fetchall()
    conn.close()

    return trips


def get_trip_options():
    trips = get_trips()

    return {
        trip[0]: f"{trip[1]} — {trip[2]}"
        for trip in trips
    }


def delete_record(table, column, record_id):
    allowed = {
        "trips": "trip_id",
        "destinations": "destination_id",
        "itinerary": "itinerary_id",
        "expenses": "expense_id",
        "packing_items": "item_id"
    }

    if table not in allowed:
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        f"DELETE FROM {table} WHERE {allowed[table]} = ?",
        (record_id,)
    )

    conn.commit()
    conn.close()


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("✈️ TripCraft")
st.sidebar.caption("Your journey, beautifully planned.")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "My Trips",
        "Destinations",
        "Itinerary Planner",
        "Budget Planner",
        "Packing Assistant"
    ]
)

st.sidebar.divider()
st.sidebar.info("Plan smarter. Travel happier.")

st.sidebar.caption("TripCraft | Smart Travel Planner")


# ==========================================
# 1. DASHBOARD
# ==========================================

if page == "Dashboard":

    st.title("Welcome to TripCraft ✈️")
    st.write("Your personal travel planning companion.")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM trips")
    total_trips = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM destinations")
    total_destinations = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(budget), 0) FROM trips")
    total_budget = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
    total_expenses = cursor.fetchone()[0]

    conn.close()

    st.markdown("### Your Travel Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Trips", total_trips)
    col2.metric("Saved Places", total_destinations)
    col3.metric("Total Budget", f"₹{total_budget:,.0f}")
    col4.metric("Total Expenses", f"₹{total_expenses:,.0f}")

    st.divider()

    st.markdown("### Your Travel Activity")

    trips = get_trips()

    if trips:
        for trip in trips:
            st.markdown(
                f"**✈️ {trip[1]}** — {trip[2]} | Budget: ₹{trip[3]:,.0f}"
            )
    else:
        st.info("You haven't created any trips yet.")

    st.markdown("### Explore the world!")
    st.write(
        "Plan your destinations, organize your itinerary, "
        "manage expenses and prepare your packing checklist."
    )


# ==========================================
# 2. MY TRIPS
# ==========================================

elif page == "My Trips":

    st.title("🧳 My Trips")
    st.write("Create and manage your travel plans.")

    st.markdown("### Create a New Trip")

    with st.form("trip_form"):

        trip_name = st.text_input("Trip Name")
        destination = st.text_input("Main Destination")

        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input(
                "Start Date",
                value=date.today()
            )

        with col2:
            end_date = st.date_input(
                "End Date",
                value=date.today()
            )

        budget = st.number_input(
            "Estimated Budget (₹)",
            min_value=0.0,
            step=500.0
        )

        travelers = st.number_input(
            "Number of Travelers",
            min_value=1,
            step=1
        )

        submitted = st.form_submit_button("➕ Save Trip")

        if submitted:

            if not trip_name.strip() or not destination.strip():
                st.error("Please enter the trip name and destination.")

            elif end_date < start_date:
                st.error("End date cannot be before start date.")

            else:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO trips
                    (trip_name, destination, start_date,
                     end_date, budget, travelers)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    trip_name.strip(),
                    destination.strip(),
                    str(start_date),
                    str(end_date),
                    budget,
                    travelers
                ))

                conn.commit()
                conn.close()

                st.success("Your trip has been saved successfully! ✈️")

    st.divider()
    st.markdown("### Your Saved Trips")

    trips = get_trips()

    if trips:

        for trip in trips:

            with st.expander(f"✈️ {trip[1]} - {trip[2]}"):

                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT start_date, end_date, budget, travelers "
                    "FROM trips WHERE trip_id = ?",
                    (trip[0],)
                )

                details = cursor.fetchone()
                conn.close()

                st.write(f"**Start Date:** {details[0]}")
                st.write(f"**End Date:** {details[1]}")
                st.write(f"**Budget:** ₹{details[2]:,.0f}")
                st.write(f"**Travelers:** {details[3]}")

                if st.button(
                    "🗑️ Delete Trip",
                    key=f"delete_trip_{trip[0]}"
                ):
                    delete_record("trips", "trip_id", trip[0])
                    st.success("Trip deleted successfully!")
                    st.rerun()

    else:
        st.info("No trips added yet. Create your first trip!")


# ==========================================
# 3. DESTINATIONS
# ==========================================

elif page == "Destinations":

    st.title("📍 Destinations")
    st.write("Discover and save places you want to visit.")

    trip_options = get_trip_options()

    if not trip_options:

        st.warning("Please create a trip in My Trips first.")

    else:

        st.markdown("### Add a Destination")

        with st.form("destination_form"):

            selected_trip = st.selectbox(
                "Select Trip",
                options=list(trip_options.keys()),
                format_func=lambda x: trip_options[x]
            )

            place_name = st.text_input("Place Name")

            category = st.selectbox(
                "Category",
                [
                    "Sightseeing",
                    "Nature",
                    "Food",
                    "Shopping",
                    "Adventure",
                    "Accommodation",
                    "Other"
                ]
            )

            notes = st.text_area("Description / Notes")

            submitted = st.form_submit_button("➕ Add Destination")

            if submitted:

                if not place_name.strip():
                    st.error("Please enter a place name.")

                else:
                    conn = connect_db()
                    cursor = conn.cursor()

                    cursor.execute("""
                        INSERT INTO destinations
                        (trip_id, place_name, category, notes)
                        VALUES (?, ?, ?, ?)
                    """, (
                        selected_trip,
                        place_name.strip(),
                        category,
                        notes.strip()
                    ))

                    conn.commit()
                    conn.close()

                    st.success("Destination added successfully!")

        st.divider()
        st.markdown("### Your Saved Destinations")

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT d.destination_id, d.place_name, d.category,
                   d.notes, t.trip_name
            FROM destinations d
            JOIN trips t ON d.trip_id = t.trip_id
            ORDER BY d.destination_id DESC
        """)

        destinations = cursor.fetchall()
        conn.close()

        if destinations:

            for place in destinations:

                with st.expander(f"📍 {place[1]} — {place[4]}"):

                    st.write(f"**Category:** {place[2]}")
                    st.write(f"**Notes:** {place[3] or 'No notes added'}")

                    if st.button(
                        "🗑️ Delete Destination",
                        key=f"delete_destination_{place[0]}"
                    ):
                        delete_record(
                            "destinations",
                            "destination_id",
                            place[0]
                        )
                        st.rerun()

        else:
            st.info("No destinations saved yet.")


# ==========================================
# 4. ITINERARY PLANNER
# ==========================================

elif page == "Itinerary Planner":

    st.title("📅 Itinerary Planner")
    st.write("Organize your travel activities day by day.")

    trip_options = get_trip_options()

    if not trip_options:

        st.warning("Please create a trip in My Trips first.")

    else:

        st.markdown("### Schedule an Activity")

        with st.form("itinerary_form"):

            selected_trip = st.selectbox(
                "Select Trip",
                options=list(trip_options.keys()),
                format_func=lambda x: trip_options[x]
            )

            plan_date = st.date_input(
                "Activity Date",
                value=date.today()
            )

            plan_time = st.time_input("Activity Time")

            activity = st.text_input("Activity Name")
            location = st.text_input("Location")
            notes = st.text_area("Additional Notes")

            submitted = st.form_submit_button("➕ Add Activity")

            if submitted:

                if not activity.strip():
                    st.error("Please enter an activity name.")

                else:
                    conn = connect_db()
                    cursor = conn.cursor()

                    cursor.execute("""
                        INSERT INTO itinerary
                        (trip_id, plan_date, plan_time,
                         activity, location, notes)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        selected_trip,
                        str(plan_date),
                        str(plan_time),
                        activity.strip(),
                        location.strip(),
                        notes.strip()
                    ))

                    conn.commit()
                    conn.close()

                    st.success("Activity added to your itinerary!")

        st.divider()
        st.markdown("### Your Travel Schedule")

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.itinerary_id, i.plan_date, i.plan_time,
                   i.activity, i.location, i.notes, t.trip_name
            FROM itinerary i
            JOIN trips t ON i.trip_id = t.trip_id
            ORDER BY i.plan_date, i.plan_time
        """)

        activities = cursor.fetchall()
        conn.close()

        if activities:

            for item in activities:

                with st.expander(
                    f"📅 {item[1]} | {item[2]} | {item[3]}"
                ):

                    st.write(f"**Trip:** {item[6]}")
                    st.write(f"**Location:** {item[4] or 'Not specified'}")
                    st.write(f"**Notes:** {item[5] or 'No notes added'}")

                    if st.button(
                        "🗑️ Delete Activity",
                        key=f"delete_activity_{item[0]}"
                    ):
                        delete_record(
                            "itinerary",
                            "itinerary_id",
                            item[0]
                        )
                        st.rerun()

        else:
            st.info("Your itinerary is empty. Add your first activity!")


# ==========================================
# 5. BUDGET PLANNER
# ==========================================

elif page == "Budget Planner":

    st.title("💰 Budget Planner")
    st.write("Track your travel spending and manage your budget.")

    trip_options = get_trip_options()

    if not trip_options:

        st.warning("Please create a trip in My Trips first.")

    else:

        selected_trip = st.selectbox(
            "Select Trip",
            options=list(trip_options.keys()),
            format_func=lambda x: trip_options[x],
            key="budget_trip"
        )

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT budget FROM trips WHERE trip_id = ?",
            (selected_trip,)
        )

        estimated_budget = cursor.fetchone()[0] or 0

        cursor.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses "
            "WHERE trip_id = ?",
            (selected_trip,)
        )

        total_spent = cursor.fetchone()[0]

        conn.close()

        remaining = estimated_budget - total_spent

        st.markdown("### Budget Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Estimated Budget", f"₹{estimated_budget:,.0f}")
        col2.metric("Total Spent", f"₹{total_spent:,.0f}")
        col3.metric("Remaining", f"₹{remaining:,.0f}")

        if estimated_budget > 0:
            progress = min(total_spent / estimated_budget, 1.0)
            st.progress(progress)
            st.caption(f"{progress * 100:.1f}% of your budget used")

        if remaining < 0:
            st.warning("You have exceeded your estimated budget!")

        st.divider()
        st.markdown("### Add an Expense")

        with st.form("expense_form"):

            expense_category = st.selectbox(
                "Expense Category",
                [
                    "Transport",
                    "Accommodation",
                    "Food",
                    "Shopping",
                    "Activities",
                    "Other"
                ]
            )

            description = st.text_input("Expense Description")

            amount = st.number_input(
                "Amount (₹)",
                min_value=0.0,
                step=100.0
            )

            expense_date = st.date_input(
                "Expense Date",
                value=date.today()
            )

            submitted = st.form_submit_button("➕ Add Expense")

            if submitted:

                if not description.strip():
                    st.error("Please enter an expense description.")

                elif amount <= 0:
                    st.error("Please enter an amount greater than zero.")

                else:
                    conn = connect_db()
                    cursor = conn.cursor()

                    cursor.execute("""
                        INSERT INTO expenses
                        (trip_id, category, description, amount, expense_date)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        selected_trip,
                        expense_category,
                        description.strip(),
                        amount,
                        str(expense_date)
                    ))

                    conn.commit()
                    conn.close()

                    st.success("Expense recorded successfully!")

        st.divider()
        st.markdown("### Expense History")

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT expense_id, category, description,
                   amount, expense_date
            FROM expenses
            WHERE trip_id = ?
            ORDER BY expense_date DESC, expense_id DESC
        """, (selected_trip,))

        expenses = cursor.fetchall()
        conn.close()

        if expenses:

            for expense in expenses:

                with st.expander(
                    f"₹{expense[3]:,.0f} — {expense[2]}"
                ):

                    st.write(f"**Category:** {expense[1]}")
                    st.write(f"**Date:** {expense[4]}")

                    if st.button(
                        "🗑️ Delete Expense",
                        key=f"delete_expense_{expense[0]}"
                    ):
                        delete_record(
                            "expenses",
                            "expense_id",
                            expense[0]
                        )
                        st.rerun()

        else:
            st.info("No expenses recorded for this trip yet.")


# ==========================================
# 6. PACKING ASSISTANT
# ==========================================

elif page == "Packing Assistant":

    st.title("🎒 Packing Assistant")
    st.write("Prepare your luggage with a personalized checklist.")

    trip_options = get_trip_options()

    if not trip_options:

        st.warning("Please create a trip in My Trips first.")

    else:

        selected_trip = st.selectbox(
            "Select Trip",
            options=list(trip_options.keys()),
            format_func=lambda x: trip_options[x],
            key="packing_trip"
        )

        st.markdown("### Add Packing Items")

        with st.form("packing_form"):

            item_name = st.text_input("Item Name")

            submitted = st.form_submit_button("➕ Add Item")

            if submitted:

                if not item_name.strip():
                    st.error("Please enter an item name.")

                else:
                    conn = connect_db()
                    cursor = conn.cursor()

                    cursor.execute("""
                        INSERT INTO packing_items (trip_id, item)
                        VALUES (?, ?)
                    """, (
                        selected_trip,
                        item_name.strip()
                    ))

                    conn.commit()
                    conn.close()

                    st.success("Item added to your packing list!")

        st.divider()
        st.markdown("### Your Packing Checklist")

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT item_id, item, packed
            FROM packing_items
            WHERE trip_id = ?
            ORDER BY item_id DESC
        """, (selected_trip,))

        items = cursor.fetchall()
        conn.close()

        if items:

            packed_count = sum(item[2] for item in items)
            total_items = len(items)

            st.metric("Items Packed", f"{packed_count}/{total_items}")

            st.progress(packed_count / total_items)

            for item in items:

                col1, col2 = st.columns([5, 1])

                with col1:

                    item_key = f"packed_{item[0]}"

                    if item_key not in st.session_state:
                        st.session_state[item_key] = bool(item[2])

                    checked = st.checkbox(
                        item[1],
                        key=item_key
                    )

                    if checked != bool(item[2]):

                        conn = connect_db()
                        cursor = conn.cursor()

                        cursor.execute("""
                            UPDATE packing_items
                            SET packed = ?
                            WHERE item_id = ?
                        """, (
                            int(checked),
                            item[0]
                        ))

                        conn.commit()
                        conn.close()

                        st.rerun()

                with col2:

                    if st.button(
                        "🗑️",
                        key=f"delete_item_{item[0]}"
                    ):
                        delete_record(
                            "packing_items",
                            "item_id",
                            item[0]
                        )

                        st.session_state.pop(item_key, None)
                        st.rerun()

            if packed_count == total_items:
                st.success("Everything is packed. You're ready to go! ✈️")

        else:
            st.info("Your packing checklist is empty. Add your first item!")
