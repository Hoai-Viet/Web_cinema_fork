import requests

url = "https://www.techtarget.com/rms/onlineImages/erp-supply_chain_management.png"
file_name = "src/assets/poster/SCM.jpg"

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
