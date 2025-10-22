import streamlit as st
import pandas as pd
from catboost import CatBoostClassifier
import json, os, hashlib

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="FarmerIQ", page_icon="🌾", layout="wide")

# -------------------- THEME & DYNAMIC BACKGROUNDS --------------------
def apply_background(product=None):
    """Apply animated background dynamically based on selected product."""
    gifs = {
        "milk": "https://cdn.dribbble.com/users/220167/screenshots/2097727/media/38e7e888cb9f733bff7ce646d1f77c09.gif",
        "eggs": "https://cdn.dribbble.com/users/1226935/screenshots/6340898/eggs.gif",
        "honey": "https://cdn.dribbble.com/users/591017/screenshots/3822362/honey_drip.gif",
        "fruits": "https://cdn.dribbble.com/users/1395642/screenshots/5587985/fruits_animation.gif",
        "vegetables": "https://cdn.dribbble.com/users/5976/screenshots/2958764/veggies.gif",
    }

    if not product:
        # Default gradient for login page
        st.markdown("""
            <style>
            div[data-testid="stAppViewContainer"] > .main {
                background: linear-gradient(135deg, #e8f5e9, #f1f8e9, #f9fbe7);
                background-attachment: fixed;
                font-family: 'Poppins', sans-serif;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        gif_url = gifs.get(product, "")
        st.markdown(f"""
            <style>
            div[data-testid="stAppViewContainer"] > .main {{
                background: url('{gif_url}');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                color: #1B4332;
                transition: background 1s ease-in-out;
            }}
            </style>
        """, unsafe_allow_html=True)

# Apply background dynamically
apply_background(st.session_state.get("selected_product", None))

# -------------------- SECURITY FUNCTIONS --------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f: json.dump({"users": []}, f)
    with open("users.json", "r") as f:
        return json.load(f)["users"]

def save_users(users):
    with open("users.json", "w") as f:
        json.dump({"users": users}, f, indent=4)

def user_exists(username):
    return any(u["username"] == username for u in load_users())

def register_user(username, password):
    users = load_users()
    users.append({"username": username, "password": hash_password(password)})
    save_users(users)

def check_login(username, password):
    hashed_input = hash_password(password)
    for user in load_users():
        if user["username"] == username and user["password"] == hashed_input:
            return True
    return False

# -------------------- SESSION STATE --------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "mode" not in st.session_state:
    st.session_state["mode"] = "login"
if "selected_product" not in st.session_state:
    st.session_state["selected_product"] = None

# -------------------- LOGIN / SIGNUP --------------------
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <div style='text-align:center; margin-top:20px;'>
            <h2 style='margin-bottom:5px;'>🌾 FarmerIQ</h2>
            <p style='color:gray; font-size:16px;'>Login or Create your Farmer Account</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Center buttons
    c1, c2,c3= st.columns([2, 1,2])
    with c2:
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🔑 Login"):
                st.session_state["mode"] = "login"
        with b2:
            if st.button("🆕 Sign Up"):
                st.session_state["mode"] = "signup"

    st.write("---")

    if st.session_state["mode"] == "login":
        st.subheader("Login to Continue")
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")

        if st.button("Login Now"):
            if not username or not password:
                st.warning("⚠️ Please fill in all fields.")
            elif check_login(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success(f"✅ Welcome back, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

    elif st.session_state["mode"] == "signup":
        st.subheader("Create a New Account")
        username = st.text_input("👤 Choose a Username")
        password = st.text_input("🔒 Create Password", type="password")
        confirm = st.text_input("🔁 Confirm Password", type="password")

        if st.button("Create Account"):
            if not username or not password:
                st.warning("⚠️ Please fill in all fields.")
            elif password != confirm:
                st.error("❌ Passwords do not match.")
            elif user_exists(username):
                st.error("⚠️ Username already exists. Try another.")
            else:
                register_user(username, password)
                st.success("✅ Account created! You can now log in.")
                st.session_state["mode"] = "login"
                st.rerun()

    st.stop()

# -------------------- LOGOUT --------------------
if st.sidebar.button("🚪 Logout"):
    st.session_state["authenticated"] = False
    st.session_state["selected_product"] = None
    st.rerun()

# -------------------- MODEL LOAD --------------------
model = CatBoostClassifier()
model.load_model("quality_grade_model.cbm")
expected_features = model.feature_names_

# -------------------- HOMEPAGE --------------------
if st.session_state["selected_product"] is None:
    st.title(f"🌾 Welcome, {st.session_state['username']}!")
    st.subheader("Select a Product to Analyze Quality and Profit")

    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button("🥛"):
        st.session_state["selected_product"] = "milk"; st.rerun()
    col1.write("**Milk**")

    if col2.button("🥚"):
        st.session_state["selected_product"] = "eggs"; st.rerun()
    col2.write("**Eggs**")

    if col3.button("🍯"):
        st.session_state["selected_product"] = "honey"; st.rerun()
    col3.write("**Honey**")

    if col4.button("🍎"):
        st.session_state["selected_product"] = "fruits"; st.rerun()
    col4.write("**Fruits**")

    if col5.button("🥕"):
        st.session_state["selected_product"] = "vegetables"; st.rerun()
    col5.write("**Vegetables**")

    st.stop()

# -------------------- PRODUCT LOGIC --------------------
product = st.session_state["selected_product"]
if st.button("⬅ Back to Home"):
    st.session_state["selected_product"] = None
    st.rerun()

st.title(f"🔍 {product.capitalize()} Quality Prediction")

# Shared options
units_dict = {
    'milk': ['liters','ml'],
    'eggs': ['pieces','dozens'],
    'honey': ['kg','g'],
    'fruits': ['kg','g','pieces'],
    'vegetables': ['kg','g','pieces']
}
milk_animals = ['cow','buffalo','goat']
egg_sizes = ['small','medium','large']
egg_conditions = ['clean','dirty']
honey_types = ['light','dark']
fruits_list = ['mango','apple','banana','grapes','papaya','pineapple','guava','orange','pear',
               'kiwi','strawberry','blueberry','watermelon','pomegranate','lychee','cherry','peach']
vegetables_list = ['spinach','tomato','potato','onion','carrot','cabbage','cauliflower','cucumber','pepper',
                   'lettuce','radish','beetroot','chilli','broccoli','zucchini','eggplant','beans','pumpkin']
storage_options = ['room','refrigerated']
all_columns = ['product','animal','time_of_day','storage','days_since','density','fat','snf','size','condition',
               'type','purity','moisture','name','ripeness','color','quantity','freshness']
cat_features = ['product','animal','time_of_day','storage','size','condition','type','name','ripeness','color']
input_data = {col:0 for col in all_columns}
for cat in cat_features:
    input_data[cat] = 'unknown'

# Inputs
if product == 'milk':
    animal = st.selectbox("Animal", milk_animals)
    time_of_day = st.selectbox("Time of Day", ['morning','evening'])
    storage = st.selectbox("Storage", storage_options)
    days_since = st.number_input("Days Since Milking", 0,7,0)
    unit = st.selectbox("Units", units_dict['milk'])
    quantity = st.number_input("Quantity", 1,100,1)
    if animal=='cow': density,fat,snf=1.03,3.5,8.5
    elif animal=='buffalo': density,fat,snf=1.04,6.5,9.0
    else: density,fat,snf=1.032,4.5,8.0
    freshness=max(0,100-days_since*15)
    input_data.update({'product':'milk','animal':animal,'time_of_day':time_of_day,'storage':storage,
                       'days_since':days_since,'density':density,'fat':fat,'snf':snf,
                       'quantity':quantity,'freshness':freshness})
elif product == 'eggs':
    size=st.selectbox("Size",egg_sizes)
    condition=st.selectbox("Condition",egg_conditions)
    storage=st.selectbox("Storage",storage_options)
    days_since=st.number_input("Days Since Laying",0,14,0)
    unit = st.selectbox("Units", units_dict['eggs'])
    quantity = st.number_input("Quantity",1,100,1)
    freshness=max(0,100-days_since*7)
    input_data.update({'product':'eggs','size':size,'condition':condition,'storage':storage,
                       'days_since':days_since,'quantity':quantity,'freshness':freshness})
elif product == 'honey':
    htype=st.selectbox("Honey Type",honey_types)
    storage=st.selectbox("Storage",storage_options)
    days_since=st.number_input("Days Since Harvest",0,365,0)
    unit = st.selectbox("Units", units_dict['honey'])
    quantity = st.number_input("Quantity",1,50,1)
    purity = 85 if htype=='light' else 80
    moisture = 17 if htype=='light' else 20
    freshness=max(0,100-days_since*0.1)
    input_data.update({'product':'honey','type':htype,'storage':storage,
                       'days_since':days_since,'purity':purity,'moisture':moisture,
                       'quantity':quantity,'freshness':freshness})
else:
    name = st.selectbox("Name", fruits_list if product=='fruits' else vegetables_list)
    size = st.selectbox("Size",['small','medium','large'])
    ripeness = st.selectbox("Ripeness",['soft','medium','hard'])
    color = st.selectbox("Color",['green','red','yellow'])
    storage = st.selectbox("Storage", storage_options)
    days_since = st.number_input("Days Since Harvest",0,7,0)
    unit = st.selectbox("Units", units_dict[product])
    quantity = st.number_input("Quantity",1,50,1)
    freshness=max(0,100-days_since*10)
    input_data.update({'product':product,'name':name,'size':size,'ripeness':ripeness,'color':color,
                       'storage':storage,'days_since':days_since,'quantity':quantity,'freshness':freshness})

# Profit & Prediction
unit_price = st.number_input(f"Enter Price per {unit}", min_value=0.0, step=0.1)
total_value = unit_price * quantity
actions, profit_loss_percent = [], 0

if product == 'milk':
    if freshness >= 80:
        actions.append("Milk is very fresh. Sell immediately for best quality.")
    elif freshness >= 50:
        actions.append("Milk quality is moderate. Sell within 1–2 days.")
        profit_loss_percent = (100 - freshness) * 0.5
    else:
        actions.append("Milk is low quality. Consider processing into cheese or yogurt.")
        profit_loss_percent = (100 - freshness)
    if storage == 'refrigerated':
        actions.append("Refrigerated storage extends shelf life.")
elif product == 'eggs':
    if freshness >= 80:
        actions.append("Eggs are very fresh. Sell immediately.")
    elif freshness >= 50:
        actions.append("Eggs are moderate. Sell soon or use in baking.")
        profit_loss_percent = (100 - freshness) * 0.4
    else:
        actions.append("Eggs are old. Consider cooking or discarding.")
        profit_loss_percent = (100 - freshness) * 0.8
elif product == 'honey':
    actions.append("Honey is stable for long-term storage.")
    if freshness < 50:
        actions.append("Sell quickly to maintain aroma and taste.")
        profit_loss_percent = (100 - freshness) * 0.2
else:
    if freshness >= 80:
        actions.append(f"{name.capitalize()} is very fresh. Best to sell immediately.")
    elif freshness >= 50:
        actions.append(f"{name.capitalize()} quality is moderate. Sell within 2 days.")
        profit_loss_percent = (100 - freshness) * 0.5
    else:
        actions.append(f"{name.capitalize()} quality is low. Consider processing or discounts.")
        profit_loss_percent = (100 - freshness) * 0.9

estimated_profit = total_value * (1 - profit_loss_percent/100)

if st.button("Predict Quality Grade"):
    input_df = pd.DataFrame([input_data])
    input_df = input_df.reindex(columns=expected_features, fill_value=0)
    pred = model.predict(input_df)[0]

    st.subheader("Freshness Status:")
    if freshness >= 80:
        st.success(f"Freshness is high: {freshness:.1f}% ✅")
    elif freshness >= 50:
        st.warning(f"Freshness is moderate: {freshness:.1f}% ⚠")
    else:
        st.error(f"Freshness is low: {freshness:.1f}% ❌")

    st.subheader("Predicted Quality Grade:")
    st.success(pred)

    st.subheader("Suggested Actions:")
    for act in actions:
        st.info(act)

    st.subheader("Estimated Profit:")
    st.success(f"💰 Estimated profit: {estimated_profit:.2f} per {unit}")


