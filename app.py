import requests
from reportlab.pdfgen import canvas
import streamlit as st
import json
import os
from openai import OpenAI
if "trip_history" not in st.session_state:
    st.session_state.trip_history = []

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Trip Planner AI",
    page_icon="🌍",
    layout="wide"
)


# -------------------------
# OPENROUTER CLIENT
# -------------------------
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)
def create_pdf(text):

    pdf_file = "trip_itinerary.pdf"

    c = canvas.Canvas(pdf_file)

    y = 800

    for line in text.split("\n"):
        c.drawString(40, y, line[:100])
        y -= 20

        if y < 40:
            c.showPage()
            y = 800

    c.save()

    return pdf_file
def get_weather(city):
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    print(response.status_code)
    print(response.text)

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        return f"{temp}°C, {weather.title()}"

    return "Weather not available"
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)
# Load all registered users
users = load_users()
# -------------------------
# CUSTOM CSS
# -------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b,#334155);
    color: white;
}



.overlay{
    width:100%;
    height:100%;
    background:rgba(0,0,0,.35);
    border-radius:25px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
}

.overlay h1{
    color:white;
    font-size:60px;
    font-weight:bold;
}

.overlay p{
    color:white;
    font-size:22px;
}

/* Cards */
.card{
    background:white;
    border-radius:20px;
    padding:20px;
    box-shadow:0 10px 30px rgba(0,0,0,.15);
    transition:0.4s;
}

.card:hover{
    transform:translateY(-10px);
}

.stButton>button{
    background:#5B5CEB;
    color:white;
    border-radius:12px;
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.08);
    box-shadow:0 0 20px #5B5CEB;
}
.fade{
    animation: fadeIn 1.2s;
}

@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(30px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# LOGIN / SIGNUP
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

users = load_users()

if not st.session_state.logged_in:

    st.sidebar.title("🔐 Login / Signup")

    choice = st.sidebar.selectbox(
        "Select",
        ["Login", "Sign Up"]
    )

    if choice == "Sign Up":

        new_user = st.sidebar.text_input("Username")
        new_pass = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Create Account"):

            if new_user in users:
                st.sidebar.error("Username already exists!")
            else:
                users[new_user] = new_pass
                save_users(users)
                st.sidebar.success("Account created successfully!")

    elif choice == "Login":

        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):

            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.sidebar.error("Invalid username or password")

else:

    st.sidebar.success(f"👋 Welcome {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
  


# -------------------------
# HERO SECTION
# -------------------------
st.image(
    "assets/banner.png.png",
    use_container_width=True
)
st.success(
    "🎉 Welcome to Trip Planner AI! Generate personalized travel itineraries in seconds."
)
if not st.session_state.logged_in:

    st.warning("🔐 Please login first.")

    st.stop()

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.title("⚙️ Trip Settings")

    destination = st.text_input(
        "Destination",
        placeholder="Goa, Jaipur, Kerala, Hyderabad..."
    )

    if destination:
        weather = get_weather(destination)
        st.success(f"🌦️ {weather}")

    days = st.slider("Number of Days", 1, 15, 3)

    budget = st.selectbox(
        "Budget",
        ["Budget", "Mid-Range", "Luxury"]
    )

    interests = st.multiselect(
        "Interests",
        ["Food", "Adventure", "Nature", "History", "Shopping", "Religious"]
    )

    generate = st.button("🚀 Generate Trip")

    st.markdown("---")
    st.subheader("📜 Previous Trips")

    for trip in st.session_state.trip_history:
        st.write(f"📍 {trip['destination']} ({trip['days']} days)")

# -------------------------
# FEATURE CARDS
# -------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("✈️ AI Itinerary")

with c2:
    st.info("🏨 Hotels")

with c3:
    st.info("🍽️ Food Guide")

with c4:
    st.info("🌦️ Travel Tips")
    
st.markdown("""
<div class="fade">
<h2>🌍 Popular Destinations</h2>
</div>
""", unsafe_allow_html=True)

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.image("https://images.unsplash.com/photo-1512343879784-a960bf40e7f2")
    st.caption("Goa")

with col2:
    st.image("https://images.unsplash.com/photo-1477587458883-47145ed94245")
    st.caption("Jaipur")

with col3:
    st.image("https://images.unsplash.com/photo-1602216056096-3b40cc0c9944")
    st.caption("Kerala")
with col4:
    st.image("https://images.unsplash.com/photo-1567157577867-05ccb1388e66")
    st.caption("Mumbai")

    if st.button("📍 Explore Mumbai"):
        st.info("Mumbai selected")   

# -------------------------
# ITINERARY
# -------------------------

if generate:

    if not destination:
        st.warning("Please enter a destination.")
        st.stop()

    prompt = f"""
    You are an expert travel planner.

    Destination: {destination}
    Duration: {days} days
    Budget: {budget}
    Interests: {', '.join(interests)}

Create:
1. Day-wise itinerary
2. Morning, Afternoon, Evening plans
3. Famous food recommendations
4. Budget estimate in INR
5. Travel hacks
6. Best photo spots
7. Local phrases
8. Safety tips
    Use beautiful markdown.
    """

    with st.spinner("✈️ Planning your dream trip..."):

        response = client.chat.completions.create(
     model="nex-agi/nex-n2-pro:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        itinerary = response.choices[0].message.content

        st.session_state.trip_history.append(
            {
                "destination": destination,
                "days": days
            }
        )

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown("## 📍 Your Personalized Itinerary")
            st.markdown(itinerary)
            st.balloons()

            maps_url = f"https://www.google.com/maps/search/{destination}"

            st.link_button(
             "🗺️ Open in Google Maps",
                   maps_url)

            pdf_file = create_pdf(itinerary)

            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="📄 Download Itinerary PDF",
                    data=file,
                    file_name="TripPlannerAI_Itinerary.pdf",
                    mime="application/pdf"
                )

        with col2:
            st.markdown("""
            <div class="card">
            <h3>💡 Travel Tips</h3>
            <ul>
            <li>Carry ID proof</li>
            <li>Use UPI payments</li>
            <li>Keep emergency contacts saved</li>
            <li>Stay hydrated</li>
            <li>Book tickets early</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

# -------------------------
# CHATBOT
# -------------------------

st.divider()

st.subheader("🤖 Travel Assistant")

user_question = st.chat_input(
    "Ask anything about your trip..."
)

if user_question:

    answer = client.chat.completions.create(
        model="nex-agi/nex-n2-pro:free",
        messages=[
            {
                "role": "system",
                "content": """
                You are Trip Planner AI, a travel assistant created by Shiva.
                """
            },
            {
                "role": "user",
                "content": f"For a trip to {destination}, answer: {user_question}"
            }
        ]
    )

    st.chat_message("user").write(user_question)

    st.chat_message("assistant").write(
        answer.choices[0].message.content
    )
st.markdown("---")

st.markdown(
    "<center>🌍 Trip Planner AI | Built by Shiva 🚀</center>",
    unsafe_allow_html=True
)