import requests

url = "https://cinestar.com.vn/_next/image/?url=https%3A%2F%2Fapi-website.cinestar.com.vn%2Fmedia%2Fwysiwyg%2FPosters%2F10-2025%2FCNEN_MAIN2_1500x1200.jpg&w=1920&q=75"
file_name = "src/assets/poster/chi_nga_em_nang.jpg"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open(file_name, "wb") as f:
        f.write(response.content)
    print(f"Tải thành công, lưu tại {file_name}")
else:
    print("Không tải được ảnh, mã lỗi:", response.status_code)
