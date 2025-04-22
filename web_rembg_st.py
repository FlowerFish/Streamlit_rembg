import streamlit as st
from PIL import Image
import io
from rembg import remove

# 頁面配置
st.set_page_config(
    page_title="AI圖片去背工具",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定義CSS
def load_css():
    st.markdown("""
    <style>
        /* 全局樣式 */
        .main {
            background-color: #f5f7f9;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* 標題樣式 */
        h1 {
            color: #2c3e50;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1.5rem;
            padding-top: 1rem;
        }
        
        /* 按鈕樣式 */
        .stButton>button {
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            border: none;
            width: 100%;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #2980b9;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        /* 區塊樣式 */
        .upload-section, .result-section, .info-box {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            margin-bottom: 2rem;
        }
        
        /* 下載按鈕 */
        .stDownloadButton>button {
            background-color: #27ae60;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            border: none;
            width: 100%;
            margin-top: 1rem;
            transition: all 0.3s ease;
        }
        .stDownloadButton>button:hover {
            background-color: #2ecc71;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        /* 加載指示器 */
        .stSpinner>div {
            border-color: #3498db !important;
        }
        
        /* 頁腳 */
        .footer {
            text-align: center;
            margin-top: 2rem;
            padding-bottom: 2rem;
            color: #7f8c8d;
            font-size: 0.8rem;
        }
        
        /* 特效 */
        .highlight {
            background: linear-gradient(120deg, rgba(52, 152, 219, 0.2) 0%, rgba(52, 152, 219, 0) 100%);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-weight: bold;
        }
        
        /* 響應式設計 */
        @media screen and (max-width: 768px) {
            .stApp {
                padding: 0.5rem !important;
            }
            h1 {
                font-size: 1.5rem !important;
            }
            .upload-section, .result-section, .info-box {
                padding: 1rem !important;
            }
        }
        
        /* 圖片容器 */
        .img-container {
            border: 1px dashed #bdc3c7;
            border-radius: 5px;
            padding: 0.5rem;
            text-align: center;
            background-color: #f9f9f9;
        }
        
        /* 徽章 */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            font-size: 0.75rem;
            font-weight: 700;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: 10rem;
            color: #fff;
            background-color: #3498db;
            margin-right: 0.5rem;
        }
        
        /* 信息提示框 */
        .info-box {
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 4px solid #3498db;
        }
        
        /* 選項卡樣式 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #f1f1f1;
            border-radius: 4px 4px 0 0;
            padding: 0.5rem 1rem;
            height: auto;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff;
            border-top: 2px solid #3498db;
        }
    </style>
    """, unsafe_allow_html=True)

# 調用CSS加載函數
load_css()

# App標題
st.markdown("<h1>✨ AI 智能圖片背景移除工具</h1>", unsafe_allow_html=True)

# 介紹文字
st.markdown("""
<div style="text-align: center; max-width: 700px; margin: 0 auto 2rem auto;">
    <p>使用先進的 <span class="highlight">InSPyReNet</span> 技術，輕鬆處理複雜圖像，完美保留人像細節、毛髮和產品輪廓。</p>
</div>
""", unsafe_allow_html=True)

# 創建頁面選項卡
tab1, tab2 = st.tabs(["📷 去背工具", "ℹ️ 使用說明"])

# 主工具頁面
with tab1:
    # 上傳區域
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 1rem;'>上傳圖片</h3>", unsafe_allow_html=True)
    
    # 上傳控件
    uploaded_file = st.file_uploader("選擇要處理的圖片", type=["png", "jpg", "jpeg", "bmp"], label_visibility="collapsed")
    
    if not uploaded_file:
        st.markdown("""
        <div style="text-align: center; color: #7f8c8d; padding: 2rem;">
            <i>拖放或點擊上方按鈕上傳圖片</i>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 處理區域
    if uploaded_file is not None:
        # 創建兩列佈局
        col1, col2 = st.columns(2)
        
        # 顯示原始圖片
        input_image = Image.open(uploaded_file)
        with col1:
            st.markdown("<h3 style='text-align: center;'>原始圖片</h3>", unsafe_allow_html=True)
            st.markdown('<div class="img-container">', unsafe_allow_html=True)
            st.image(input_image, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 處理按鈕
        button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
        with button_col2:
            process_button = st.button("🔮 一鍵移除背景")
        
        # 如果點擊了處理按鈕
        if process_button:
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            with st.spinner("🧙‍♂️ AI正在智能處理圖片中..."):
                try:
                    # 移除背景
                    output_image = remove(input_image)
                    
                    # 顯示處理後的圖片
                    with col2:
                        st.markdown("<h3 style='text-align: center;'>去背結果</h3>", unsafe_allow_html=True)
                        st.markdown('<div class="img-container">', unsafe_allow_html=True)
                        st.image(output_image, use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 提供下載功能
                    buf = io.BytesIO()
                    output_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    dl_col1, dl_col2, dl_col3 = st.columns([1, 2, 1])
                    with dl_col2:
                        st.download_button(
                            label="📥 下載去背圖片 (PNG透明背景)",
                            data=byte_im,
                            file_name="removed_background.png",
                            mime="image/png"
                        )
                    
                    st.success("✅ 處理成功！背景已完美移除")
                    
                except Exception as e:
                    st.error(f"❌ 處理過程中發生錯誤: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)

# 說明頁面
with tab2:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    ### 📝 使用說明
    
    本工具使用先進的 InSPyReNet 技術，專門針對以下類型的圖像進行優化：
    
    <div style="display: flex; gap: 1rem; margin: 1rem 0;">
        <div><span class="badge">👤</span> 人像照片</div>
        <div><span class="badge">🛍️</span> 產品圖像</div>
        <div><span class="badge">✂️</span> 複雜邊緣</div>
    </div>
    
    **使用步驟：**
    1. 上傳一張你想移除背景的圖片（支持JPG、PNG、JPEG、BMP格式）
    2. 點擊「一鍵移除背景」按鈕
    3. 等待AI處理完成
    4. 下載處理後的透明背景PNG圖片
    
    **優點：**
    - 智能識別圖像主體
    - 完美處理複雜髮絲和邊緣
    - 保留原始圖像細節和質量
    - 快速處理，節省編輯時間
    
    **提示：** 為獲得最佳效果，請上傳清晰、光線充足的圖片，背景與主體有明顯區分。
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 技術說明
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    ### 🔬 關於技術
    
    本工具采用 **InSPyReNet** 算法，這是一種基於深度學習的先進圖像分割技術，特別擅長處理：
    
    - **複雜髮絲：** 精確分離髮絲與背景
    - **透明和半透明物體：** 處理如玻璃、煙霧等複雜元素
    - **細微紋理：** 保留產品和對象的細微紋理和細節
    
    工具基於Streamlit構建，提供了直觀易用的Web界面，讓設計師、電商從業者和普通用戶無需專業圖像編輯軟件即可獲得專業級別的去背效果。
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 頁腳
st.markdown("""
<div class="footer">
    <p>由 InSPyReNet 技術驅動 | © 2025 AI圖片背景移除工具</p>
</div>
""", unsafe_allow_html=True)
