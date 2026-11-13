
import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="MediQueue | ระบบติดตามคิวรับยา",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CSS DESIGN
# =====================================
st.markdown("""
<style>
.stApp {
    background-color: #F1F5F9;
}
[data-testid="stSidebar"] {
    background-color: #E8F1FC;
}
.main-title {
    background: linear-gradient(120deg,#1769D2,#4299E1);
    padding: 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 20px;
}
.main-title h1 {
    color: white;
    font-size: 30px;
}
.main-title p {
    color: #E5EEFF;
}
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    min-height: 125px;
}
.metric-label {
    color: #64748B;
    font-size: 14px;
}
.metric-value {
    font-size: 30px;
    font-weight: bold;
    margin-top: 8px;
}
.section-card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    margin-bottom: 15px;
}
.stButton button {
    background-color: #1769D2;
    color: white;
    border-radius: 10px;
    border: none;
    width: 100%;
}
.stButton button:hover {
    background-color: #1255AD;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# SAMPLE DATA
# =====================================
queue_data = pd.DataFrame({
    "หมายเลขคิว": [
        "A021", "A022", "A023", "A024",
        "A025", "A026", "A027", "A028"
    ],
    "สถานะ": [
        "กำลังจัดยา", "กำลังจัดยา",
        "รอรับยา", "รอรับยา",
        "รอรับยา", "รอรับยา",
        "รอรับยา", "จ่ายยาแล้ว"
    ],
    "เวลารอโดยประมาณ": [
        5, 10, 15, 20, 25, 30, 35, 0
    ]
})

total_queue = 120
waiting_queue = 25
completed_queue = 95
average_wait = 28

# =====================================
# SIDEBAR
# =====================================
st.sidebar.markdown("## 🏥 MediQueue")
st.sidebar.caption("Hospital Pharmacy System")
st.sidebar.divider()

menu = st.sidebar.radio(
    "เมนูการใช้งาน",
    [
        "หน้าหลัก",
        "ตรวจสอบคิว",
        "พยากรณ์เวลารอ",
        "จัดการระบบ"
    ]
)

st.sidebar.divider()
st.sidebar.info(
    "ระบบต้นแบบสำหรับการศึกษา "
    "ข้อมูลที่แสดงเป็นข้อมูลจำลอง"
)

# =====================================
# HEADER
# =====================================
st.markdown("""
<div class="main-title">
    <h1>🏥 ระบบติดตามคิวรับยา</h1>
    <p>ตรวจสอบสถานะคิวและเวลารอรับยาที่คาดการณ์ได้</p>
    <p>Hospital Pharmacy Queue System</p>
</div>
""", unsafe_allow_html=True)

# =====================================
# PAGE 1 : HOME
# =====================================
if menu == "หน้าหลัก":

    st.subheader("📊 ภาพรวมการให้บริการห้องยา")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">👥 คิวทั้งหมดวันนี้</div>
            <div class="metric-value" style="color:#2563EB">
                120
            </div>
            <div class="metric-label">คิว</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">🕒 เวลารอเฉลี่ย</div>
            <div class="metric-value" style="color:#D97706">
                28
            </div>
            <div class="metric-label">นาที</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">⌛ กำลังรอรับยา</div>
            <div class="metric-value" style="color:#7C3AED">
                25
            </div>
            <div class="metric-label">คิว</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">✅ จ่ายยาแล้ว</div>
            <div class="metric-value" style="color:#059669">
                95
            </div>
            <div class="metric-label">คิว</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Queue table
    st.markdown("""
    <div class="section-card">
        <h3>📋 สถานะคิวรับยาปัจจุบัน</h3>
    </div>
    """, unsafe_allow_html=True)

    display_data = queue_data[
        ["หมายเลขคิว", "สถานะ"]
    ]

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "ข้อมูลตัวอย่างสำหรับแสดงรูปแบบหน้า Dashboard"
    )

# =====================================
# PAGE 2 : CHECK QUEUE
# =====================================
elif menu == "ตรวจสอบคิว":

    st.subheader("🔍 ตรวจสอบสถานะคิวรับยา")

    st.write(
        "กรอกหมายเลขคิวของคุณเพื่อตรวจสอบสถานะ"
    )

    queue_number = st.text_input(
        "หมายเลขคิว",
        placeholder="ตัวอย่าง A025"
    ).strip().upper()

    if st.button("🔎 ตรวจสอบคิว"):

        result = queue_data[
            queue_data["หมายเลขคิว"] == queue_number
        ]

        if not result.empty:

            row = result.iloc[0]

            st.success("พบข้อมูลหมายเลขคิวของคุณ")

            st.markdown(
                f"""
                <div class="section-card">
                    <h3>หมายเลขคิว: {row['หมายเลขคิว']}</h3>
                    <h2 style="color:#1769D2">
                        {row['สถานะ']}
                    </h2>
                    <p>เวลารอโดยประมาณ</p>
                    <h1 style="color:#1769D2">
                        {row['เวลารอโดยประมาณ']} นาที
                    </h1>
                </div>
                """,
                unsafe_allow_html=True
            )

            if row["สถานะ"] == "จ่ายยาแล้ว":
                st.success("คุณได้รับยาเรียบร้อยแล้ว")

            else:
                queue_index = queue_data.index[
                    queue_data["หมายเลขคิว"] == queue_number
                ][0]

                st.info(
                    f"ลำดับคิวในรายการตัวอย่าง: "
                    f"{queue_index + 1}"
                )

        else:
            st.error(
                "ไม่พบหมายเลขคิว กรุณาตรวจสอบอีกครั้ง"
            )

# =====================================
# PAGE 3 : PREDICTION
# =====================================
elif menu == "พยากรณ์เวลารอ":

    st.subheader("🧠 พยากรณ์ระยะเวลารอรับยา")

    st.write(
        "กรอกข้อมูลเพื่อแสดงตัวอย่างการคาดการณ์เวลารอรับยา"
    )

    col1, col2 = st.columns(2)

    with col1:
        drug_count = st.number_input(
            "จำนวนรายการยา",
            min_value=1,
            max_value=50,
            value=5
        )

        waiting_count = st.number_input(
            "จำนวนคิวก่อนหน้า",
            min_value=0,
            max_value=200,
            value=5
        )

    with col2:
        hour = st.selectbox(
            "ช่วงเวลาที่รับบริการ",
            [
                "08:00 - 09:00",
                "09:00 - 10:00",
                "10:00 - 11:00",
                "11:00 - 12:00",
                "13:00 - 14:00",
                "14:00 - 15:00"
            ]
        )

        patient_type = st.selectbox(
            "ประเภทผู้ป่วย",
            ["ผู้ป่วยนอกทั่วไป", "ผู้ป่วยนัด"]
        )

    if st.button("🔮 พยากรณ์เวลารอรับยา"):

        # ตัวอย่างสูตรจำลองเท่านั้น
        predicted_time = (
            5 + waiting_count * 3 + drug_count * 2
        )

        if hour in ["09:00 - 10:00", "10:00 - 11:00"]:
            predicted_time += 5

        if patient_type == "ผู้ป่วยนัด":
            predicted_time += 2

        st.markdown(
            f"""
            <div class="section-card">
                <p>เวลารอรับยาที่คาดการณ์</p>
                <h1 style="color:#1769D2;font-size:42px">
                    {predicted_time} นาที
                </h1>
                <p>ผลการคำนวณจากข้อมูลตัวอย่าง</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            "เมื่อมีข้อมูลจริง สามารถนำโมเดล "
            "Machine Learning มาเชื่อมต่อแทนสูตรตัวอย่างนี้ได้"
        )

# =====================================
# PAGE 4 : ADMIN
# =====================================
elif menu == "จัดการระบบ":

    st.subheader("⚙️ จัดการข้อมูลคิวรับยา")

    st.write("ข้อมูลคิวตัวอย่าง")

    edited_data = st.data_editor(
        queue_data,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    csv = edited_data.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "📥 ดาวน์โหลดข้อมูลคิว CSV",
        data=csv,
        file_name="mediqueue_data.csv",
        mime="text/csv"
    )

    st.success("สามารถแก้ไขและดาวน์โหลดข้อมูลตัวอย่างได้")

# =====================================
# FOOTER
# =====================================
st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#64748B">
        <p><b>MediQueue</b> | Hospital Pharmacy System</p>
        <p>ระบบต้นแบบเพื่อการศึกษา</p>
    </div>
    """,
    unsafe_allow_html=True
)
