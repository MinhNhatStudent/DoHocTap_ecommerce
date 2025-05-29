import os
import shutil
import platform

def delete_model_cache():
    """Delete cache directories for Hugging Face and Sentence Transformers"""
    # Get home directory based on platform
    home_dir = os.path.expanduser("~")
    
    # Define cache directories
    huggingface_cache = os.path.join(home_dir, ".cache", "huggingface")
    sentence_transformers_cache = os.path.join(home_dir, ".cache", "torch", "sentence_transformers")
    
    # Check and delete Hugging Face cache
    if os.path.exists(huggingface_cache):
        try:
            shutil.rmtree(huggingface_cache)
            print(f"✓ Đã xóa cache HuggingFace tại: {huggingface_cache}")
        except Exception as e:
            print(f"✗ Lỗi khi xóa cache HuggingFace: {e}")
    else:
        print(f"ℹ️ Không tìm thấy cache HuggingFace tại: {huggingface_cache}")
    
    # Check and delete Sentence Transformers cache
    if os.path.exists(sentence_transformers_cache):
        try:
            shutil.rmtree(sentence_transformers_cache)
            print(f"✓ Đã xóa cache Sentence Transformers tại: {sentence_transformers_cache}")
        except Exception as e:
            print(f"✗ Lỗi khi xóa cache Sentence Transformers: {e}")
    else:
        print(f"ℹ️ Không tìm thấy cache Sentence Transformers tại: {sentence_transformers_cache}")
    
    print("\nHoàn thành xóa cache. Hệ thống sẽ tải lại mô hình khi chạy lại ứng dụng.")

if __name__ == "__main__":
    print("Bắt đầu xóa cache mô hình...\n")
    delete_model_cache()
    
    # Keep console window open until user presses a key (for Windows)
    if platform.system() == "Windows":
        input("\nNhấn Enter để đóng cửa sổ...")