# Cloud Todo List Demo

Ứng dụng Todo List tối giản minh họa cách sử dụng Google Cloud Datastore với Flask/Python.

## Tính năng chính

- Tạo, xem, cập nhật và xóa các công việc (CRUD).
- Lưu trữ dữ liệu trên Datastore theo mô hình NoSQL (Entity/Kind/Property).
- Giao diện web đơn giản sử dụng Bootstrap.

## Cấu hình môi trường

1. Cài đặt Python 3.10+ và `pip`.
2. Sao chép file khóa dịch vụ Google Cloud (JSON) và đặt đường dẫn vào biến môi trường `GOOGLE_APPLICATION_CREDENTIALS`.
3. Đặt biến môi trường `GOOGLE_CLOUD_PROJECT` tương ứng với project ID của bạn.
4. (Tùy chọn) Đặt `FLASK_SECRET_KEY` để cấu hình secret key cho Flask.

Ví dụ trên Linux/macOS:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
export FLASK_SECRET_KEY="super-secret"
```

## Cài đặt phụ thuộc

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng local

```bash
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=8080
```

Ứng dụng sẽ chạy tại `http://localhost:8080`. Bạn có thể tạo mới, chỉnh sửa hoặc xóa công việc trực tiếp trên giao diện.

## Triển khai nhanh lên Google Cloud Run

1. Đảm bảo Google Cloud SDK đã được cài đặt và cấu hình project.
2. Xây dựng image và deploy:

```bash
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/cloud-todo-demo
gcloud run deploy cloud-todo-demo \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/cloud-todo-demo \
  --platform managed \
  --allow-unauthenticated
```

Ứng dụng sẽ tự động lấy thông tin chứng thực từ môi trường khi chạy trên Cloud Run/App Engine.
