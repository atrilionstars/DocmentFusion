import requests
import json

# API配置
BASE_URL = "http://192.168.1.13:8000/v1"
API_KEY = "2JysWWdHfyKvp2AsGYznw7pwPfkwDehtPZHEtj26GIA"
MODEL_NAME = "qwen-max"

# 请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# 测试文本生成
def test_text_generation():
    url = f"{BASE_URL}/chat/completions"
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": "你好，请介绍一下你自己"}
        ],
        "temperature": 0.7
    }

    try:
        # 发送请求
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        print("API响应状态码:", response.status_code)
        print("模型名称:", result.get("model", "未知"))
        print("生成内容:", result["choices"][0]["message"]["content"].strip())
        return True
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        if response.status_code == 401:
            print("认证失败，请检查API密钥是否正确")
        elif response.status_code == 404:
            print("API端点未找到，请检查URL是否正确")
        elif response.status_code == 500:
            print("服务器内部错误，请稍后再试")
        return False
    except (KeyError, json.JSONDecodeError) as e:
        print(f"响应解析错误: {e}")
        return False

# 测试模型列表
def test_model_list():
    url = f"{BASE_URL}/models"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        models = response.json().get("data", [])
        model_names = [model.get("id", "未知") for model in models]

        print("\n可用模型列表:")
        for name in model_names:
            print(f"- {name}")

        if MODEL_NAME in model_names:
            print(f"✅ 目标模型 '{MODEL_NAME}' 可用")
        else:
            print(f"❌ 目标模型 '{MODEL_NAME}' 不可用")

        return True
    except requests.exceptions.RequestException as e:
        print(f"获取模型列表失败: {e}")
        return False

if __name__ == "__main__":
    print(f"正在测试大模型API连通性 (模型: {MODEL_NAME})...")

    # 测试文本生成
    print("\n=== 测试文本生成 ===")
    text_gen_success = test_text_generation()

    # 测试模型列表
    print("\n=== 测试模型列表 ===")
    model_list_success = test_model_list()

    # 输出总体测试结果
    print("\n=== 测试结果 ===")
    if text_gen_success and model_list_success:
        print("✅ 所有测试通过，API连通性正常")
    else:
        print("❌ 测试未通过，请检查上述错误信息")