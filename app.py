import streamlit as st

import json

DATA_FILE = "products.json"

def load_products():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"urls": []}

def save_products(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

st.title("Ürün Takip Sistemi")

products = load_products()

with st.form("add_product"):
    store = st.selectbox("Mağaza", ["zara", "bershka"])
    url = st.text_input("Ürün Linki")
    sizes = st.text_input("Bedenler (virgül ile ayırın, örn: S,M,L)")
    submitted = st.form_submit_button("Ekle")

    if submitted:
        if url and sizes:
            size_list = [s.strip() for s in sizes.split(",")]
            products["urls"].append({
                "store": store,
                "url": url,
                "sizes": size_list
            })
            save_products(products)
            st.success("Ürün eklendi!")

st.subheader("Takip edilen ürünler")

# Burada ürünleri listelerken her satıra bir "Sil" butonu koyuyoruz.
# Sil butonuna tıklanırsa o ürünü siliyoruz.
for i, p in enumerate(products["urls"]):
    cols = st.columns([8, 1])  # genişlik oranları: metin 8, buton 1
    cols[0].write(f"- {p['store']} : {p['url']} | Bedenler: {', '.join(p['sizes'])}")
    if cols[1].button("Sil", key=f"delete_{i}"):
        products["urls"].pop(i)
        save_products(products)
        st.experimental_rerun()  # sayfayı yenile ki değişiklik görünür
