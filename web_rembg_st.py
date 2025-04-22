import streamlit as st
from PIL import Image
import os
import io
from rembg import remove

def main():
    st.set_page_config(page_title="圖片背景移除工具")
    
    st.title("圖片背景移除工具")
    st.write("上傳圖片並自動移除背景")
    
    # 上傳檔案
    uploaded_file = st.file_uploader("選擇要處理的圖片", type=["png", "jpg", "jpeg", "bmp", "gif"])
    
    col1, col2 = st.columns(2)
    
    if uploaded_file is not None:
        # 顯示原始圖片
        input_image = Image.open(uploaded_file)
        with col1:
            st.subheader("原始圖片")
            st.image(input_image, use_column_width=True)
        
        # 處理按鈕
        if st.button("移除背景"):
            with st.spinner("處理中..."):
                try:
                    # 移除背景
                    output_image = remove(input_image)
                    
                    # 顯示處理後的圖片
                    with col2:
                        st.subheader("去背後圖片")
                        st.image(output_image, use_column_width=True)
                    
                    # 提供下載功能
                    buf = io.BytesIO()
                    output_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="下載去背圖片",
                        data=byte_im,
                        file_name="removed_background.png",
                        mime="image/png"
                    )
                    
                    st.success("背景已成功移除!")
                    
                except Exception as e:
                    st.error(f"處理過程中發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()