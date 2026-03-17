import urllib.request
import urllib.error
import socket

# ==========================================
# テストするURLのリスト（先ほどの必須ドメイン）
# ==========================================
TEST_URLS = [
    "https://nvcr.io",
    "https://layers.nvcr.io",
    "https://pypi.org",
    "https://files.pythonhosted.org",
    "https://assets.ubuntu.com",
    "https://github.com",
    "https://api.github.com",
    "https://raw.githubusercontent.com"
]

TIMEOUT = 5  # タイムアウト秒数

def check_access(url):
    # システムのプロキシ設定（環境変数の HTTP_PROXY など）を自動で使用
    proxy_support = urllib.request.ProxyHandler()
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)

    # 弾かれにくくするために、一般的なブラウザのフリをする
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            status = response.getcode()
            body = response.read().decode('utf-8', errors='ignore')
            
            # ★ポイント：社内プロキシのブロック画面が返ってきていないかチェック
            if "w3.org/TR/html4/loose.dtd" in body or "Access Denied" in body or "blocked" in body.lower():
                return f"❌ ブロックされています（警告画面を検知 / Status: {status}）"
            
            return f"✅ 通信成功 (Status: {status})"

    except urllib.error.HTTPError as e:
        # 401(認証エラー)や 404(Not Found) は、宛先サーバーまで到達した結果のエラーなので
        # 「プロキシ自体は通過している（＝ホワイトリストは効いている）」と判断できます。
        body = e.read().decode('utf-8', errors='ignore')
        if "w3.org/TR/html4/loose.dtd" in body or "Access Denied" in body or "blocked" in body.lower():
            return f"❌ ブロックされています（警告画面を検知 / Status: {e.code}）"
            
        return f"✅ プロキシは通過しています (サーバー応答: {e.code} {e.reason})"

    except urllib.error.URLError as e:
        # 名前解決エラーや、プロキシによって完全に通信が遮断されている場合
        return f"❌ 通信失敗 (URLError: {e.reason})"
    
    except socket.timeout:
        return f"❌ タイムアウト（プロキシが応答を握りつぶしている可能性大）"
    except Exception as e:
        return f"❌ 予期せぬエラー: {e}"

def main():
    print("社内ネットワーク通信チェックを開始します...\n")
    print("-" * 60)
    for url in TEST_URLS:
        print(f"テスト中: {url}")
        result = check_access(url)
        print(f"結果: {result}")
        print("-" * 60)
    print("\nチェックが完了しました。")

if __name__ == "__main__":
    main()