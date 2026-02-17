import torch

def check_gpu():
    print(f"--- GPU Check ---")
    cuda_available = torch.cuda.is_available()
    print(f"CUDA Available: {cuda_available}")
    
    if cuda_available:
        print(f"GPU Device: {torch.cuda.get_device_name(0)}")
        print(f"Memory allocated: {torch.cuda.memory_allocated(0)/1024**3:.2f} GB")
        print(f"Memory reserved: {torch.cuda.memory_reserved(0)/1024**3:.2f} GB")
        
    print(f"PyTorch version: {torch.__version__}")

if __name__ == "__main__":
    try:
        check_gpu()
    except Exception as e:
        print(f"Error checking GPU: {e}")
