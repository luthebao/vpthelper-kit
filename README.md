# VPTHELPER KIT OPENSOURCE

## Giới thiệu

- Đây là bộ kit để tự làm Auto game Vua Pháp Thuật
- Bộ kit có sử dụng OpenCV (xử lý hình ảnh), Py Memory (xử lý đọc dữ liệu từ RAM) và Win32 Api (Click chuột, ...)

## Miễn trừ trách nhiệm

- Lưu ý: đây là công cụ để thiết lập thao tác chuột làm auto click, công cụ này không thể tác động vào mã nguồn game.
- Công cụ được public để phục vụ cho việc nghiên cứu cá nhân, mình không chịu trách nhiệm cho toàn bộ mục đích sử dụng của người dùng.

## Hướng dẫn

1. Cài đặt môi trường python (virtual env)

2. Cài đặt các gói tiện ích từ requirements.txt:

```python
pip install -r requirements.txt
```

3. Import `helperkit` vào dự án và sử dụng

## Kiến thức liên quan

1. Python
2. Cheat Engine: [Pointer Scan](https://www.youtube.com/watch?v=8oC0w6WhZ1E)

## Công cụ hỗ trợ

1. Dev Helper `dev-helper.py`

![dev-helper](/assets/dev-helper.png)

2. Tìm hiểu thêm tại [wiki](/wiki)

## Lưu ý

- VPT HELPER KIT chỉ sử dụng được trên **windows**
- Chỉ sử dụng được file **flash.exe** (Flash 10) để log game. Nếu muốn đổi flash bạn cần có kiến thức về Cheat Engine và Memory để sửa lại các pointer trong class HelperKit
- File **acc.txt** để lưu trữ danh sách link acc. Có thể chỉnh sửa lại tên file trong class **AccountInfo**
